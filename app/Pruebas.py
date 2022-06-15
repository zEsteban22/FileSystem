from msilib.schema import File
from tkinter import Button, StringVar
import tkinter as tk
from numpy import true_divide
from pyparsing import col
import Vista
from threading import Thread

def enviarComando(comando):
    print(comando)

def prueba1():
    import FileSystem
    vista = Vista.Vista()
    FileSystem = vista.FileSystem
    FileSystem.inicializar("S:")
    FileSystem.crear_archivo("archivo1.txt", "contenido1")
    FileSystem.crear_directorio("escritorio")
    FileSystem.cambiar_directorio("escritorio")
    FileSystem.crear_directorio("juegos")
    FileSystem.crear_archivo("progra1.py","print('hola mundo')")
    FileSystem.cambiar_directorio("juegos")
    FileSystem.crear_archivo("juego1.exe", "contenido2")
    FileSystem.crear_archivo("juego2.exe", "contenido3")
    b = Button(vista, text='Actualizar árbol', command=lambda:vista.actualizarArbol(FileSystem.raiz))
    b.grid(row=1, column=0)

    label = tk.Label(vista,text="Comando")
    label.grid(row =2 ,column=0)

    comando=StringVar()
    entry = tk.Entry(vista, width=25, textvariable=comando)
    entry.grid(row=3,column=0)
    entry.focus()

    b1 = Button(vista, text='Listo',width=15, font = ('Arial bold',10), command=enviarComando(comando))
    b1.grid(row=4,column=0)

    FileSystem.crear_archivo("juego3.exe", "contenido4")
    vista.actualizarArbol()
    vista.mainloop()
    

prueba1()
