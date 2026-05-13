import tkinter as tk
from typing import Literal

Name = tuple[str, str]


class NameStore:
    def __init__(self) -> None:
        self.names: list[Name] = [
            ("Emil", "Hans"),
            ("Mustermann", "Max"),
            ("Tisch", "Roman"),
        ]

    def filtered(self, prefix: str) -> list[tuple[int, Name]]:
        prefix = prefix.lower()
        return [(i, n) for i, n in enumerate(self.names) if n[1].lower().startswith(prefix)]

    def create(self, name: str, surname: str) -> None:
        self.names.append((name, surname))

    def update(self, index: int, name: str, surname: str) -> None:
        self.names[index] = (name, surname)

    def delete(self, index: int) -> None:
        del self.names[index]


def main() -> None:
    root = tk.Tk()
    root.title("CRUD")

    store = NameStore()
    prefix = tk.StringVar()
    name = tk.StringVar()
    surname = tk.StringVar()
    visible_indices: list[int] = []

    root.columnconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)

    filter_frame = tk.Frame(root)
    filter_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 4), sticky="ew")
    filter_frame.columnconfigure(1, weight=1)
    tk.Label(filter_frame, text="Filter prefix:").grid(row=0, column=0, sticky="w")
    tk.Entry(filter_frame, textvariable=prefix).grid(row=0, column=1, padx=(6, 0), sticky="ew")

    listbox = tk.Listbox(root, exportselection=False)
    listbox.grid(row=1, column=0, padx=(10, 4), pady=4, sticky="nsew")

    form = tk.Frame(root)
    form.grid(row=1, column=1, padx=(4, 10), pady=4, sticky="nsew")
    form.columnconfigure(1, weight=1)
    tk.Label(form, text="Name:").grid(row=0, column=0, sticky="w")
    tk.Entry(form, textvariable=name).grid(row=0, column=1, sticky="ew")
    tk.Label(form, text="Surname:").grid(row=1, column=0, pady=(6, 0), sticky="w")
    tk.Entry(form, textvariable=surname).grid(row=1, column=1, pady=(6, 0), sticky="ew")

    buttons = tk.Frame(root)
    buttons.grid(row=2, column=0, columnspan=2, padx=10, pady=(4, 10), sticky="ew")
    buttons.columnconfigure((0, 1, 2), weight=1)
    create_button = tk.Button(buttons, text="Create")
    update_button = tk.Button(buttons, text="Update")
    delete_button = tk.Button(buttons, text="Delete")
    create_button.grid(row=0, column=0, sticky="ew")
    update_button.grid(row=0, column=1, padx=6, sticky="ew")
    delete_button.grid(row=0, column=2, sticky="ew")

    def selected_index() -> int | None:
        selection = listbox.curselection()
        if not selection:
            return None
        return visible_indices[selection[0]]

    def refresh(keep: int | None = None) -> None:
        nonlocal visible_indices
        shown = store.filtered(prefix.get())
        visible_indices = [index for index, _ in shown]
        listbox.delete(0, "end")
        for _, (first, last) in shown:
            listbox.insert("end", f"{last}, {first}")
        if keep in visible_indices:
            listbox.selection_set(visible_indices.index(keep))
        selection_changed()

    def selection_changed(*_: tk.Event | str) -> None:
        index = selected_index()
        state: Literal["normal", "disabled"] = "normal" if index is not None else "disabled"
        update_button.configure(state=state)
        delete_button.configure(state=state)
        if index is not None:
            first, last = store.names[index]
            name.set(first)
            surname.set(last)

    def create() -> None:
        store.create(name.get(), surname.get())
        refresh(len(store.names) - 1)

    def update() -> None:
        index = selected_index()
        if index is not None:
            store.update(index, name.get(), surname.get())
            refresh(index)

    def delete() -> None:
        index = selected_index()
        if index is not None:
            store.delete(index)
            refresh()

    create_button.configure(command=create)
    update_button.configure(command=update)
    delete_button.configure(command=delete)
    listbox.bind("<<ListboxSelect>>", selection_changed)
    prefix.trace_add("write", lambda *_: refresh())
    refresh()

    root.mainloop()


if __name__ == "__main__":
    main()
