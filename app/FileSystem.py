from copy import copy
from ctypes import sizeof
from hashlib import new
from tkinter import StringVar
from numpy import size
from datetime import datetime
from abc import ABC, abstractmethod
import ntpath
from tkinter import messagebox

#from urllib3 import Retry

from DiskManager import DiskManager

class Elemento(ABC):
    id = 0
    def __init__(self,fecha_creacion = datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                                    fecha_modificacion = datetime.now().strftime("%d/%m/%Y %H:%M:%S")):
        Elemento.id += 1
        self.id = Elemento.id
        self.fecha_creacion = fecha_creacion
        self.fecha_modificacion = fecha_modificacion
    @abstractmethod
    def propiedades(self):
        pass

class Archivo(Elemento):
    def __init__(self, nombre, contenido):
        super().__init__()
        self.nombre = nombre
        self.contenido = contenido
    def propiedades(self):
        return "Archivo: " + self.nombre + "\nFecha de creación: " + self.fecha_creacion+"\nUltima modificación: "+self.fecha_modificacion

class Directorio(Elemento):
    def __init__(self, nombre:str, papá=None):
        super().__init__()
        self.nombre = nombre
        self.archivos = []
        self.directorios = []
        self.papá = papá
    def propiedades(self):
        return "Directorio: " + self.nombre + "\nFecha de creación: " + self.fecha_creacion+"\nUltima modificación: "+self.fecha_modificacion
    def children(self):
        return self.archivos + self.directorios

