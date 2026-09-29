# Encontrar un elemento por su índice.
#
# ¿Qué hace?
# Recibe una lista y un índice (la posición del elemento que queremos)
# y devuelve el elemento que está en esa posición.
# Recuerda que en Python los índices empiezan en 0: el primer elemento
# está en la posición 0, el segundo en la posición 1, etc.
#
# ¿Cómo lo hace?
# Accede directamente a la posición con lista[indice]. No necesita
# recorrer la lista, porque Python sabe exactamente en qué lugar de la
# memoria está cada posición.
#
# Complejidad: O(1) (tiempo constante)
# Sin importar si la lista tiene 6, 1,000 o 1,000,000 de elementos,
# siempre se hace 1 sola operación. El número de iteraciones NO depende
# del tamaño de la lista.

def encontrar_por_indice(lista, indice):
    tamanio_input = len(lista)  # Tamaño de la entrada (n)
    iteraciones = 0             # Contador de operaciones realizadas

    elemento_encontrado = lista[indice]  # Acceso directo, sin recorrer la lista
    iteraciones += 1

    return tamanio_input, iteraciones, elemento_encontrado

# Pruebas: cada prueba es una pareja (lista, índice a buscar).
# Aunque las listas tienen tamaños distintos (6, 7 y 11),
# esperamos siempre 1 iteración.
lista1 = [5, 9, 3, 5, 6, 0]
lista2 = [33, 6, 1, 98, 3, 1, 3]
lista3 = [1, 2, 333, 4, 5, 64, 6, 7, -8, 9, -10]
lista_pruebas = [(lista1, 2), (lista2, 4), (lista3, 6)]

for lista, indice in lista_pruebas:
    resultado_tamanio_input, resultado_iteraciones, resultado_elemento_encontrado = encontrar_por_indice(lista, indice)
    print()
    print("resultado_tamanio_input:", resultado_tamanio_input)
    print("resultado_iteraciones:", resultado_iteraciones)
    print("resultado_elemento_encontrado:", resultado_elemento_encontrado)
