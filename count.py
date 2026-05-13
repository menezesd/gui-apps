import tkinter as tk


def main() -> None:
    root = tk.Tk()
    root.title("Counter")

    value = tk.IntVar(value=0)

    display = tk.Entry(root, textvariable=value, state="readonly", width=12)
    display.grid(row=0, column=0, padx=10, pady=10)

    button = tk.Button(root, text="Count", command=lambda: value.set(value.get() + 1))
    button.grid(row=0, column=1, padx=(0, 10), pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
