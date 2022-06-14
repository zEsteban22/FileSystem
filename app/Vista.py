from tkinter import Tk, ttk, END
from FileSystem import FileSystem, Archivo, Directorio

class Vista(Tk):
    def __init__(self):
        super().__init__()
        self.title("File System")
        self.geometry("400x200")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.tree = ttk.Treeview(self)
        self.tree.grid(row=0, column=0, sticky='nsew')
    def actualizarArbol(self,raiz:Directorio):
        self.tree.delete(*self.tree.get_children())
        self.tree.insert('', END, text=raiz.nombre, iid=raiz.id, open=False)
        self.generarArbol(raiz)
    def generarArbol(self,raiz:Directorio):
        for archivo in raiz.archivos:
            self.tree.insert(raiz.id, END, text=archivo.nombre, iid=archivo.id, open=False)
        for directorio in raiz.directorios:
            self.tree.insert(raiz.id, END, text=directorio.nombre, iid=directorio.id, open=False)
            self.generarArbol(directorio)
    