from abc import ABC, abstractmethod

class ServicioBase(ABC):
    """Clase abstracta para servicios[cite: 97]."""
    def __init__(self, nombre, costo_base, id_servicio):
        self.nombre = nombre
        self.costo_base = costo_base
        self.id_servicio = id_servicio

    @abstractmethod
    def consultar_disponibilidad(self):
        """Método abstracto para verificar disponibilidad."""
        pass

    @abstractmethod
    def calcular_costo(self, *args, **kwargs):
        """Método polimórfico para calcular costos."""
        pass

class ReservaSalas(ServicioBase):
    def calcular_costo(self, duracion, impuesto=0.19):
        # Sobrecarga mediante parámetro opcional 'impuesto' 
        base = self.costo_base * duracion
        return base + (base * impuesto)

    def consultar_disponibilidad(self):
        return True # Las salas siempre están disponibles en esta simulación

class AlquilerEquipos(ServicioBase):
    def calcular_costo(self, duracion, descuento=0):
        # Sobrecarga mediante parámetro opcional 'descuento' 
        return (self.costo_base * duracion) - descuento

    def consultar_disponibilidad(self):
        # Simulación: No hay equipos disponibles para probar el manejo de errores [cite: 93]
        return False

class AsesoriaEspecializada(ServicioBase):
    def calcular_costo(self, duracion):
        return self.costo_base * duracion

    def consultar_disponibilidad(self):
        return True