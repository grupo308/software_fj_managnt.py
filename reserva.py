import logging
from excepciones import SoftwareFJError, ServiceUnavailableError, DuracionInvalidaError

class Reserva:
    def __init__(self, cliente, servicio, duracion):
        # Punto 5: Validar duración mayor a cero
        if duracion <= 0:
            raise DuracionInvalidaError(f"Duración ({duracion}) debe ser mayor a 0.")
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "PENDIENTE"

    def procesar(self):
        try:
            logging.info(f"Procesando: {self.cliente.nombre}")
            if not self.servicio.consultar_disponibilidad():
                raise ServiceUnavailableError(f"Servicio '{self.servicio.nombre}' sin cupo.")
            
            costo = self.servicio.calcular_costo(self.duracion)
            self.estado = "CONFIRMADA"
            print(f"✔ EXITOSA: {self.cliente.nombre}. Total: ${costo}")
        except (DuracionInvalidaError, ServiceUnavailableError) as e:
            logging.error(f"Fallo: {e}")
            self.estado = "RECHAZADA"
            raise SoftwareFJError(str(e)) from e
        finally:
            print(f"Estado final: {self.estado}")

    def cancelar(self):
        # Punto 3: Método cancelar
        self.estado = "CANCELADA"
        logging.info(f"Reserva cancelada: {self.cliente.nombre}")
        print(f"✘ Reserva de {self.cliente.nombre} CANCELADA.")