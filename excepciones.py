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