# ============================================================
# MÓDULO: cliente.py
# DESCRIPCIÓN: Define la clase Cliente con validaciones robustas
# y encapsulación de datos personales.
# AUTORA: Eliana Marcela Rojas Garzón
# CURSO: Programación 213023 - UNAD
# FASE: 4 - Prácticas Simuladas
# ============================================================

import re  # Módulo para validar el formato del correo electrónico


# --- Excepción personalizada para clientes inválidos ---
class ClienteInvalidoError(Exception):
    """
    Excepción personalizada que se lanza cuando los datos
    de un cliente no superan las validaciones requeridas.
    """
    pass


# --- Clase base abstracta ---
class EntidadBase:
    """
    Clase abstracta que representa una entidad general del sistema.
    Toda entidad debe implementar el método describir().
    """

    def describir(self):
        # Este método debe ser implementado por cada subclase
        raise NotImplementedError("El método describir() debe implementarse en la subclase.")


# --- Clase Cliente ---
class Cliente(EntidadBase):
    """
    Representa un cliente del sistema Software FJ.
    Implementa encapsulación estricta mediante propiedades
    con validaciones sobre cada atributo privado.
    """

    def __init__(self, nombre, correo, telefono, identificacion):
        """
        Constructor de la clase Cliente.
        Recibe los datos personales y los valida antes de asignarlos.
        Lanza ClienteInvalidoError si algún dato es inválido.
        """
        # Se usan los setters para aplicar validaciones desde el inicio
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        self.identificacion = identificacion

    # --- Propiedad: nombre ---
    @property
    def nombre(self):
        # Retorna el nombre privado del cliente
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        # Valida que el nombre no esté vacío ni sea solo espacios
        if not valor or not valor.strip():
            raise ClienteInvalidoError("El nombre del cliente no puede estar vacío.")
        self.__nombre = valor.strip()

    # --- Propiedad: correo ---
    @property
    def correo(self):
        # Retorna el correo privado del cliente
        return self.__correo

    @correo.setter
    def correo(self, valor):
        # Valida que el correo tenga un formato básico con '@' y dominio
        patron = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
        if not re.match(patron, valor):
            raise ClienteInvalidoError(
                f"El correo '{valor}' no tiene un formato válido."
            )
        self.__correo = valor

    # --- Propiedad: telefono ---
    @property
    def telefono(self):
        # Retorna el teléfono privado del cliente
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        # Valida que el teléfono contenga solo dígitos y tenga entre 7 y 15 caracteres
        if not str(valor).isdigit() or not (7 <= len(str(valor)) <= 15):
            raise ClienteInvalidoError(
                f"El teléfono '{valor}' no es válido. Debe contener entre 7 y 15 dígitos."
            )
        self.__telefono = str(valor)

    # --- Propiedad: identificacion ---
    @property
    def identificacion(self):
        # Retorna la identificación privada del cliente
        return self.__identificacion

    @identificacion.setter
    def identificacion(self, valor):
        # Valida que la identificación no esté vacía
        if not str(valor).strip():
            raise ClienteInvalidoError("La identificación del cliente no puede estar vacía.")
        self.__identificacion = str(valor).strip()

    # --- Método describir (implementación del método abstracto) ---
    def describir(self):
        """
        Retorna una descripción legible del cliente con sus datos principales.
        """
        return (
            f"Cliente: {self.__nombre} | "
            f"ID: {self.__identificacion} | "
            f"Correo: {self.__correo} | "
            f"Teléfono: {self.__telefono}"
        )

    # --- Representación en consola ---
    def __str__(self):
        # Permite imprimir el objeto directamente con print()
        return self.describir()


# ============================================================
# BLOQUE DE PRUEBAS - Demuestra el funcionamiento de la clase
# ============================================================
if __name__ == "__main__":

    print("=" * 60)
    print("PRUEBAS DE LA CLASE CLIENTE")
    print("=" * 60)

    # --- Operación 1: Registro de cliente válido ---
    print("\n[Operación 1] Registro de cliente válido:")
    try:
        cliente1 = Cliente(
            nombre="Juan Pérez",
            correo="juan.perez@email.com",
            telefono="3001234567",
            identificacion="1098765432"
        )
        print(f"  ✔ Cliente creado exitosamente: {cliente1}")
    except ClienteInvalidoError as e:
        print(f"  ✘ Error: {e}")

    # --- Operación 2: Registro con correo inválido ---
    print("\n[Operación 2] Registro con correo inválido:")
    try:
        cliente2 = Cliente(
            nombre="María López",
            correo="correo-sin-arroba",
            telefono="3109876543",
            identificacion="1087654321"
        )
    except ClienteInvalidoError as e:
        # Se captura la excepción y se informa sin detener el programa
        print(f"  ✘ ClienteInvalidoError capturada: {e}")
    finally:
        # El bloque finally garantiza que siempre se registre el intento
        print("  → Intento de registro procesado (válido o inválido).")

    # --- Operación 3: Registro con nombre vacío ---
    print("\n[Operación 3] Registro con nombre vacío:")
    try:
        cliente3 = Cliente(
            nombre="   ",
            correo="sinnombre@email.com",
            telefono="3201112233",
            identificacion="1076543210"
        )
    except ClienteInvalidoError as e:
        print(f"  ✘ ClienteInvalidoError capturada: {e}")
    else:
        # El bloque else solo se ejecuta si no hubo excepción
        print("  ✔ Cliente registrado correctamente.")
    finally:
        print("  → Operación 3 finalizada.\n")