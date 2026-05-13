import copy
import math
import tkinter as tk


DEFAULT_DIAMETER = 30
Circle = dict[str, float]
Snapshot = list[Circle]


class CircleDrawer:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.circles: Snapshot = []
        self.selected: int | None = None
        self.undo_stack: list[Snapshot] = []
        self.redo_stack: list[Snapshot] = []
        self.drag_start_snapshot: Snapshot | None = None

        toolbar = tk.Frame(root)
        toolbar.pack(fill="x", padx=10, pady=(10, 4))
        self.undo_button = tk.Button(toolbar, text="Undo", command=self.undo)
        self.redo_button = tk.Button(toolbar, text="Redo", command=self.redo)
        self.undo_button.pack(side="left")
        self.redo_button.pack(side="left", padx=(6, 0))

        self.canvas = tk.Canvas(root, width=520, height=360, bg="white")
        self.canvas.pack(fill="both", expand=True, padx=10, pady=(4, 10))
        self.canvas.bind("<Button-1>", self.create_circle)
        self.canvas.bind("<Motion>", self.select_nearest)
        self.canvas.bind("<Button-3>", self.open_menu)
        self.canvas.bind("<Button-2>", self.open_menu)

        self.menu = tk.Menu(root, tearoff=False)
        self.menu.add_command(label="Adjust diameter...", command=self.open_adjuster)
        self.update_buttons()

    def snapshot(self) -> Snapshot:
        return copy.deepcopy(self.circles)

    def restore(self, circles: Snapshot) -> None:
        self.circles = copy.deepcopy(circles)
        self.selected = None
        self.draw()

    def commit(self, before: Snapshot | None) -> None:
        if before is None:
            return
        if before != self.circles:
            self.undo_stack.append(before)
            self.redo_stack.clear()
            self.update_buttons()

    def update_buttons(self) -> None:
        self.undo_button.configure(state="normal" if self.undo_stack else "disabled")
        self.redo_button.configure(state="normal" if self.redo_stack else "disabled")

    def create_circle(self, event: tk.Event) -> None:
        if self.hit(event.x, event.y) is not None:
            return
        before = self.snapshot()
        self.circles.append({"x": event.x, "y": event.y, "diameter": DEFAULT_DIAMETER})
        self.commit(before)
        self.draw()

    def hit(self, x: int, y: int) -> int | None:
        candidates: list[tuple[float, int]] = []
        for i, circle in enumerate(self.circles):
            radius = circle["diameter"] / 2
            distance = math.hypot(x - circle["x"], y - circle["y"])
            if distance < radius:
                candidates.append((distance, i))
        return min(candidates)[1] if candidates else None

    def select_nearest(self, event: tk.Event) -> None:
        self.selected = self.hit(event.x, event.y)
        self.draw()

    def open_menu(self, event: tk.Event) -> None:
        self.selected = self.hit(event.x, event.y)
        self.draw()
        if self.selected is not None:
            self.menu.tk_popup(event.x_root, event.y_root)

    def open_adjuster(self) -> None:
        if self.selected is None:
            return
        index = self.selected
        self.drag_start_snapshot = self.snapshot()

        win = tk.Toplevel(self.root)
        win.title("Adjust diameter")
        diameter = tk.IntVar(value=int(self.circles[index]["diameter"]))

        def change(value: str) -> None:
            if index < len(self.circles):
                self.circles[index]["diameter"] = int(float(value))
                self.draw()

        def close() -> None:
            self.commit(self.drag_start_snapshot)
            win.destroy()

        tk.Scale(
            win,
            from_=10,
            to=200,
            orient="horizontal",
            variable=diameter,
            command=change,
            length=260,
        ).pack(padx=12, pady=12)
        win.protocol("WM_DELETE_WINDOW", close)

    def undo(self) -> None:
        if not self.undo_stack:
            return
        self.redo_stack.append(self.snapshot())
        self.restore(self.undo_stack.pop())
        self.update_buttons()

    def redo(self) -> None:
        if not self.redo_stack:
            return
        self.undo_stack.append(self.snapshot())
        self.restore(self.redo_stack.pop())
        self.update_buttons()

    def draw(self) -> None:
        self.canvas.delete("all")
        for i, circle in enumerate(self.circles):
            radius = circle["diameter"] / 2
            fill = "#b8b8b8" if i == self.selected else ""
            self.canvas.create_oval(
                circle["x"] - radius,
                circle["y"] - radius,
                circle["x"] + radius,
                circle["y"] + radius,
                fill=fill,
                outline="black",
            )


def main() -> None:
    root = tk.Tk()
    root.title("Circle Drawer")
    CircleDrawer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
