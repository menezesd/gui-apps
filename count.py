import tkinter as tk

def my_click():
    ''' This function is called when clicking on the button'''
    v.set(v.get() + 1)

window = tk.Tk()

v = tk.IntVar()
g = tk.Entry (state = "readonly", textvariable=v)
g.pack()
g.insert(0,  "Hello World!" )

b = tk.Button(text="Count", command=my_click)
b.pack()


window.mainloop()
