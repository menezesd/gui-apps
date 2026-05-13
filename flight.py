import tkinter as tk
from datetime import date, datetime
from tkinter import messagebox, ttk


DATE_FORMAT = "%d.%m.%Y"


def parse_date(text: str) -> date | None:
    try:
        return datetime.strptime(text, DATE_FORMAT).date()
    except ValueError:
        return None


def main() -> None:
    root = tk.Tk()
    root.title("Flight Booker")

    flight_type = tk.StringVar(value="one-way flight")
    start = tk.StringVar(value="04.04.2014")
    end = tk.StringVar(value="04.04.2014")

    combo = ttk.Combobox(
        root,
        textvariable=flight_type,
        values=("one-way flight", "return flight"),
        state="readonly",
        width=18,
    )
    start_entry = tk.Entry(root, textvariable=start, width=18)
    end_entry = tk.Entry(root, textvariable=end, width=18)
    book_button = tk.Button(root, text="Book")

    combo.grid(row=0, column=0, padx=10, pady=(10, 4), sticky="ew")
    start_entry.grid(row=1, column=0, padx=10, pady=4, sticky="ew")
    end_entry.grid(row=2, column=0, padx=10, pady=4, sticky="ew")
    book_button.grid(row=3, column=0, padx=10, pady=(4, 10), sticky="ew")

    def validate(*_: str) -> None:
        start_date = parse_date(start.get())
        end_date = parse_date(end.get())
        is_return = flight_type.get() == "return flight"

        end_entry.configure(state="normal" if is_return else "disabled")
        start_entry.configure(bg="white" if start_date else "#ffcccc")
        end_entry.configure(bg="white" if end_date or not is_return else "#ffcccc")

        valid = start_date is not None
        if is_return:
            valid = start_date is not None and end_date is not None and end_date >= start_date
        book_button.configure(state="normal" if valid else "disabled")

    def book() -> None:
        if flight_type.get() == "one-way flight":
            message = f"You have booked a one-way flight on {start.get()}."
        else:
            message = f"You have booked a return flight from {start.get()} to {end.get()}."
        messagebox.showinfo("Flight booked", message)

    book_button.configure(command=book)
    flight_type.trace_add("write", validate)
    start.trace_add("write", validate)
    end.trace_add("write", validate)
    validate()

    root.mainloop()


if __name__ == "__main__":
    main()
