# Ordenar una lista con Bubble Sort (ordenamiento de burbuja).
#
# ¿Qué hace?
# Recibe una lista de números y devuelve una nueva lista con los mismos
# números ordenados de menor a mayor.
#
# ¿Cómo lo hace?
# Recorre la lista comparando cada elemento con el que está a su derecha.
# Si están en el orden incorrecto, los intercambia.
# Después de cada recorrido (pasada), el número más grande "sube" hasta
# el final de la lista, como una burbuja.
# Se repiten tantas pasadas como elementos tenga la lista.
#
# Complejidad: O(n^2) (tiempo cuadrático)
# Hay un ciclo dentro de otro ciclo, igual que en 2_generar_rutas.py:
# el de afuera da n pasadas y el de adentro hace n - 1 comparaciones.
# En total son n * (n - 1) iteraciones, que crece aproximadamente como n^2.

def bubble_sort(lista):
    tamanio_input = len(lista)     # Tamaño de la entrada (n)
    iteraciones = 0                # Contador de operaciones realizadas
    lista_ordenada = lista.copy()  # Copiamos la lista para no modificar la original

    for pasada in range(tamanio_input):             # Se repite n veces

        for posicion in range(tamanio_input - 1):   # Se repite n - 1 veces por cada pasada
            iteraciones += 1

            elemento_actual = lista_ordenada[posicion]
            elemento_siguiente = lista_ordenada[posicion + 1]

            if elemento_actual > elemento_siguiente:
                # Están en el orden incorrecto, los intercambiamos
                lista_ordenada[posicion] = elemento_siguiente
                lista_ordenada[posicion + 1] = elemento_actual

    return tamanio_input, iteraciones, lista_ordenada

# Pruebas: listas de tamaño 6, 7 y 11.
# Esperamos n * (n - 1) iteraciones: 6 * 5 = 30, 7 * 6 = 42 y 11 * 10 = 110.
lista1 = [5, 9, 3, 5, 6, 0]
lista2 = [33, 6, 1, 98, 3, 1, 3]
lista3 = [1, 2, 333, 4, 5, 64, 6, 7, -8, 9, -10]
lista_pruebas = [lista1, lista2, lista3]

for lista in lista_pruebas:
    resultado_tamanio_input, resultado_iteraciones, resultado_lista_ordenada = bubble_sort(lista)
    print()
    print("resultado_tamanio_input:", resultado_tamanio_input)
    print("resultado_iteraciones:", resultado_iteraciones)
    print("resultado_lista_ordenada:", resultado_lista_ordenada)
