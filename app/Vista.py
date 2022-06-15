from tkinter import Button, PhotoImage, Text, Tk, ttk, END
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
        self.tree.bind("<<TreeviewOpen>>", self.tree_click)
        self.tree.bind("<<TreeviewClose>>", self.tree_click)
        self.console = Text(self)
        self.console.insert(END, ">>> ")
        self.console.grid(row=1, column=0, sticky='nsew')
        self.console.bind("<Return>", self.procesar_comando)
        self.icono_archivo = PhotoImage(file='assets/archivo.png')
        self.icono_directorio = PhotoImage(file='assets/directorio.png')
        self.FileSystem = FileSystem()
    def tree_click(self, event):
        self.FileSystem.tocar(int(self.tree.focus()))
    
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
        self.tree.insert('', END, image=self.icono_directorio, text=r.nombre, iid=r.id, open=r.abierto)
        self.generarArbol(r)
    def generarArbol(self,raiz:Directorio):
        for archivo in raiz.archivos:
            self.tree.insert(raiz.id, END, image=self.icono_archivo, text=archivo.nombre, iid=archivo.id, open=False)
        for directorio in raiz.directorios:
            self.tree.insert(raiz.id, END, image=self.icono_directorio, text=directorio.nombre, iid=directorio.id, open=directorio.abierto)
            self.generarArbol(directorio)

if __name__ == "__main__":
    Vista().mainloop()
else:
    print(__name__)