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
        self.abierto = False

class FileSystem:
    def __init__(self):
        pass
    def inicializar(self, nombre, cantidad_sectores:int = 10, tamaño_sector:int = 8):
        self.cantidad_sectores = cantidad_sectores
        self.tamaño_sector = tamaño_sector
        self.actual_dir = self.raiz = Directorio(nombre)
        return "Disco creado con éxito."
    def crear_archivo(self, nombre:str, contenido:str):
        archivo = Archivo(nombre, contenido)
        self.actual_dir.archivos.append(archivo)
    def crear_directorio(self, nombre:str):
        directorio = Directorio(nombre)
        self.actual_dir.directorios.append(directorio)
    def cambiar_directorio(self, nombre:str):
        for directorio in self.actual_dir.directorios:
            if directorio.nombre == nombre:
                self.actual_dir = directorio
                return
        raise Exception("No se encontró el directorio")
    def abrir_archivo(self, nombre:str):
        for archivo in self.actual_dir.archivos:
            if archivo.nombre == nombre:
                return archivo.contenido
        return "No se encontró el archivo"
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
        else:
            return "Comando no reconocido."

