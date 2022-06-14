#https://www.pythontutorial.net/tkinter/tkinter-treeview/
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from random import randint
# create root window
root = tk.Tk()
root.title('Treeview Demo - Hierarchical Data')
root.geometry('400x200')

# configure the grid layout
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)


# create a treeview
tree = ttk.Treeview(root)


# adding data
tree.insert('', tk.END, text='Administration', iid=0, open=False)
tree.insert('', tk.END, text='Logistics', iid=1, open=False)
tree.insert('', tk.END, text='Sales', iid=2, open=False)
tree.insert('', tk.END, text='Finance', iid=3, open=False)
tree.insert('', tk.END, text='IT', iid=4, open=False)
tree.insert('', tk.END, text='John Doe', iid=5, open=False)
tree.insert('', tk.END, text='Jane Doe', iid=6, open=False)
# defining children of the nodes
tree.move(5, 0, 0)

def mover_aleatorio():
    tree.move(6, randint(0,5), 0)

# place the Treeview widget on the root window
tree.grid(row=0, column=0, sticky='nsew')
boton = ttk.Button(root, text='mover', command=mover_aleatorio)
boton.grid(row=1, column=0, sticky='nsew')

# run the app
root.mainloop()