from tkinter import Button, Text, Tk, ttk, END
from FileSystem import FileSystem, Archivo, Directorio

class Vista(Tk):
    def __init__(self):
        super().__init__()
        self.title("File System")
        self.geometry("400x600")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.tree = ttk.Treeview(self)
        self.tree.grid(row=0, column=0, sticky='nsew')
        #Button(self, text='Actualizar árbol', command=self.actualizarArbol).grid(row=1, column=0)
        self.console = Text(self)
        self.console.insert(END, ">>> ")
        self.console.grid(row=1, column=0, sticky='nsew')
        self.console.bind("<Return>", self.procesar_comando)
        self.FileSystem = FileSystem()
    def procesar_comando(self,event):
        comando = self.console.get("end-1c linestart+4c", "end-1c")
        respuesta = self.FileSystem.procesar_comando(comando)
        self.console.insert(END, "\n")
        self.console.insert(END, respuesta)
        self.console.insert(END, "\n>>> ")
        try:
            self.actualizarArbol()
        except:
            pass
        return "break"
    def actualizarArbol(self):
        r = self.FileSystem.raiz
        self.tree.delete(*self.tree.get_children())
        self.tree.insert('', END, text=r.nombre, iid=r.id, open=r.abierto)
        self.generarArbol(r)
    def generarArbol(self,raiz:Directorio):
        for archivo in raiz.archivos:
            self.tree.insert(raiz.id, END, text=archivo.nombre, iid=archivo.id, open=False)
        for directorio in raiz.directorios:
            self.tree.insert(raiz.id, END, text=directorio.nombre, iid=directorio.id, open=directorio.abierto)
            self.generarArbol(directorio)

if __name__ == "__main__":
    Vista().mainloop()
else:
    print(__name__)