from tkinter import Button, Label, Menu, PhotoImage, Text, Tk, ttk, END
from FileSystem import FileSystem, Archivo, Directorio

class VistaContenido(Tk):
    def __init__(self,nombre:str,cont:str):
        super().__init__()
        self.title(nombre)
        self.geometry("350x300")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        label = Label(self,text=cont)
        label.grid(row=0, column=0, sticky='nw')


class VistaPropiedades(Tk):
    def __init__(self,props:str):
        super().__init__()
        self.title("Propiedades del Archivo")
        self.geometry("350x300")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        label = Label(self,text=props)
        label.grid(row=0, column=0, sticky='nsew')
        
class Vista(Tk):
    def __init__(self):
        super().__init__()
        self.title("File System")
        self.geometry("400x600")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.tree = ttk.Treeview(self)
        self.tree.grid(row=0, column=0, sticky='nsew')
        self.tree.bind("<<TreeviewOpen>>", self.tree_open)
        self.tree.bind("<<TreeviewClose>>", self.tree_close)

        self.menu_click_derecho = Menu(self, tearoff=0)
        self.menu_click_derecho.add_command(label="Abrir", command=self.abrir_archivo)
        self.menu_click_derecho.add_command(label="Eliminar", command=self.eliminar_archivo)
        #self.menu_click_derecho.add_command(label="Renombrar", command=self.renombrar_archivo)
        self.menu_click_derecho.add_command(label="Propiedades", command=self.ver_propiedades)
        self.tree.bind("<Button-3>", self.desplegar_menu_click_derecho)
        
        self.console = Text(self)
        #self.console.insert(END, self.FileSystem.get_actual_dir())
        self.console.insert(END, "\n>>> ")
        self.console.grid(row=1, column=0, sticky='nsew')
        self.console.bind("<Return>", self.procesar_comando)
        self.console.bind("<Key>", self.procesar_tecla)
        
        self.icono_archivo = PhotoImage(file='assets/archivo.png')
        self.icono_directorio = PhotoImage(file='assets/directorio.png')
        
        self.abiertos = []
        
        self.FileSystem = FileSystem()
    
    
    def tree_close(self, event):
        self.abiertos.remove(int(self.tree.focus()))

    def tree_open(self, event):
        self.abiertos += [int(self.tree.focus())]

    def abrir_archivo(self):
        print(self.tree.selection())
        for iid in self.tree.selection():
            archivo = self.FileSystem.get_archivo_id(int(iid))
            try:
                VistaContenido(archivo.nombre,archivo.contenido)
            except:
                pass
    
    def eliminar_archivo(self):
        for iid in self.tree.selection():
            self.FileSystem.borrar_seleccionado(int(iid))
        self.actualizarArbol()

    def ver_propiedades(self):
        tree_selection = self.tree.selection()
        if len(tree_selection) == 1:
            VistaPropiedades(self.FileSystem.propiedades(int(tree_selection[0])))

    def desplegar_menu_click_derecho(self,event):
        if len(self.tree.selection()) <= 1:
            #select item at mouse position
            self.tree.selection_set(self.tree.identify_row(event.y))
        self.menu_click_derecho.tk_popup(event.x_root, event.y_root)

    def procesar_comando(self,event):
        comando = self.console.get("end-1c linestart+4c", "end-1c")
        respuesta = self.FileSystem.procesar_comando(comando)
        self.console.insert(END, "\n"+respuesta)
        self.console.insert(END, "\n"+self.FileSystem.get_actual_dir())
        self.console.insert(END, "\n>>> ")
        try:
            self.actualizarArbol()
        except:
            pass
        return "break"

    def procesar_tecla(self,event):
        line, col = self.console.index("insert").split('.')
        
        if int(col) < 4 or str(int(line) + 1) != self.console.index('end').split('.')[0] or event.keycode == 46 and int(col) < 4 or len(event.char) > 0 and ord(event.char) == 8 and int(col) < 5:
            self.console.mark_set('insert','end')
            return "break"
        

    def actualizarArbol(self):
        r = self.FileSystem.raiz
        self.tree.delete(*self.tree.get_children())
        self.tree.insert('', END, image=self.icono_directorio, text=r.nombre, iid=r.id, open=True) 
        self.generarArbol(r)

    def generarArbol(self,raiz:Directorio):
        for archivo in raiz.archivos:
            self.tree.insert(raiz.id, END, image=self.icono_archivo, text=archivo.nombre, iid=archivo.id, open=False)
        for directorio in raiz.directorios:
            self.tree.insert(raiz.id, END, image=self.icono_directorio, text=directorio.nombre, iid=directorio.id, open=directorio.id in self.abiertos)
            self.generarArbol(directorio)