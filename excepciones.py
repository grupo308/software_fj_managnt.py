class SoftwareFJError(Exception):
    """Clase base para todas las excepciones del sistema."""
    pass

class ClienteInvalidoError(SoftwareFJError):
    """Se lanza cuando los datos de un cliente no son válidos."""
    pass

class ServiceUnavailableError(SoftwareFJError):
    """Se lanza cuando un servicio no está disponible."""
    pass

class DuracionInvalidaError(SoftwareFJError):
    """Se lanza cuando la duración es cero o negativa (Punto 5)."""
    pass

class ReservaInvalidaError(SoftwareFJError):
    """Se lanza para errores en el estado de la reserva."""
    pass