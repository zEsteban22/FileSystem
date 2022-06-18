from ctypes import sizeof
from hashlib import new
from tkinter import StringVar
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
    def propiedades(self):
        return "Archivo: " + self.nombre + "\nFecha de creación: " + self.fecha_creacion+"\nUltima modificación: "+self.fecha_modificacion

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

    def get_actual_dir(self):
        ruta=self.actual_dir.nombre
        def actual_dir_recursivo(ruta,dir:Directorio):
            if dir.papá != None:
                padre = dir.papá
                ruta = padre.nombre+"/"+ruta
                return actual_dir_recursivo(ruta,padre)
            else:
                return ruta
        return actual_dir_recursivo(ruta,self.actual_dir)

    def tocar(self, id, r = None) -> bool:
        if r is None:
            r = self.raiz
        for directorio in r.directorios:
            if directorio.id == id:
                directorio.abierto = directorio.abierto == False
                return directorio.abierto
            abierto = self.tocar(id, directorio)
            if abierto is not None:
                return abierto    
        return None
        
    def crear_archivo(self, nombre:str, contenido:str):
        archivo = Archivo(nombre, contenido)
        self.actual_dir.archivos.append(archivo)

    def crear_directorio(self, nombre:str):
        directorio = Directorio(nombre, self.actual_dir)
        self.actual_dir.directorios.append(directorio)

    def cambiar_directorio(self, nombre:str):
        if nombre == '..':
            if self.actual_dir.papá is None:
                return "No existe directorio padre"
            self.actual_dir = self.actual_dir.papá
            return ""
        else:
            for directorio in self.actual_dir.directorios:
                if directorio.nombre == nombre:
                    self.actual_dir = directorio
                    return ""
            return "No se encontró el directorio"

    def propiedades(self, id):
        for archivo in self.raiz.archivos:
            if archivo.id == id:
                return archivo.propiedades()

        def propiedades_recursivo(r = self.raiz):
            for directorio in r.directorios:
                #if directorio.id == id:
                #   return directorio.propiedades() ##No implementado
                for archivo in directorio.archivos:
                    if archivo.id == id:
                        return archivo.propiedades()
                propiedades = propiedades_recursivo(directorio)
                if propiedades != None:
                    return propiedades
            return None

        return propiedades_recursivo()

    def contenido(self, id):
        for archivo in self.raiz.archivos:
            if archivo.id == id:
                return archivo.contenido
        
        def contenido_recursivo(r = self.raiz):
            for directorio in r.directorios:
                for archivo in directorio.archivos:
                    if archivo.id == id:
                        return archivo.contenido
                contenido = contenido_recursivo(directorio)
                if contenido != None:
                    return contenido
            return None
        
        return contenido_recursivo()

    def get_archivo_id(self,id):
        for archivo in self.raiz.archivos:
            if archivo.id == id:
                return archivo
        
        def get_archivo_id_recursivo(r = self.raiz):
            for directorio in r.directorios:
                for archivo in directorio.archivos:
                    if archivo.id == id:
                        return archivo
                archivo = get_archivo_id_recursivo(directorio)
                if archivo != None:
                    return archivo
            return None
        
        return get_archivo_id_recursivo()

    def abrir_archivo(self, nombre:str):
        for archivo in self.actual_dir.archivos:
            if archivo.nombre == nombre:
                return archivo.contenido
        return "No se encontró el archivo"

    def borrar_archivo(self, nombre:str):
        for archivo in self.actual_dir.archivos:
            if archivo.nombre==nombre:
                self.actual_dir.archivos.remove(archivo)

    #Las siguientes 3 funciones son de la funcionalidad de buscar archivos
    def arch(self,nombre:str, archivo:Archivo,ruta:str):
        if nombre in archivo.nombre:
            return ruta+ archivo.nombre+"\n"
        else:
            return ""

    def buscar_aqui(self,nombre:str, directorio:Directorio,ruta:str):
        rutas=""
        for dir in directorio.directorios:
            rutas = rutas + self.buscar_aqui(nombre,dir,ruta+dir.nombre+"/")
        for archivo in directorio.archivos:
            rutas = rutas + self.arch(nombre,archivo,ruta)
        return rutas

    def buscar_archivo(self, nombre:str):
        ruta=self.raiz.nombre+"/"
        rutas = self.buscar_aqui(nombre,self.raiz,ruta)
        if rutas == "":
            return "No se encontraron coincidencias"
        else:
            return rutas
    #
    #
    #def ver_propiedades(self, filename:str):
    #    for archivo in self.actual_dir.archivos:
    #        if archivo.nombre==filename:
    #            text = 
    #            VistaPropiedades(text)

    #def ver_contenido(self, filename:str):
    #    for archivo in self.actual_dir.archivos:
    #        if archivo.nombre==filename:
    #            VistaContenido(archivo.nombre,archivo.contenido)

    

    ###############################################################################

    def procesar_comando(self, comando:str):
        comando = comando.split(" ")
        if comando[0] == "inicializar":
            return self.inicializar(comando[1], int(comando[2]), int(comando[3])) 
        elif comando[0] == "cd":
            return self.cambiar_directorio(comando[1])
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

