class Elemento:
    id = 1
    def __init__(self):
        self.id = Elemento.id
        Elemento.id += 1

class Archivo(Elemento):
    def __init__(self, nombre, contenido):
        super().__init__()
        self.nombre = nombre
        self.contenido = contenido

class Directorio(Elemento):
    def __init__(self, nombre):
        super().__init__()
        self.nombre = nombre
        self.archivos = []
        self.directorios = []

class FileSystem:
    def __init__(self, cantidad_sectores:int = 10, tamaño_sector:int = 8):
        self.cantidad_sectores = cantidad_sectores
        self.tamaño_sector = tamaño_sector
        self.actual_dir = self.raiz = Directorio("S:")
    def crear_archivo(self, nombre:str, contenido:str):
        archivo = Archivo(nombre, contenido)
        self.actual_dir.archivos.append(archivo)
    def crear_directorio(self, nombre:str):
        directorio = Directorio(nombre)
        self.actual_dir.directorios.append(directorio)
        self.actual_dir = directorio
    def cambiar_directorio(self, nombre:str):
        for directorio in self.actual_dir.directorios:
            if directorio.nombre == nombre:
                self.actual_dir = directorio
                return
        raise Exception("No se encontró el directorio")
