class Elemento:
    id = 0
    def __init__(self):
        Elemento.id += 1
        self.id = Elemento.id

class Archivo(Elemento):
    def __init__(self, nombre, contenido):
        super().__init__()
        self.nombre = nombre
        self.contenido = contenido

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
                return True
            if self.tocar(directorio, id):
                return True
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

    def mod_archivo(self, nombre:str, contenido:str):
        archivo = self.actual_dir.archivos[nombre]
        archivo.contenido = contenido

    def ver_archivo(self, nombre:str):
        archivo = self.actual_dir.archivos[nombre]
        print(archivo.nombre+ "\n"+ archivo.contenido)

