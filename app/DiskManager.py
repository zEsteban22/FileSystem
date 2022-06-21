from math import ceil

class DiskManager:
    def __init__(self, nombre, tamaño_sector, cantidad_sectores):
        self.sectores_por_archivo = {}
        self.nombre = nombre
        self.tamaño_sector = tamaño_sector
        self.cantidad_sectores = cantidad_sectores
        self.nombre = f"Discos/Disco {self.nombre}.txt"
        disco = open(self.nombre, "w")
        disco.write(" "*self.tamaño_sector*self.cantidad_sectores)
        disco.close()
    def no_se_puede_escribir(self, tamaño_archivo, cantidad_sectores_ocupados):
        return self.cantidad_sectores - cantidad_sectores_ocupados < ceil(tamaño_archivo/self.tamaño_sector)

    def escribir(self, archivo, contenido):
        cantidad_sectores = ceil(len(contenido)/self.tamaño_sector)
        with open(self.nombre, "r") as f:
            disco = f.readline()
        
        if archivo not in self.sectores_por_archivo: 
            sectores_ocupados = []
            for sectores in self.sectores_por_archivo.values():
                sectores_ocupados += sectores
            if self.no_se_puede_escribir(len(contenido), len(sectores_ocupados)):
                return -1
            self.sectores_por_archivo[archivo] = []
            for i in range(self.cantidad_sectores * self.tamaño_sector):
                if i not in sectores_ocupados:
                    cantidad_sectores -= 1
                    self.sectores_por_archivo[archivo] += [i]
                    disco = disco[:i*self.tamaño_sector] + contenido[:self.tamaño_sector] + " " * (self.tamaño_sector - len(contenido[:self.tamaño_sector])) + disco[(i + 1 ) * self.tamaño_sector:]
                    contenido = contenido[self.tamaño_sector:]
                    if cantidad_sectores == 0:
                        break
            with open(self.nombre, "w") as f:
                f.write(disco)
            return 0
                
        else:
            self.eliminar(archivo)
            return self.escribir(archivo,contenido)


    def eliminar(self, archivo):
        with open(self.nombre, "r") as f:
            disco = f.readline()
        for sector in self.sectores_por_archivo[archivo]:
            disco = disco[:sector*self.tamaño_sector] + " "*self.tamaño_sector + disco[(sector + 1) * self.tamaño_sector:]
        del self.sectores_por_archivo[archivo]
        with open(self.nombre, "w") as f:
            f.write(disco)
        return 0
      