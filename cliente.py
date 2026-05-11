# ============================================================
# MÓDULO: cliente.py
# DESCRIPCIÓN: Define la clase Cliente con validaciones robustas
# y encapsulación de datos personales.
# AUTORA: Eliana Marcela Rojas Garzón
# CURSO: Programación 213023 - UNAD
# FASE: 4 - Prácticas Simuladas
# ============================================================

import re
from abc import ABC, abstractmethod
from excepciones import ClienteInvalidoError

class EntidadBase(ABC):
    @abstractmethod
    def describir(self):
        """Contrato obligatorio para clases derivadas (Punto 2)."""
        pass

class Cliente(EntidadBase):
    def __init__(self, nombre, correo, telefono, identificacion):
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        self.identificacion = identificacion

    @property
    def nombre(self): return self.__nombre
    @nombre.setter
    def nombre(self, v):
        if not v or not v.strip(): raise ClienteInvalidoError("Nombre vacío.")
        self.__nombre = v.strip()

    @property
    def correo(self): return self.__correo
    @correo.setter
    def correo(self, v):
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w{2,}$', v):
            raise ClienteInvalidoError(f"Correo '{v}' inválido.")
        self.__correo = v

    @property
    def identificacion(self): return self.__identificacion
    @identificacion.setter
    def identificacion(self, v):
        if not str(v).isdigit(): raise ClienteInvalidoError("ID debe ser numérico.")
        self.__identificacion = str(v)

    def describir(self):
        # Punto 4: Se usa el atributo, evitando imprimir el método
        return f"Cliente: {self.nombre} | ID: {self.identificacion} | Correo: {self.correo}"