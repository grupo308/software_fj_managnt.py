import logging
from abc import ABC, abstractmethod

# Configuración del archivo de logs
logging.basicConfig(filename='system.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# EXCEPCIONES PERSONALIZADAS[4]
class SoftwareFJError(Exception):
    """Clase base para excepciones del sistema."""
    pass

class InvalidDataError(SoftwareFJError):
    """Se lanza cuando los datos de entrada son inválidos."""
    pass

class ServiceUnavailableError(SoftwareFJError):
    """Se lanza cuando un servicio no puede procesarse."""
    pass
# CLASES ASTRACTAS Y ENTIDADES[7]
class EntidadBase(ABC):
    @abstractmethod
    def obtener_detalles(self):
        pass
class Cliente(EntidadBase):
    def __init__(self, id_cliente, nombre, email):
        #Encapsulacion con validaciones estrictas [7,8]   self.id = id_cliente = self.validar_id(id_cliente)
        self.nombre = nombre
        self.email = email

    def validar_id(self, id_valor):
        if not str(id_valor).isdigit():
            # Uso de excepciones personalizadas para validación [4, 6]
            raise InvalidDataError(f"ID inválido: {id_valor}. Must be numeric.")
        return id_valor
    def obtener_detalles(self):
        return f"Cliente[ID: {self.validar_id}, Name: {self.nombre}, Email: {self.email}]"
# JERARQUIA DE SERVICIOS (Herencia y Polimorfismo) [7, 9]
class ServicioBase(ABC):
    def __init__(self, nombre, costo_base):
        self.nombre = nombre
        self.costo_base = costo_base
    @abstractmethod
    def consultar_disponibilidad(self):
        pass
class ReservaSalas(ServicioBase):
    def calcular_costo(self,duracion,impuesto=0.19):
        # Variante con impuesto opcional (sobrecarga)[5]
        base = self.costo_base * duracion
        return base + (base * impuesto)
    def consultar_disponibilidad(self):
        return True # Simulación de éxito

class AlquilerEquipos(ServicioBase):
    def calcular_costo(self, duracion, descuento=0):
        # Variante con descuento (Sobrecarga) [5]
        return (self.costo_base * duracion) - descuento

    def consultar_disponibilidad(self):
        # Simulación de error de disponibilidad
        return False

class AsesoriaEspecializada(ServicioBase):
    def calcular_costo(self, duracion):
        return self.costo_base * duracion

    def consultar_disponibilidad(self):
        return True
# GESTIÓN DE RESERVAS CON MANEJO DE EXCEPCIONES AVANZADO [3, 7, 11]
class reserva:
    def __init__(self, cliente, servicio, duracion):
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "PENDING"
    def procesar(self):
        try:
            logging.info(f"starting process for {self.cliente.obtener_detalles()}")
            if not self.servicio.consultar_disponibilidad():
                # Lanzamiento de excepción controlada [4, 12]
                raise ServiceUnavailableError(f"Servicio '{self.servicio.nombre}' is full")
            # Cálculo polimorfico [10]
            total = self.servicio.calcular_costo(self.duracion)
            self.estado = "CONFIRMED"
            print(f"RES_SUCCESS: Total price ${total}")

        except ServiceUnavailableError as e:
            # Encadenamiento de excepciones y registro en log [3, 4]
            logging.error(f"Reservation failed: {e}")
            self.estado = "REJECTED"
            # Se relanza la excepción para que el simulador la vea si es necesario
            raise SoftwareFJError("Process halted due to availability issues.") from e
        
        except Exception as e:
            # Captura genérica para mantener la estabilidad [2, 13]
            logging.critical(f"Unexpected system error: {e}")
            self.estado = "SYSTEM_ERROR"
        
        else:
            # Se ejecuta solo si no hubo excepciones [13, 14]
            logging.info("Transaction completed successfully.")
        
        finally:
            # Acción de limpieza o cierre siempre ejecutada [15, 16]
            print(f"Final Status: {self.estado}")

# 6. SIMULACIÓN DE 10 OPERACIONES (Registros y Reservas) [5]
def ejecutar_simulacion():
    print("--- SOFTWARE FJ SYSTEM SIMULATION (2026) ---")
    
    # Datos de prueba: Servicios
    s1 = ReservaSalas("Auditorium A", 100)
    s2 = AlquilerEquipos("Laptops Kit", 50)
    s3 = AsesoriaEspecializada("Cloud Architecture", 200)

    # Lista para simular operaciones consecutivas
    operaciones = [
        # (ID, Nombre, Email, Servicio, Duracion)
        ("1001", "Ana Garcia", "ana@fj.com", s1, 5),      # Operación 1: Válida
        ("1002", "Luis Perez", "luis@fj.com", s3, 2),     # Operación 2: Válida
        ("ABC", "Error User", "err@fj.com", s1, 3),       # Operación 3: ID Inválido
        ("1003", "Marta Ruiz", "marta@fj.com", s2, 4),    # Operación 4: Sin disponibilidad
        ("1004", "Jose Gil", "jose@fj.com", s1, 0),       # Operación 5: Válida
        ("1005", "Rosa Sol", "rosa@fj.com", s3, 8),       # Operación 6: Válida
        ("9999", "Tester", "test@fj.com", s2, 1),         # Operación 7: Fallida (equipo)
        ("1006", "Ian Cook", "ian@fj.com", s1, 2),        # Operación 8: Válida
        ("INVALID", "No Name", "no@fj.com", s3, 1),       # Operación 9: ID Inválido
        ("1007", "Eva Luna", "eva@fj.com", s3, 10),       # Operación 10: Válida
    ]

    for i, op in enumerate(operaciones, 1):
        print(f"\n>>> Running Operation {i}:")
        try:
            # Registro de cliente con validación encapsulada [8]
            cliente_obj = Cliente(op[0], op[1], op[2])
            reserva_obj = reserva(cliente_obj, op[3], op[4])
            reserva_obj.procesar()
        except SoftwareFJError as e:    
            print(f"Caught logic error: {e}")
        except Exception as e:
            print(f"Critical error bypassed: {e}")

if __name__ == "__main__":
    ejecutar_simulacion()
