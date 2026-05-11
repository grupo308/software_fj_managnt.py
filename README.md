# Este es un espacio para el desarrollo de python main.py
Tarea 4 trabajo colaborativo Estructura base de clientes y manejo de excepciones SoftwareFJError

# Sistema Integral de Gestión Software FJ - Fase 4

## Descripción
Este proyecto implementa un sistema de gestión de clientes y reservas para la empresa "Software FJ". El software aplica de forma rigurosa los pilares de la POO (Abstracción, Herencia, Polimorfismo y Encapsulamiento) y se enfoca en la robustez mediante un manejo avanzado de excepciones.

## Requerimientos Técnicos Cumplidos
1. **Unificación:** Sistema consolidado en `software_fj_managnt.py`.
2. **Abstracción Real:** Uso de la clase `ABC` para `EntidadBase` y `Servicio`.
3. **Robustez:** Validación de duración > 0 y IDs numéricos.
4. **Persistencia:** Registro de eventos en el archivo `software_fj.log`.


## Cómo Ejecutar
1. Clonar el repositorio: `git clone [https://github.com/grupo308/software_fj_managnt.py.git]`
2. Ejecutar el archivo principal: `python main.py`
3. Mostrara los resultados de las 10 operaciones simuladas.

## Integrantes - Grupo 308
Estudiante 1: Ivan Darío Saenz Lugo
Estudiante 2: Duván Andrés Fajardo Mejía
Estudiante 3: Eliana Marcela Rojas Garzón
Estudiante 4: Kevin Arley Aguiar Rubiano
Estudiante 5:


## Correcciones Aplicadas
1. **Unificación:** Código centralizado en módulos, ejecutado desde `main.py`.
2. **Abstracción:** Uso estricto de `ABC` y `@abstractmethod`.
3. **Cancelación:** Método `cancelar()` implementado en `Reserva`.
4. **Logs:** Limpieza de mensajes en `error_log.txt`.
5. **Validación:** Control de duración > 0.
6. **Estructura:** README detallado.