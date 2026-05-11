from abc import ABC, abstractmethod

class ServicioBase(ABC):
    def __init__(self, nombre, costo_base):
        self.nombre = nombre
        self.costo_base = costo_base

    @abstractmethod
    def consultar_disponibilidad(self): pass

    @abstractmethod
    def calcular_costo(self, duracion): pass

class ReservaSalas(ServicioBase):
    def calcular_costo(self, d): return (self.costo_base * d) * 1.19
    def consultar_disponibilidad(self): return True

class AlquilerEquipos(ServicioBase):
    def calcular_costo(self, d): return (self.costo_base * d) - 10
    def consultar_disponibilidad(self): return False # Simulación de error

class AsesoriaEspecializada(ServicioBase):
    def calcular_costo(self, d): return self.costo_base * d
    def consultar_disponibilidad(self): return True