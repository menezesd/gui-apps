import tkinter as tk

def my_click():
    my_click.counter = getattr(my_click, 'counter', 0) + 1
    g.configure(state='normal')
    g.delete(0,'end')
    g.insert(0, str(my_click.counter))
    g.configure(state='readonly')

window = tk.Tk()

g = tk.Entry (state = "readonly")
g.pack()
g.insert(0,  "Hello World!" )

b = tk.Button(text="Count", command=my_click)
b.pack()


window.mainloop()
