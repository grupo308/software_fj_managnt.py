import logging
from cliente import Cliente, ClienteInvalidoError
from servicios import ReservaSalas, AlquilerEquipos, AsesoriaEspecializada
from reserva import Reserva
from excepciones import SoftwareFJError, DuracionInvalidaError

# Configuración global del archivo de Logs (error_log.txt) [cite: 92, 105]
logging.basicConfig(
    filename='error_log.txt', 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def ejecutar_simulacion():
    print("=== SISTEMA INTEGRAL SOFTWARE FJ - SIMULACIÓN FASE 4 ===\n")
    
    # Crear los servicios disponibles
    sala = ReservaSalas("Sala de Juntas A", 50000, "S01")
    equipos = AlquilerEquipos("Kit de Laptops", 30000, "S02")
    asesoria = AsesoriaEspecializada("Asesoría TI", 80000, "S03")

    # Lista de 10 operaciones (Datos para probar el sistema) 
    # Formato: (Nombre, Correo, Teléfono, ID, Servicio_Objeto, Duración)
    datos_operaciones = [
        ("Kevin Aguiar", "kevin@unad.edu.co", "3001234567", "101", sala, 3),      # 1. Exitosa
        ("Ana Lopez", "ana@mail.com", "3109876543", "102", asesoria, 2),          # 2. Exitosa
        ("Error User", "correo_malo", "123", "103", sala, 5),                      # 3. Fallo (Datos inválidos)
        ("Luis Perez", "luis@mail.com", "3201112233", "104", equipos, 4),         # 4. Fallo (Sin disponibilidad)
        ("Marta Ruiz", "marta@mail.com", "3004445566", "105", asesoria, 1),       # 5. Exitosa
        ("Jose Gil", "jose@mail.com", "3157778899", "106", sala, 0),              # 6. Fallo (Duración inválida)
        ("Rosa Sol", "rosa@mail.com", "3001239876", "107", equipos, 2),           # 7. Fallo (Sin disponibilidad)
        ("Ian Cook", "ian@mail.com", "3151234321", "108", sala, 2),               # 8. Exitosa
        ("Eva Luna", "eva@mail.com", "3104567890", "109", asesoria, 10),          # 9. Exitosa
        ("No Name", " ", "0000000", "110", sala, 1),                              # 10. Fallo (Nombre vacío)
    ]

    for i, datos in enumerate(datos_operaciones, 1):
        print(f"Ejecutando Operación #{i}...")
        try:
            # Intentamos crear el cliente (aquí puede saltar ClienteInvalidoError)
            nuevo_cliente = Cliente(datos[0], datos[1], datos[2], datos[3])
            
            # Intentamos procesar la reserva
            nueva_reserva = Reserva(nuevo_cliente, datos[4], datos[5])
            nueva_reserva.procesar()

        except ClienteInvalidoError as e:
            print(f"✘ Error en datos del cliente: {e}")
            logging.warning(f"Operación {i} fallida por datos de cliente: {e}")
            print("-" * 30)
            
        except DuracionInvalidaError as e:
            print(f"✘ Error en duración de reserva: {e}")
            logging.warning(f"Operación {i} fallida por duración inválida: {e}")
            print("-" * 30)
            
        except SoftwareFJError as e:
            print(f"✘ Error de negocio: {e}")
            print("-" * 30)
        except Exception as e:
            print(f"✘ Error crítico capturado: {e}")
            print("-" * 30)

    print("\n=== SIMULACIÓN FINALIZADA. REVISE 'error_log.txt' PARA DETALLES ===")

if __name__ == "__main__":
    ejecutar_simulacion()