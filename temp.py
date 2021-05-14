import tkinter as tk

root = tk.Tk()

root.title("Temperature Converter")

mf = tk.Frame(root)
mf.grid(column=0, row=0, sticky='nswe')

C = tk.DoubleVar()
F = tk.DoubleVar()

Ce = tk.Entry(mf, textvariable=C)
Fe = tk.Entry(mf, textvariable=F)

Cl = tk.Label(mf, text="Celsius =")
Fl = tk.Label(mf, text="Fahrenheit")

Ce.grid(column=0, row=0, sticky='nswe')
Cl.grid(column=1, row=0, sticky='nswe')
Fe.grid(column=2, row=0, sticky='nswe')
Fl.grid(column=3, row=0, sticky='nswe')


def C_update(*a):
    Fe.delete(0, 'end')
    Fe.insert(0, (C.get()) * (9 / 5) + 32)


def F_update(*a):
    Ce.delete(0, 'end')
    Ce.insert(0, ((F.get()) - 32) * (5 / 9))


Ce.bind('<KeyRelease>', C_update)
Fe.bind('<KeyRelease>', F_update)

root.mainloop()