class FileSystem:
    def __init__(self):
        pass

    def inicializar(self, nombre, cantidad_sectores:int = 10, tamaño_sector:int = 8):
        self.diskManager = DiskManager(nombre, tamaño_sector, cantidad_sectores)
        self.cantidad_sectores = cantidad_sectores
        self.tamaño_sector = tamaño_sector
        self.actual_dir = self.raiz = Directorio(nombre)
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

        
    def crear_archivo(self, nombre:str, contenido:str):
        idViejo = 0
        for arch in self.actual_dir.archivos:
            if nombre == arch.nombre:
                res = messagebox.askquestion("askquestion", "Ya existe un archivo con ese nombre, desea reescribirlo?")
                if res == "no":
                    return "Operación Cancelada"
                elif res == "yes":
                    for archivo in self.actual_dir.archivos:
                        if archivo.nombre==nombre:
                            self.actual_dir.archivos.remove(archivo)
                            idViejo = archivo.id
        archivo = Archivo(nombre, contenido)
        if idViejo != 0:
            archivo.id = idViejo
        if self.diskManager.escribir(archivo.id,contenido) == 0:
            self.actual_dir.archivos.append(archivo)
            return "Archivo creado correctamente"
        else:
            return "No se pudo crear el archivo debido a que no hay espacio en el disco."

    def crear_directorio(self, nombre:str):
        for dir in self.actual_dir.directorios:
            if nombre == dir.nombre:
                res = messagebox.askquestion("askquestion", "Ya existe un directorio con ese nombre, desea reescribirlo?")
                if res == "no":
                    return "Operación Cancelada"
                elif res == "yes":
                    for dir in self.actual_dir.directorios:
                        if dir.nombre==nombre:
                            self.actual_dir.directorios.remove(dir)
        directorio = Directorio(nombre, self.actual_dir)
        self.actual_dir.directorios.append(directorio)
        return "Directorio creado correctamente"

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

    def propiedades(self, id):
        archivo = self.get_archivo_id(id)
        if archivo is None:
            return "No se encontró el archivo"
        return archivo.propiedades()

    def ver_contenido(self, id):
        archivo = self.get_archivo_id(id)
        if archivo is None:
            return "No se encontró el archivo"
        return archivo.contenido
        
    def abrir_archivo(self, nombre:str):
        for archivo in self.actual_dir.archivos:
            if archivo.nombre == nombre:
                return archivo.contenido
        return "No se encontró el archivo"

    def borrar_archivo(self, nombre:str):
        for archivo in self.actual_dir.archivos:
            if archivo.nombre==nombre:
                self.actual_dir.archivos.remove(archivo)
                self.diskManager.eliminar(archivo.id)
                return("Archivo eliminado correctamente")
        return("No se encontró el Archivo")

    def borrar_directorio(self, nombre:str):
        def borrar_directorio_recursivo(directorio):
            for archivo in directorio.archivos:
                self.diskManager.eliminar(archivo.id)
            for directorio in directorio.directorios:
                borrar_directorio_recursivo(directorio)

        for dir in self.actual_dir.directorios:
            if dir.nombre==nombre:
                self.actual_dir.directorios.remove(dir)
                borrar_directorio_recursivo(dir)
                return("Directorio eliminado correctamente")
        return("No se encontró el directorio")

    def borrar_seleccionado(self,id):
        def buscar(directorio):
            for arch in directorio.archivos:
                if arch.id == id:
                    directorio.archivos.remove(arch)
                    self.diskManager.eliminar(id)
                    return ("Archivo elimiando")
            for dir in directorio.directorios:
                if dir.id == id:
                    directorio.directorios.remove(dir)
                    self.borrar_directorio(dir.nombre)
                    return ("Directorio eliminado")
            for dir in directorio.directorios:
                buscar(dir)
        buscar(self.raiz)

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
        
    def modificar_archivo(self,nombre:str,contenido:str):
        for arch in self.actual_dir.archivos:
            if arch.nombre == nombre:
                if self.diskManager.escribir(arch.id,contenido) == 0:
                    arch.contenido=contenido
                    arch.fecha_modificacion=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    return "Archivo modificado correctamente"
                else:
                    self.diskManager.escribir(arch.id,arch.contenido)
                    return "No se pudo modificar el archivo debido a que no hay espacio suficiente en el disco."
                    
        return "No se pudo encontrar el archivo"

    def buscar_ruta(self, rutas):
        rutas=rutas.split('/')
        path = self.raiz
        if rutas[0] == self.raiz.nombre:
            if len(rutas)==1:
                return path
        else:
            return "La ruta ingresada no existe"
        def busca(rutas,path):
            for rut in rutas[1:]:
                finded=False
                for dir in path.directorios:
                    if dir.nombre == rut:
                        path=dir
                        finded=True
                if finded==False:
                    return "La ruta ingresada no existe"
            return path
        return busca(rutas,path)

    def copiar(self, elemento:str, ruta:str, modo:str):
        if modo == "-v":
            try:
                path_origen=ntpath.dirname(elemento)
                if path_origen[-1]=="/":
                    path_origen=path_origen[:-1]
                path_origen = self.buscar_ruta(path_origen)
                if type(path_origen) != Directorio:
                    path_origen = self.actual_dir
            except:
                path_origen=self.actual_dir
            elemento=ntpath.basename(elemento)
            path = self.buscar_ruta(ruta)
            if type(path) == Directorio:
                for arch in path_origen.archivos:
                    if arch.nombre == elemento:
                        archivo=copy(arch)
                        if self.diskManager.escribir(Elemento.id + 1,archivo.contenido) == 0:
                            Elemento.id += 1
                            archivo.id = Elemento.id
                            path.archivos.append(archivo)
                            return "Archivo copiado correctamente"
                        else:
                            return "No se pudo copiar el archivo debido a que no hay espacio suficiente en el disco."
                for dir in path_origen.directorios:
                    if dir.nombre == elemento:
                        directorio=copy(dir)
                        Elemento.id += 1
                        directorio.id=Elemento.id     
                        path.directorios.append(directorio)
                        return "Copiado Correctamente"
                return "No se encontró el Archivo"
            else:
                return "No se encontró el directorio de destino"
        elif modo == "-vl":
            try:
                path_origen=ntpath.dirname(elemento)
                if path_origen[-1]=="/":
                    path_origen=path_origen[:-1]
                path_origen = self.buscar_ruta(path_origen)
                if type(path_origen) != Directorio:
                    path_origen = self.actual_dir
            except:
                path_origen=self.actual_dir
            elemento=ntpath.basename(elemento)
            for arch in path_origen.archivos:
                if arch.nombre == elemento:
                    try:
                        print(ruta+"/"+elemento)
                        with open(ruta+"/"+elemento, 'w') as f:
                            f.write(arch.contenido)
                        return "Elemento copiado correctamente"
                    except:
                        return "Error al copiar"
            return "Error al copiar"
            
        elif modo == "-lv":
            nombre=elemento.split("/")[-1]
            print("Nombre: ",nombre)
            texto=""
            print(elemento)
            try:
                with open(elemento, 'r') as f:
                    texto=f.read()
                    print(texto)
            except:
                return "No se encontró el archivo local"
            
            path = self.buscar_ruta(ruta)
            if type(path) == Directorio:
                for arch in path.archivos:
                    if nombre == arch.nombre:
                        return "Ya existe un archivo con ese nombre"
                archivo = Archivo(nombre, texto)
                if self.diskManager.escribir(archivo.id,texto) == 0:
                    path.archivos.append(archivo)
                    return "Archivo copiado correctamente"
                else:
                    return "No se pudo copiar el archivo debido a que no hay espacio suficiente en el disco."

        else:
            return "Debe seleccionar un modo de copia válido."

    def mover(self, elemento:str, ruta:str):
        try:
            path_origen = ntpath.dirname(elemento)
            nuevo_nombre = ntpath.basename(ruta)
            ruta = ntpath.dirname(ruta)
            if path_origen[-1]=="/":
                path_origen=path_origen[:-1]
            path_origen = self.buscar_ruta(path_origen)
            if type(path_origen) != Directorio:
                path_origen = self.actual_dir
        except:
            path_origen=self.actual_dir
        elemento=ntpath.basename(elemento)
        path = self.buscar_ruta(ruta)
        if type(path) == Directorio:
            for arch in path_origen.archivos:
                if arch.nombre == elemento:
                    archivo=copy(arch)
                    Elemento.id += 1
                    archivo.id = Elemento.id
                    if nuevo_nombre != "":
                        archivo.nombre=nuevo_nombre
                    path_origen.archivos.remove(arch)
                    path.archivos.append(archivo)
                    return "Movido Correctamente"
            for dir in path_origen.directorios:
                if dir.nombre == elemento:
                    directorio=copy(dir)
                    if nuevo_nombre != "":
                        directorio.nombre=nuevo_nombre
                    path_origen.directorios.remove(dir)
                    path.directorios.append(directorio)
                    return "Movido Correctamente"
            return "No se encontró el Archivo"
        else:
            return "No se encontró el directorio de destino"

    def procesar_comando(self, comando:str):
        comando = comando.split(" ")
        if len(comando) == 0:
            return "Ingrese un comando."
        if comando[0] == "inicializar":
            if len(comando) != 4:
                return "El comando inicializar debe tener 3 argumentos: nombre, tamaño de los sectores y cantidad de sectores."
            elif nombre_no_valido(comando[1]):
                return "El nombre del disco no es válido"
            try:
                comando[2] = int(comando[2])
                comando[3] = int(comando[3])
                return self.inicializar(comando[1], comando[2], comando[3])
            except:
                return "El tamaño de los sectores y la cantidad de sectores deben ser enteros."
        elif comando[0] == "cd":
            if len(comando) != 2:
                return "El comando cd debe tener 1 argumento: ruta."
            if nombre_no_valido(comando[1]):
                return "El nombre del directorio no es válido"
            return self.cambiar_directorio(comando[1])
        elif comando[0] == "mkdir":
            if len(comando) != 2:
                return "El comando mkdir debe tener 1 argumento: nombre."
            if nombre_no_valido(comando[1]):
                return "El nombre del directorio no es válido"
            return self.crear_directorio(comando[1])
        elif comando[0] == "mkfile":
            if len(comando) <= 2:
                return "El comando mkfile debe tener dos argumentos: nombre y contenido."
            text=""
            for i in range(len(comando)):
                if i >=2:
                    text = text + " " +comando[i]
            if nombre_no_valido(comando[1]):
                return "El nombre del archivo no es válido"
            return self.crear_archivo(comando[1],text)
        elif comando[0] == "cat":
            if len(comando) != 2:
                return "El comando cat debe tener 1 argumento: ruta."
            if nombre_no_valido(comando[1]):
                return "El nombre del archivo no es válido"
            return self.abrir_archivo(comando[1])
        elif comando[0] == "find":
            if len(comando) != 2:
                return "El comando find debe tener 1 argumento: nombre."
            if nombre_no_valido(comando[1]):
                return "El nombre del archivo no es válido"
            return self.buscar_archivo(comando[1])
        elif comando[0] == "delDir":
            if len(comando) != 2:
                return "El comando delDir debe tener 1 argumento: nombre."
            if nombre_no_valido(comando[1]):
                return "El nombre del directorio no es válido"
            return self.borrar_directorio(comando[1])
        elif comando[0] == "delFile":
            if len(comando) != 2:
                return "El comando delFile debe tener 1 argumento: nombre."
            if nombre_no_valido(comando[1]):
                return "El nombre del archivo no es válido"
            return self.borrar_archivo(comando[1])
        elif comando[0] == "mod":
            if len(comando) != 3:
                return "El comando mod debe tener 2 argumentos: nombre y contenido."
            if nombre_no_valido(comando[1]):
                return "El nombre del archivo no es válido"
            text=""
            for i in range(len(comando)):
                if i >=2:
                    text = text + " " +comando[i]
            return self.modificar_archivo(comando[1],text)
        elif comando[0] == "copy":
            if len(comando) != 4:
                return "El comando copy debe tener 3 argumentos: modo, origen y destino.\nEl modo -lv es para copiar de ruta local a ruta virtual, el modo -vl es para copar de ruta virtual a ruta local y el modo -v es para copiar de ruta virtual a ruta virtual."
            return self.copiar(comando[2],comando[3],comando[1])
        elif comando[0] == "mov":
            if len(comando) != 3:
                return "El comando mov debe tener 2 argumentos: origen y destino."
            return self.mover(comando[1],comando[2])
        else:
            return "Comando no reconocido."
def nombre_no_valido(nombre_directorio):
    for i in nombre_directorio:
        if i not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.$":
            return True
    return False