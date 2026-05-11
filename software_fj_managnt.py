import logging
from abc import ABC, abstractmethod

# 1. CONFIGURACIÓN DE LOGS (Registro de eventos y errores) [3]
logging.basicConfig(
    filename='system.log', 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# EXCEPCIONES PERSONALIZADAS [4, 5]
class SoftwareFJError(Exception):
    """Clase base para excepciones del sistema."""
    pass

class InvalidDataError(SoftwareFJError):
    """Se lanza para IDs no numéricos o duraciones <= 0."""
    pass

class ServiceUnavailableError(SoftwareFJError):
    """Se lanza cuando un servicio no tiene disponibilidad."""
    pass

# 2. CLASE ABSTRACTA EntidadBase (Corrección 2: Uso estricto de ABC) [6, 7]
class EntidadBase(ABC):
    @abstractmethod
    def obtener_detalles(self):
        """Contrato obligatorio para clases derivadas."""
        pass

class Cliente(EntidadBase):
    def __init__(self, id_cliente, nombre, email):
        # (Corrección 4: Se asigna el VALOR retornado, no el método) [2, 7]
        self._id_cliente = self.validar_id(id_cliente)
        self.nombre = nombre
        self.email = email

    def validar_id(self, id_valor):
        if not str(id_valor).isdigit():
            raise InvalidDataError(f"ID inválido: {id_valor}. Debe ser numérico.")
        return id_valor

    def obtener_detalles(self):
        # (Corrección 4: Se imprime el atributo ya validado) [8]
        return f"Cliente[ID: {self._id_cliente}, Nombre: {self.nombre}, Email: {self.email}]"

# JERARQUÍA DE SERVICIOS (Herencia y Polimorfismo) [6, 8]
class ServicioBase(ABC):
    def __init__(self, nombre, costo_base):
        self.nombre = nombre
        self.costo_base = costo_base

    @abstractmethod
    def calcular_costo(self, duracion):
        pass

    @abstractmethod
    def consultar_disponibilidad(self):
        pass

class ReservaSalas(ServicioBase):
    def calcular_costo(self, duracion):
        return (self.costo_base * duracion) * 1.19  # Polimorfismo con impuesto

    def consultar_disponibilidad(self):
        return True 

class AlquilerEquipos(ServicioBase):
    def calcular_costo(self, duracion):
        return (self.costo_base * duracion) - 10 # Polimorfismo con descuento

    def consultar_disponibilidad(self):
        return False # Simulación de error de disponibilidad

class AsesoriaEspecializada(ServicioBase):
    def calcular_costo(self, duracion):
        return self.costo_base * duracion

    def consultar_disponibilidad(self):
        return True

# GESTIÓN DE RESERVAS
class reserva:
    def __init__(self, cliente, servicio, duracion):
        # (Corrección 5: Validar que la duración sea mayor a cero) [4]
        if duracion <= 0:
            raise InvalidDataError(f"Duración inválida: {duracion}. Debe ser mayor a 0.")
        
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "PENDING"

    def procesar(self):
        try:
            logging.info(f"Iniciando proceso para {self.cliente.obtener_detalles()}")
            if not self.servicio.consultar_disponibilidad():
                raise ServiceUnavailableError(f"Servicio '{self.servicio.nombre}' no disponible.")
            
            total = self.servicio.calcular_costo(self.duracion)
            self.estado = "CONFIRMED"
            print(f"RES_SUCCESS: Precio total ${total:.2f}")

        except ServiceUnavailableError as e:
            # (Encadenamiento de excepciones) [4, 9]
            logging.error(f"Fallo de reserva: {e}")
            self.estado = "REJECTED"
            raise SoftwareFJError("Proceso detenido por falta de disponibilidad.") from e
        
        except Exception as e:
            logging.critical(f"Error inesperado del sistema: {e}")
            self.estado = "SYSTEM_ERROR"
        
        else:
            logging.info("Transacción completada satisfactoriamente.")
        
        finally:
            print(f"Estado final: {self.estado}")

    # (Corrección 3: Agregar método cancelar) [6]
    def cancelar(self):
        self.estado = "CANCELLED"
        logging.info(f"Reserva de {self.cliente.nombre} ha sido cancelada.")
        print("La reserva ha sido cancelada exitosamente.")

# (Corrección 1: Unificación de la simulación de 10 operaciones) [10, 11]
def ejecutar_simulacion():
    print("--- SIMULACIÓN SISTEMA SOFTWARE FJ (2026) ---")
    s1 = ReservaSalas("Auditorio A", 100)
    s2 = AlquilerEquipos("Kit de Laptops", 50)
    s3 = AsesoriaEspecializada("Arquitectura Cloud", 200)

    operaciones = [
        ("1001", "Ana Garcia", "ana@fj.com", s1, 5),      # 1. Válida
        ("1002", "Luis Perez", "luis@fj.com", s3, 0),     # 2. INVÁLIDA (Duración 0)
        ("ABC", "Error User", "err@fj.com", s1, 3),       # 3. INVÁLIDA (ID letras)
        ("1003", "Marta Ruiz", "marta@fj.com", s2, 4),    # 4. FALLIDA (Disponibilidad)
        ("1004", "Jose Gil", "jose@fj.com", s1, 2),       # 5. Válida
        ("1005", "Rosa Sol", "rosa@fj.com", s3, 8),       # 6. Válida
        ("9999", "Tester", "test@fj.com", s2, 1),         # 7. FALLIDA (Disponibilidad)
        ("1006", "Ian Cook", "ian@fj.com", s1, 2),        # 8. Válida
        ("INVALID", "No Name", "no@fj.com", s3, 1),       # 9. INVÁLIDA (ID letras)
        ("1007", "Eva Luna", "eva@fj.com", s3, 10),      # 10. Válida
    ]

    for i, op in enumerate(operaciones, 1):
        print(f"\n>>> Ejecutando Operación {i}:")
        try:
            cliente_obj = Cliente(op, op[12], op[13])
            reserva_obj = reserva(cliente_obj, op[14], op[15])
            reserva_obj.procesar()
        except SoftwareFJError as e:
            print(f"Error de lógica capturado: {e}")
        except Exception as e:
            print(f"Error crítico evitado: {e}")

if __name__ == "__main__":
    ejecutar_simulacion()