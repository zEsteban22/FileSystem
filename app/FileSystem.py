from ctypes import sizeof
from typing_extensions import Self
from numpy import size
from datetime import datetime


class Elemento:
    id = 0
    def __init__(self):
        Elemento.id += 1
        self.id = Elemento.id

class Archivo(Elemento):
    def __init__(self, nombre, contenido,fecha_creacion = datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                                    fecha_modificacion = datetime.now().strftime("%d/%m/%Y %H:%M:%S")):
        super().__init__()
        self.nombre = nombre
        self.contenido = contenido
        self.fecha_creacion = fecha_creacion
        self.fecha_modificacion = fecha_modificacion

class Directorio(Elemento):
    def __init__(self, nombre:str, papá=None, abierto=False):
        super().__init__()
        self.nombre = nombre
        self.archivos = []
        self.directorios = []
        self.abierto = abierto
        self.papá = papá

class FileSystem:
    def __init__(self):
        pass

    def inicializar(self, nombre, cantidad_sectores:int = 10, tamaño_sector:int = 8):
        self.cantidad_sectores = cantidad_sectores
        self.tamaño_sector = tamaño_sector
        self.actual_dir = self.raiz = Directorio(nombre, abierto=True)
        return "Disco creado con éxito."

    def tocar(self, id, r=None):
        if r is None:
            r = self.raiz
        for directorio in r.directorios:
            if directorio.id == id:
                directorio.abierto = directorio.abierto == False
                return directorio.abierto
            self.tocar(directorio, id)
        return False
        
    def crear_archivo(self, nombre:str, contenido:str):
        archivo = Archivo(nombre, contenido)
        self.actual_dir.archivos.append(archivo)

    def crear_directorio(self, nombre:str):
        directorio = Directorio(nombre, self.actual_dir)
        self.actual_dir.directorios.append(directorio)

    def cambiar_directorio(self, nombre:str):
        if nombre == '..':
            if self.actual_dir.papá is None:
                return "No se puede cambiar al directorio padre"
            self.actual_dir = self.actual_dir.papá
        for directorio in self.actual_dir.directorios:
            if directorio.nombre == nombre:
                self.actual_dir = directorio
                return "Cambiado al directorio " + nombre
        return "No se encontró el directorio"

    def abrir_archivo(self, nombre:str):
        for archivo in self.actual_dir.archivos:
            if archivo.nombre == nombre:
                return archivo.contenido
        return "No se encontró el archivo"

    def borrar_archivo(self, nombre:str):
        for archivo in self.actual_dir.archivos:
            if archivo.nombre==nombre:
                self.actual_dir.archivos.remove(archivo)

    #Las siguientes tres funciones son de la funcionalidad de buscar archivos
    def buscar_aqui(self,nombre:str, dir:Directorio,ruta:str):
        for archivo in dir.archivos:
            if nombre in archivo.nombre:
                print("Se encontró: " + ruta+ archivo.nombre)

    def hay_directorios(self,nombre:str,directorio:Directorio,ruta:str):
        self.buscar_aqui(nombre,directorio,ruta)
        if size(directorio.directorios)>=1:
            for dir in directorio.directorios:
                print(dir.nombre)
                return self.hay_directorios(nombre,dir,ruta+dir.nombre+"/")

    def buscar_archivo(self, nombre:str):
        ruta=self.raiz.nombre+"/"
        self.hay_directorios(nombre,self.raiz,ruta)
    #

    def ver_propiedades(self, filename:str):
        for archivo in self.actual_dir.archivos:
            if archivo.nombre==filename:
                print("Archivo: " + archivo.nombre + "\nFecha de creacion: " + archivo.fecha_creacion+"\nUltima modificacion: "+archivo.fecha_modificacion)

    

    ###############################################################################

    def procesar_comando(self, comando:str):
        comando = comando.split(" ")
        if comando[0] == "inicializar":
            return self.inicializar(comando[1], int(comando[2]), int(comando[3])) 
        elif comando[0] == "cd":
            self.cambiar_directorio(comando[1])
            return "Cambiado al directorio " + comando[1]
        elif comando[0] == "mkdir":
            self.crear_directorio(comando[1])
            return "Creado el directorio " + comando[1]
        elif comando[0] == "mkfile":
            self.crear_archivo(comando[1], comando[2])
            return "Creado el archivo " + comando[1]
        elif comando[0] == "cat":
            return self.abrir_archivo(comando[1])
        elif comando[0] == "find":
            return self.buscar_archivo(comando[1])
        else:
            return "Comando no reconocido."

