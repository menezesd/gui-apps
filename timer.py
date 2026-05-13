import time
import tkinter as tk
from tkinter import ttk


MAX_DURATION = 30.0
TICK_MS = 50


def main() -> None:
    root = tk.Tk()
    root.title("Timer")

    elapsed = tk.DoubleVar(value=0.0)
    duration = tk.DoubleVar(value=10.0)
    last_tick: dict[str, float] = {"time": time.monotonic()}

    tk.Label(root, text="Elapsed Time:").grid(row=0, column=0, padx=10, pady=(10, 4), sticky="w")
    gauge = ttk.Progressbar(root, maximum=1.0, length=240)
    gauge.grid(row=0, column=1, padx=10, pady=(10, 4), sticky="ew")

    elapsed_label = tk.Label(root, width=10, anchor="w")
    elapsed_label.grid(row=1, column=1, padx=10, pady=4, sticky="w")

    tk.Label(root, text="Duration:").grid(row=2, column=0, padx=10, pady=4, sticky="w")
    slider = tk.Scale(
        root,
        from_=0.1,
        to=MAX_DURATION,
        resolution=0.1,
        orient="horizontal",
        variable=duration,
        showvalue=False,
        length=240,
    )
    slider.grid(row=2, column=1, padx=10, pady=4, sticky="ew")

    reset_button = tk.Button(root, text="Reset")
    reset_button.grid(row=3, column=1, padx=10, pady=(4, 10), sticky="ew")

    root.columnconfigure(1, weight=1)

    def refresh() -> None:
        ratio = min(elapsed.get() / duration.get(), 1.0)
        gauge.configure(value=ratio)
        elapsed_label.configure(text=f"{elapsed.get():.1f}s")

    def reset() -> None:
        elapsed.set(0.0)
        last_tick["time"] = time.monotonic()
        refresh()

    def tick() -> None:
        now = time.monotonic()
        if elapsed.get() < duration.get():
            elapsed.set(min(elapsed.get() + now - last_tick["time"], duration.get()))
        last_tick["time"] = now
        refresh()
        root.after(TICK_MS, tick)

    reset_button.configure(command=reset)
    duration.trace_add("write", lambda *_: refresh())
    refresh()
    root.after(TICK_MS, tick)
    root.mainloop()


if __name__ == "__main__":
    main()
