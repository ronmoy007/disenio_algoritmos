# Ordenar una lista con Merge Sort (ordenamiento por mezcla).
# Versión simplificada de 5_merge_sort.py, para leer solo el algoritmo.
#
# ¿Qué hace?
# Recibe una lista de números y devuelve una nueva lista con los mismos
# números ordenados de menor a mayor. Resuelve el MISMO problema que
# 3_bubble_sort.py, pero con un algoritmo diferente.
#
# ¿Cómo lo hace?
# Usa una estrategia llamada "divide y vencerás":
#   1. Dividir la lista a la mitad, una y otra vez, hasta tener
#      listas de un solo elemento (una lista de 1 elemento ya está ordenada).
#   2. Mezclar (merge) las listas pequeñas ya ordenadas para formar
#      listas más grandes, también ordenadas.

def mezclar(lista_izquierda, lista_derecha):
    lista_mezclada = []
    i = 0  # Posición actual en lista_izquierda
    d = 0  # Posición actual en lista_derecha

    # Mientras ambas listas tengan elementos, tomamos el más pequeño de los dos
    while i < len(lista_izquierda) and d < len(lista_derecha):

        if lista_izquierda[i] <= lista_derecha[d]:
            lista_mezclada.append(lista_izquierda[i])
            i += 1
        else:
            lista_mezclada.append(lista_derecha[d])
            d += 1

    # Si sobraron elementos en la lista izquierda, los agregamos al final
    while i < len(lista_izquierda):
        lista_mezclada.append(lista_izquierda[i])
        i += 1

    # Si sobraron elementos en la lista derecha, los agregamos al final
    while d < len(lista_derecha):
        lista_mezclada.append(lista_derecha[d])
        d += 1

    return lista_mezclada

def merge_sort(lista):

    # Caso base: una lista con 0 o 1 elementos ya está ordenada
    if len(lista) <= 1:
        return lista

    # Dividimos la lista a la mitad
    mitad = len(lista) // 2
    lista_izquierda = lista[:mitad]
    lista_derecha = lista[mitad:]

    # Ordenamos cada mitad llamando a la misma función (recursión)
    izquierda_ordenada = merge_sort(lista_izquierda)
    derecha_ordenada = merge_sort(lista_derecha)

    # Mezclamos las dos mitades ya ordenadas
    lista_ordenada = mezclar(izquierda_ordenada, derecha_ordenada)

    return lista_ordenada

# Pruebas: lista4 es el ejemplo que se sigue paso a paso en
# merge_sort_recursion.md y merge_sort_explanation.md.
lista1 = [5, 9, 3, 0]
lista2 = [33, 6, 1, 98, 3, 1, 3, -8]
lista3 = [1, 2, 333, 4, 5, 64, 6, 7, -8, 9, -10, 150, 20, 3, 0, 12]
lista4 = [8, 7, 6, 5, 4, 3, 2, 1]
lista_pruebas = [lista1, lista2, lista3, lista4]

for lista in lista_pruebas:
    resultado_lista_ordenada = merge_sort(lista)
    print()
    print("lista_original:", lista)
    print("resultado_lista_ordenada:", resultado_lista_ordenada)
