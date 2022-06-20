def prueba1():
    import Vista
    import FileSystem
    vista = Vista.Vista()
    FileSystem = vista.FileSystem
    FileSystem.inicializar("S")
    FileSystem.crear_archivo("archivo1.txt", "contenido1")
    FileSystem.crear_directorio("escritorio")
    FileSystem.cambiar_directorio("escritorio")
    FileSystem.crear_directorio("juegos")
    FileSystem.crear_archivo("progra1.py","print('hola mundo')")
    FileSystem.cambiar_directorio("juegos")
    FileSystem.crear_archivo("juego1.exe", "contenido2")
    FileSystem.crear_archivo("juego2.exe", "contenido3")
    FileSystem.crear_archivo("juego3.exe", "contenido4")
    FileSystem.modificar_archivo("juego3.exe", "Este es el juego 3")
    FileSystem.copiar("S/archivo1.txt", "S/escritorio","-v")
    FileSystem.copiar("juego1.exe", "Archivos","-vl")
    #FileSystem.borrar_archivo("juego3.exe")
    vista.actualizarArbol()
    vista.mainloop()
def prueba2():
    from DiskManager import DiskManager
    disco = DiskManager('1', 4, 4)
    disco.escribir("as.txt","aaaa")
    disco.escribir("bs.txt","bb")
    assert disco.escribir("cs.txt","cccccccccc") == -1
    disco.eliminar("as.txt")
    disco.escribir("cs.txt","cccccccccc")
    with open("Discos/Disco 1.txt", "r") as f:
        assert f.readline() == 'ccccbb  cccccc  '
def prueba3():
    from DiskManager import DiskManager
    disco = DiskManager('2', 4, 4)
    disco.escribir("a.txt","aaaa")
    disco.escribir("b.txt","bb")
    disco.escribir("a.txt","cccccccccc")
    with open("Discos/Disco 2.txt", "r") as f:
        assert f.readline() == 'ccccbb  cccccc  '
prueba1()