import logging
from cliente import Cliente, ClienteInvalidoError
from servicios import ReservaSalas, AlquilerEquipos, AsesoriaEspecializada
from reserva import Reserva
from excepciones import SoftwareFJError

logging.basicConfig(filename='error_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

def ejecutar():
    print("=== SOFTWARE FJ - SISTEMA UNIFICADO ===\n")
    s1, s2, s3 = ReservaSalas("Sala A", 50000), AlquilerEquipos("Laptops", 30000), AsesoriaEspecializada("TI", 80000)

    ops = [
        ("Kevin Aguiar", "kevin@mail.com", "300123", "101", s1, 3),  # Válida
        ("Ana Lopez", "ana@mail.com", "310456", "102", s3, 2),     # Válida
        ("Error", "malo", "000", "103", s1, 5),                    # ID/Correo malo
        ("Luis", "luis@mail.com", "320111", "104", s2, 4),         # Sin cupo
        ("Marta", "marta@mail.com", "300444", "105", s3, 1),       # Válida
        ("Jose", "jose@mail.com", "315777", "106", s1, 0),         # Duración 0
        ("Rosa", "rosa@mail.com", "300123", "107", s2, 2),         # Sin cupo
        ("Ian", "ian@mail.com", "315123", "108", s1, 2),           # Válida
        ("Eva", "eva@mail.com", "310456", "109", s3, 10),          # Válida
        ("No Name", " ", " ", "110", s1, 1),                       # Datos vacíos
    ]

    for i, d in enumerate(ops, 1):
        print(f"Op #{i}:")
        try:
            c = Cliente(d[0], d[1], d[2], d[3])
            r = Reserva(c, d[4], d[5])
            r.procesar()
        except (ClienteInvalidoError, SoftwareFJError) as e:
            print(f"✘ Error capturado: {e}")
        print("-" * 20)

if __name__ == "__main__": ejecutar()