import logging
from excepciones import ServiceUnavailableError, SoftwareFJError

class Reserva:
    """
    Gestiona la unión entre Cliente y Servicio.
    Implementa el procesamiento con manejo avanzado de excepciones.
    """
    def __init__(self, cliente, servicio, duracion):
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "PENDIENTE"

    def procesar(self):
        try:
            # Registro en el archivo de logs (exigido por la guía)
            logging.info(f"Iniciando proceso de reserva para: {self.cliente.nombre}")
            
            # 1. Verificar disponibilidad
            if not self.servicio.consultar_disponibilidad():
                # Lanzamiento de excepción personalizada [cite: 91]
                raise ServiceUnavailableError(f"El servicio '{self.servicio.nombre}' no está disponible actualmente.")
            
            # 2. Cálculo del costo usando polimorfismo
            total = self.servicio.calcular_costo(self.duracion)
            self.estado = "CONFIRMADA"
            print(f"✔ RESERVA EXITOSA: Cliente {self.cliente.nombre}. Total: ${total}")

        except ServiceUnavailableError as e:
            # Encadenamiento de excepciones (mantiene el rastro del error) [cite: 91]
            logging.error(f"Fallo en reserva por disponibilidad: {e}")
            self.estado = "RECHAZADA"
            raise SoftwareFJError("La operación fue detenida por problemas de cupo.") from e
        
        except Exception as e:
            # Captura genérica para que el sistema no se cierre (estabilidad) [cite: 85, 93]
            logging.critical(f"Error inesperado: {e}")
            self.estado = "ERROR_SISTEMA"
            print("Ocurrió un error técnico, pero el sistema sigue activo.")
        
        else:
            # Se ejecuta solo si todo salió bien [cite: 91]
            logging.info(f"Transacción finalizada con éxito para {self.cliente.nombre}")
        
        finally:
            # Se ejecuta siempre, sin importar si hubo error o no [cite: 91]
            print(f"Resultado final del proceso: {self.estado}")
            print("-" * 30)