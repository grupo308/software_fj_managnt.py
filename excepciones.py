# Módulo de excepciones personalizadas para Software FJ
class SoftwareFJError(Exception):
    """Clase base para todas las excepciones del sistema."""
    pass

class InvalidDataError(SoftwareFJError):
    """Se lanza cuando los datos de entrada no son válidos."""
    pass

class ServiceUnavailableError(SoftwareFJError):
    """Se lanza cuando un servicio no está disponible."""
    pass

class DuracionInvalidaError(SoftwareFJError):
    """Se lanza cuando la duración de una reserva es inválida (cero o negativa)."""
    pass

class DescuentoInvalidoError(SoftwareFJError):
    """Se lanza cuando el descuento aplicado está fuera del rango permitido (0% - 50%)."""
    pass

class ReservaInvalidaError(SoftwareFJError):
    """Se lanza cuando una reserva no puede confirmarse o cancelarse."""
    pass