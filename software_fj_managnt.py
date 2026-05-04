import logging
from abc import ABC, abstractmethod
from datetime import datetime

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
    def __init__(self, id_cliente, nombre, email, telefono):
        #ATRIBUTOS PRIVADOS PARA ENCAPSULAMIENTO
        self.__id=None
        self.__nombre=None
        self.__email=None
        self.__telefono=None
        #VALIDACION AL CREAR EL CLIENTE
        self.__id=self.validar_id(id_cliente)
        self.nombre=nombre
        self.email=email
        self.telefono=telefono
    def validar_id(self, id_valor):
        if not str(id_valor).isdigit():
            raise InvalidDataError(f"ID '{id_valor}' Solo se permiten numeros.")
        return str(id_valor)
    @property
    def id(self):
        return self.__id
    @property
    def nombre(self):
        return self.__nombre
    @nombre.setter
    def nombre(self, valor):
        if not valor or len(valor.strip()) <3:
            raise InvalidDataError(f"Nombre invalido: '{valor}'. Debe tener al menos 3 caracteres.")
        self.__nombre = valor.strip()
    @property
    def email(self):
        return self.__email
    @email.setter
    def email(self, valor):
        if "@" not in valor or "." not in valor:
            raise InvalidDataError(f"Email invalido: '{valor}'.Formato: usuario@dominio.com")
        self.__email = valor.strip().lower()
    @property
    def telefono(self):
        return self.__telefono
    @telefono.setter
    def telefono(self, valor):
        if not str(valor).isdigit()or len(str(valor))!=10:
            raise InvalidDataError(f"Telefono invalido: '{valor}'. Debe ser un numero de 10 digitos.")
        self.__telefono = str(valor)
        
    def obtener_detalles(self):
        return (f"Cliente[ID: {self.__id} |"
                f"Nombre: {self.__nombre} |"
                f"Email: {self.__email} |"
                f"Tel: {self.__telefono}]")
        
# JERARQUIA DE SERVICIOS (Herencia y Polimorfismo) [7, 9]
class ServicioBase(ABC):
    def __init__(self, nombre, costo_base, id_servicio):
        self.nombre = nombre
        self.costo_base = costo_base
        self.id_servicio = id_servicio
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
class Reserva:
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

#GESTIÓN DEL SISTEMA CENTRALIZADA (Clase GestorSistema) 
# esta clase centraliza la gestión de clientes, servicios y reservas, 
# facilitando la simulación y el manejo de excepciones a nivel de sistema. [7, 9, 11]        
class GestorSistema:
    def __init__(self):
        # Diccionarios internos que actúan como libro de registros
        # Se usa ID como clave única para búsqueda rápida
        self.__clientes = {}
        self.__servicios = {}
        self.__reservas = {}
    def registrar_cliente(self, id_cliente, nombre, email, telefono):
        # Verifica que no exista un cliente con el mismo ID antes de crear uno nuevo
        if id_cliente in self.__clientes:
            raise InvalidDataError(f"Client with ID ´{id_cliente}´ already exists.")
        try:
            # Crea el cliente y lo guarda en el diccionario con su ID como clave para fácil acceso
            self.__clientes[id_cliente]=Cliente(id_cliente, nombre, email, telefono)
            logging.info(f"Registered customer: {id_cliente}")
        except InvalidDataError as e:
            logging.warning(f"Failed to register customer: {e}")
            raise   
    def registrar_servicio(self, servicio):
        # Verifica que no exista un servicio con el mismo ID
        if servicio.id_servicio in self.__servicios:
            raise InvalidDataError(f"Service '{servicio.id_servicio}' is not available.")
        try:
            self.__servicios[servicio.id_servicio]=servicio
            logging.info(f"Registered service: {servicio.id_servicio}")
        except InvalidDataError as e:
            logging.warning(f"Failed to register service: {e}")
            raise
    def crear_reserva(self, id_cliente, id_servicio, duracion):
        # Verifica que el cliente esté registrado antes de continuar
        if id_cliente not in self.__clientes:
            raise InvalidDataError(f"Client with ID '{id_cliente}' not found.")
        if id_servicio not in self.__servicios:
            raise InvalidDataError(f"Service with ID '{id_servicio}' not found.")
        if not self.__servicios[id_servicio].consultar_disponibilidad():
            raise ServiceUnavailableError(f"Service '{id_servicio}' is not available.")
        if duracion <= 0:
            raise InvalidDataError(f"Invalid duration: {duracion}. Must be greater than 0.")
        reserva = Reserva(self.__clientes[id_cliente], self.__servicios[id_servicio], duracion)
        try:
            reserva.procesar()
            # Genera un ID único usando cliente + fecha/hora exacta
            # para no tener conflictos en caso de dos reservas del mismo cliente
            id_reserva=f"{id_cliente}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            self.__reservas[id_reserva]=reserva
            logging.info(f"Created reservation for client '{id_cliente}' and service '{id_servicio}' with duration {duracion}.")
        except SoftwareFJError as e:
            logging.error(f"Failed to create reservation: {e}")
            raise
    def mostrar_resumen(self):  # Imprime el estado completo del sistema como un libro de registros
        print("\n--- System Summary ---")
        print("\n----Clients----")  # Lista todos los clientes registrados con sus detalles
        for id, cliente in self.__clientes.items():
            print(f" {cliente.obtener_detalles()}")
        print("\n----Services----")  # Lista todos los servicios dsponibles
        for id, servicio in self.__servicios.items():
            print(f" {servicio.nombre} | base cost: ${servicio.costo_base}")
        print("\n----Reservations----") # Lista todas las reservas con su estado actual
        for id, reserva in self.__reservas.items():
            print(f" {id} | Client: {reserva.cliente.nombre} | Service: {reserva.servicio.nombre} | Duration: {reserva.duracion}h | Status: {reserva.estado}")
