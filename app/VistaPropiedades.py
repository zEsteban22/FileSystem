from tkinter import *

class VistaPropiedades(Tk):
    def __init__(self,props:str):
        super().__init__()
        self.title("Propiedades del Archivo")
        self.geometry("350x300")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        label = Label(self,text=props)
        label.grid(row=0, column=0, sticky='nsew')