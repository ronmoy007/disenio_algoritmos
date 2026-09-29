# Ordenar una lista con Merge Sort (ordenamiento por mezcla).
#
# ¿Qué hace?
# Recibe una lista de números y devuelve una nueva lista con los mismos
# números ordenados de menor a mayor. Resuelve el MISMO problema que
# 3_bubble_sort.py, pero con un algoritmo diferente y más eficiente.
#
# ¿Cómo lo hace?
# Usa una estrategia llamada "divide y vencerás":
#   1. Dividir la lista a la mitad, una y otra vez, hasta tener
#      listas de un solo elemento (una lista de 1 elemento ya está ordenada).
#   2. Mezclar (merge) las listas pequeñas ya ordenadas para formar
#      listas más grandes, también ordenadas.
#
# Complejidad: O(n log n)
# La lista se puede partir a la mitad log2(n) veces (igual que en
# 4_busqueda_binaria.py), así que hay log2(n) niveles de divisiones.
# En cada nivel, la función mezclar recorre los n elementos una vez.
# En total: n elementos * log2(n) niveles = n * log2(n) iteraciones,
# que es mucho mejor que el O(n^2) de Bubble Sort.

def mezclar(lista_izquierda, lista_derecha):
    lista_mezclada = []
    iteraciones = 0  # Contador de operaciones realizadas
    i = 0  # Posición actual en lista_izquierda
    d = 0  # Posición actual en lista_derecha

    # Mientras ambas listas tengan elementos, tomamos el más pequeño de los dos
    while i < len(lista_izquierda) and d < len(lista_derecha):
        iteraciones += 1

        if lista_izquierda[i] <= lista_derecha[d]:
            lista_mezclada.append(lista_izquierda[i])
            i += 1
        else:
            lista_mezclada.append(lista_derecha[d])
            d += 1

    # Si sobraron elementos en la lista izquierda, los agregamos al final
    while i < len(lista_izquierda):
        iteraciones += 1
        lista_mezclada.append(lista_izquierda[i])
        i += 1

    # Si sobraron elementos en la lista derecha, los agregamos al final
    while d < len(lista_derecha):
        iteraciones += 1
        lista_mezclada.append(lista_derecha[d])
        d += 1

    return iteraciones, lista_mezclada

def merge_sort(lista):
    tamanio_input = len(lista)  # Tamaño de la entrada (n)

    # Caso base: una lista con 0 o 1 elementos ya está ordenada
    if tamanio_input <= 1:
        return tamanio_input, 0, lista

    # Dividimos la lista a la mitad
    mitad = tamanio_input // 2
    lista_izquierda = lista[:mitad]
    lista_derecha = lista[mitad:]

    # Ordenamos cada mitad llamando a la misma función (recursión)
    _, iteraciones_izquierda, izquierda_ordenada = merge_sort(lista_izquierda)
    _, iteraciones_derecha, derecha_ordenada = merge_sort(lista_derecha)

    # Mezclamos las dos mitades ya ordenadas
    iteraciones_mezcla, lista_ordenada = mezclar(izquierda_ordenada, derecha_ordenada)

    iteraciones = iteraciones_izquierda + iteraciones_derecha + iteraciones_mezcla

    return tamanio_input, iteraciones, lista_ordenada

# Pruebas: listas de tamaño 4, 8 y 16 (potencias de 2), para que las mitades
# siempre sean iguales y el resultado sea exacto.
# Esperamos n * log2(n) iteraciones: 4 * 2 = 8, 8 * 3 = 24 y 16 * 4 = 64.
lista1 = [5, 9, 3, 0]
lista2 = [33, 6, 1, 98, 3, 1, 3, -8]
lista3 = [1, 2, 333, 4, 5, 64, 6, 7, -8, 9, -10, 150, 20, 3, 0, 12]
lista_pruebas = [lista1, lista2, lista3]

for lista in lista_pruebas:
    resultado_tamanio_input, resultado_iteraciones, resultado_lista_ordenada = merge_sort(lista)
    print()
    print("resultado_tamanio_input:", resultado_tamanio_input)
    print("resultado_iteraciones:", resultado_iteraciones)
    print("resultado_lista_ordenada:", resultado_lista_ordenada)
