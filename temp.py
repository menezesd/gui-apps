import tkinter as tk


def parse_number(text: str) -> float | None:
    try:
        return float(text)
    except ValueError:
        return None


def main() -> None:
    root = tk.Tk()
    root.title("Temperature Converter")

    celsius = tk.StringVar()
    fahrenheit = tk.StringVar()
    updating: dict[str, bool] = {"active": False}

    def set_from_celsius(*_: str) -> None:
        if updating["active"]:
            return
        value = parse_number(celsius.get())
        if value is None:
            return
        updating["active"] = True
        fahrenheit.set(f"{value * 9 / 5 + 32:g}")
        updating["active"] = False

    def set_from_fahrenheit(*_: str) -> None:
        if updating["active"]:
            return
        value = parse_number(fahrenheit.get())
        if value is None:
            return
        updating["active"] = True
        celsius.set(f"{(value - 32) * 5 / 9:g}")
        updating["active"] = False

    tk.Entry(root, textvariable=celsius, width=12).grid(row=0, column=0, padx=(10, 4), pady=10)
    tk.Label(root, text="Celsius =").grid(row=0, column=1, padx=4, pady=10)
    tk.Entry(root, textvariable=fahrenheit, width=12).grid(row=0, column=2, padx=4, pady=10)
    tk.Label(root, text="Fahrenheit").grid(row=0, column=3, padx=(4, 10), pady=10)

    celsius.trace_add("write", set_from_celsius)
    fahrenheit.trace_add("write", set_from_fahrenheit)

    root.mainloop()


if __name__ == "__main__":
    main()
