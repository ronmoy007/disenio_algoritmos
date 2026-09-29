# Generar todas las rutas posibles entre aeropuertos.
#
# ¿Qué hace?
# Recibe una lista de aeropuertos y devuelve todas las rutas posibles
# (origen, destino) entre ellos. No se generan rutas de un aeropuerto
# hacia sí mismo, por ejemplo ("MEX", "MEX").
#
# ¿Cómo lo hace?
# Usa un ciclo dentro de otro ciclo (ciclos anidados):
#   - El ciclo de afuera elige un aeropuerto de origen.
#   - El ciclo de adentro recorre todos los aeropuertos como destino.
# Por cada origen se revisan TODOS los destinos.
#
# Complejidad: O(n^2) (tiempo cuadrático)
# Si hay n aeropuertos, el ciclo de afuera da n vueltas y, en cada una,
# el ciclo de adentro da otras n vueltas: n * n = n^2 iteraciones.
# Si la lista crece al doble, las iteraciones crecen 4 veces.

def generar_rutas(lista_rutas):
    tamanio_input = len(lista_rutas)  # Tamaño de la entrada (n)
    iteraciones = 0                   # Contador de operaciones realizadas
    rutas_generadas = []

    for origen in lista_rutas:             # Se repite n veces

        for destino in lista_rutas:        # Se repite n veces por cada origen
            iteraciones += 1

            if origen != destino:          # Evitamos rutas como ("MEX", "MEX")
                rutas_generadas.append((origen, destino))

    return tamanio_input, iteraciones, rutas_generadas

# Pruebas: listas de 2, 3 y 4 aeropuertos.
# Esperamos n * n iteraciones: 2 * 2 = 4, 3 * 3 = 9 y 4 * 4 = 16.
lista_rutas1 = ["MEX", "USA"]
lista_rutas2 = ["MEX", "USA", "CAN"]
lista_rutas3 = ["MEX", "USA", "CAN", "BRA"]
lista_pruebas = [lista_rutas1, lista_rutas2, lista_rutas3]

for lista in lista_pruebas:
    resultado_tamanio_input, resultado_iteraciones, resultado_rutas = generar_rutas(lista)
    print()
    print("resultado_tamanio_input:", resultado_tamanio_input)
    print("resultado_iteraciones:", resultado_iteraciones)
    print("resultado_rutas:", resultado_rutas)