# 6. SIMULACIÓN DE 10 OPERACIONES (Registros y Reservas) [5]
def ejecutar_simulacion():
    print("--- SOFTWARE FJ SYSTEM SIMULATION (2026) ---")
    #se crea el gestor del sistema para centralizar la gestión de clientes, servicios y reservas
    gestor=GestorSistema()
    
    # registro de servicios con validación encapsulada [8]
    gestor.registrar_servicio(ReservaSalas("Auditorium A", 100, "S1"))
    gestor.registrar_servicio(AlquilerEquipos("Laptops Kit", 50, "S2"))
    gestor.registrar_servicio(AsesoriaEspecializada("Cloud Architecture", 200, "S3"))

    # Lista para simular operaciones consecutivas
    operaciones = [
   # (ID, Nombre, Email, Telefono, Servicio, Duracion)
        ("1001", "Ana Garcia", "ana@fj.com", "3001234567", "S1", 5),      # Operación 1: Válida
        ("1002", "Luis Perez", "luis@fj.com", "3109876543", "S3", 2),     # Operación 2: Válida
        ("ABC", "Error User", "err@fj.com", "3001112222", "S1", 3),       # Operación 3: ID Inválido
        ("1003", "Marta Ruiz", "marta@fj.com", "3205554433", "S2", 4),    # Operación 4: Sin disponibilidad
        ("1004", "Jose Gil", "jose@fj.com", "3157778899", "S1", 0),       # Operación 5: Duración inválida
        ("1005", "Rosa Sol", "rosa@fj.com", "3001239876", "S3", 8),       # Operación 6: Válida
        ("9999", "Tester", "test@fj.com", "3209991234", "S2", 1),         # Operación 7: Fallida (equipo)
        ("1006", "Ian Cook", "ian@fj.com", "3151234321", "S1", 2),        # Operación 8: Válida
        ("INVALID", "No Name", "no@fj.com", "3001110000", "S3", 1),       # Operación 9: ID Inválido
        ("1007", "Eva Luna", "eva@fj.com", "3104567890", "S3", 10),       # Operación 10: Válida
    ]

    for i, op in enumerate(operaciones, 1):
        print(f"\n>>> Running Operation {i}:")
        try:
            # Registro del cliente y creación de reserva con manejo de excepciones integrado
            gestor.registrar_cliente(op[0], op[1], op[2], op[3])
            gestor.crear_reserva(op[0], op[4], op[5])
        except SoftwareFJError as e:    
            print(f"Caught logic error: {e}")
        except Exception as e:
            print(f"Critical error bypassed: {e}")
    # Mostrar resumen final del sistema
    gestor.mostrar_resumen()

if __name__ == "__main__":
    ejecutar_simulacion()
