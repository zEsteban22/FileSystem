from tkinter import *

class VistaContenido(Tk):
    def __init__(self,nombre:str,cont:str):
        super().__init__()
        self.title(nombre)
        self.geometry("350x300")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        label = Label(self,text=cont)
        label.grid(row=0, column=0, sticky='nw')