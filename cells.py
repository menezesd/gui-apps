import ast
import re
import tkinter as tk
from typing import Any
from tkinter import simpledialog, ttk


ROWS = 100
COLS = 26
CELL_RE = re.compile(r"\b([A-Z])([0-9]{1,2})\b")
Cell = tuple[str, int]


class Spreadsheet:
    def __init__(self) -> None:
        self.formulas: dict[Cell, str] = {}
        self.values: dict[Cell, str] = {}
        self.dependencies: dict[Cell, set[Cell]] = {}
        self.dependents: dict[Cell, set[Cell]] = {}

    def set_formula(self, cell: Cell, formula: str) -> set[Cell]:
        old_dependencies = self.dependencies.get(cell, set())
        for dep in old_dependencies:
            self.dependents.get(dep, set()).discard(cell)

        self.formulas[cell] = formula
        deps = set(CELL_RE.findall(formula.upper()))
        deps = {(col, int(row)) for col, row in deps if int(row) < ROWS}
        self.dependencies[cell] = deps
        for dep in deps:
            self.dependents.setdefault(dep, set()).add(cell)

        changed = self.propagate_from(cell)
        return changed

    def propagate_from(self, start: Cell) -> set[Cell]:
        queue: list[Cell] = [start]
        seen: set[Cell] = set()
        changed: set[Cell] = set()
        while queue:
            cell = queue.pop(0)
            if cell in seen:
                continue
            seen.add(cell)
            old = self.values.get(cell, "")
            self.values[cell] = self.evaluate(cell, set())
            if self.values[cell] != old:
                changed.add(cell)
                queue.extend(self.dependents.get(cell, set()))
        return changed

    def value(self, cell: Cell) -> str:
        return self.values.get(cell, "")

    def evaluate(self, cell: Cell, visiting: set[Cell]) -> str:
        if cell in visiting:
            return "#CYCLE"
        formula = self.formulas.get(cell, "")
        if formula == "":
            return ""
        if not formula.startswith("="):
            return formula

        def replace(match: re.Match[str]) -> str:
            ref = (match.group(1), int(match.group(2)))
            value = self.evaluate(ref, visiting | {cell})
            try:
                return str(float(value))
            except (TypeError, ValueError):
                return "0"

        expression = CELL_RE.sub(replace, formula[1:].upper())
        try:
            tree = ast.parse(expression, mode="eval")
            if not self.safe_expression(tree):
                return "#ERR"
            result: Any = eval(compile(tree, "<cell>", "eval"), {"__builtins__": {}}, {})
            return f"{result:g}" if isinstance(result, (int, float)) else str(result)
        except Exception:
            return "#ERR"

    def safe_expression(self, tree: ast.AST) -> bool:
        allowed = (
            ast.Expression,
            ast.BinOp,
            ast.UnaryOp,
            ast.Constant,
            ast.Add,
            ast.Sub,
            ast.Mult,
            ast.Div,
            ast.USub,
            ast.UAdd,
            ast.Mod,
            ast.Pow,
        )
        return all(isinstance(node, allowed) for node in ast.walk(tree))


class CellsApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.sheet = Spreadsheet()
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)

        self.tree = ttk.Treeview(
            root,
            columns=[chr(65 + i) for i in range(COLS)],
            show="tree headings",
        )
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.tree.heading("#0", text="")
        self.tree.column("#0", width=48, minwidth=48, anchor="e", stretch=False)

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=72, minwidth=60, anchor="center")
        for row in range(ROWS):
            self.tree.insert("", "end", iid=str(row), text=str(row), values=["" for _ in range(COLS)])

        yscroll = ttk.Scrollbar(root, orient="vertical", command=self.tree.yview)
        xscroll = ttk.Scrollbar(root, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)
        yscroll.grid(row=0, column=1, sticky="ns")
        xscroll.grid(row=1, column=0, sticky="ew")

        self.tree.bind("<Double-1>", self.edit_cell)

    def edit_cell(self, event: tk.Event) -> None:
        row_id = self.tree.identify_row(event.y)
        column_id = self.tree.identify_column(event.x)
        if not row_id or not column_id:
            return
        col_index = int(column_id[1:]) - 1
        cell = (chr(65 + col_index), int(row_id))
        current = self.sheet.formulas.get(cell, "")
        formula = simpledialog.askstring("Edit cell", f"{cell[0]}{cell[1]}", initialvalue=current)
        if formula is None:
            return
        changed = self.sheet.set_formula(cell, formula)
        changed.add(cell)
        for changed_cell in changed:
            self.refresh_cell(changed_cell)

    def refresh_cell(self, cell: Cell) -> None:
        col, row = cell
        values = list(self.tree.item(str(row), "values"))
        values[ord(col) - 65] = self.sheet.value(cell)
        self.tree.item(str(row), values=values)


def main() -> None:
    root = tk.Tk()
    root.title("Cells")
    root.geometry("900x480")
    CellsApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
