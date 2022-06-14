from tkinter import Button


def prueba1():
    import Vista
    import FileSystem
    from threading import Thread
    vista = Vista.Vista()
    directorio = FileSystem.Directorio("S:")
    directorio.directorios.append(FileSystem.Directorio("documentos"))
    directorio.directorios.append(FileSystem.Directorio("imágenes"))
    directorio.directorios.append(FileSystem.Directorio("videos"))
    escritorio = FileSystem.Directorio("escritorio")
    escritorio.directorios.append(FileSystem.Directorio("juegos"))
    escritorio.archivos.append(FileSystem.Archivo("progra1.py","print('hola mundo')"))
    directorio.directorios.append(escritorio)
    directorio.directorios.append(FileSystem.Directorio("programas"))
    b = Button(vista, text='Actualizar árbol', command=lambda:vista.actualizarArbol(directorio))
    b.grid(row=1, column=0)
    vista.mainloop()
prueba1()