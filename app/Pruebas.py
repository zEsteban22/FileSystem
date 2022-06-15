def prueba1():
    import Vista
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
    FileSystem.crear_archivo("juego3.exe", "contenido4")

    FileSystem.buscar_archivo("jue")

    vista.actualizarArbol()
    vista.mainloop()
prueba1()