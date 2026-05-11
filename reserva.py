import logging
from excepciones import ServiceUnavailableError, SoftwareFJError, DuracionInvalidaError, ReservaInvalidaError

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
            # Registro en el archivo de logs
            logging.info(f"Iniciando proceso de reserva para: {self.cliente.nombre}")

            # Validar que la duración sea mayor a cero
            if self.duracion <= 0:
                raise DuracionInvalidaError(
                    f"Duración inválida: {self.duracion}. Debe ser mayor a 0."
                )

            # Verificar disponibilidad del servicio
            if not self.servicio.consultar_disponibilidad():
                raise ServiceUnavailableError(
                    f"El servicio '{self.servicio.nombre}' no está disponible actualmente."
                )

            # Cálculo del costo usando polimorfismo
            total = self.servicio.calcular_costo(self.duracion)
            self.estado = "CONFIRMADA"
            print(f"✔ RESERVA EXITOSA: Cliente {self.cliente.nombre}. Total: ${total}")

        except DuracionInvalidaError as e:
            logging.error(f"Duración inválida: {e}")
            self.estado = "RECHAZADA"
            raise

        except ServiceUnavailableError as e:
            logging.error(f"Fallo en reserva por disponibilidad: {e}")
            self.estado = "RECHAZADA"
            raise SoftwareFJError("La operación fue detenida por problemas de cupo.") from e

        except Exception as e:
            logging.critical(f"Error inesperado: {e}")
            self.estado = "ERROR_SISTEMA"
            print("Ocurrió un error técnico, pero el sistema sigue activo.")

        else:
            logging.info(f"Transacción finalizada con éxito para {self.cliente.nombre}")

        finally:
            print(f"Resultado final del proceso: {self.estado}")
            print("-" * 30)

    def confirmar(self):
        """Confirma la reserva si está en estado PENDIENTE."""
        try:
            if self.estado != "PENDIENTE":
                raise ReservaInvalidaError(
                    f"No se puede confirmar una reserva en estado '{self.estado}'."
                )
            self.estado = "CONFIRMADA"
            logging.info(f"Reserva confirmada para {self.cliente.nombre}")
            print(f"✔ Reserva CONFIRMADA para {self.cliente.nombre}")
        except ReservaInvalidaError as e:
            logging.error(f"Error al confirmar: {e}")
            raise
        else:
            logging.info("Confirmación exitosa.")
        finally:
            print(f"Estado final: {self.estado}")

    def cancelar(self, motivo="Sin motivo especificado"):
        """Cancela la reserva si no ha sido procesada aún."""
        try:
            if self.estado == "CANCELADA":
                raise ReservaInvalidaError("La reserva ya está cancelada.")
            if self.estado == "CONFIRMADA":
                raise ReservaInvalidaError(
                    "No se puede cancelar una reserva ya confirmada."
                )
            self.estado = "CANCELADA"
            logging.warning(f"Reserva CANCELADA. Motivo: {motivo}")
            print(f"✘ Reserva CANCELADA. Motivo: {motivo}")
        except ReservaInvalidaError as e:
            logging.error(f"Error al cancelar: {e}")
            raise
        else:
            logging.info("Cancelación completada exitosamente.")
        finally:
            print(f"Estado final: {self.estado}")