# Buscar un número en una lista ordenada con búsqueda binaria.
#
# ¿Qué hace?
# Recibe una lista que YA ESTÁ ORDENADA y un número a buscar.
# Devuelve la posición donde se encuentra el número, o -1 si no está.
#
# ¿Cómo lo hace?
# En lugar de revisar los elementos uno por uno, revisa el elemento
# de en medio:
#   - Si es el número buscado, terminamos.
#   - Si el número buscado es más grande, descartamos la mitad izquierda.
#   - Si el número buscado es más pequeño, descartamos la mitad derecha.
# En cada iteración, la parte de la lista donde buscamos se reduce a la mitad.
#
# Complejidad: O(log n) (tiempo logarítmico)
# ¿Cuántas veces se puede partir n a la mitad hasta quedar 1 elemento?
# log2(n) veces. Por ejemplo, con n = 8: 8 -> 4 -> 2 -> 1 son 3 divisiones,
# así que log2(8) = 3.
# Si la lista crece al doble, solo se necesita 1 iteración más.

def busqueda_binaria(lista, numero_buscado):
    tamanio_input = len(lista)  # Tamaño de la entrada (n)
    iteraciones = 0             # Contador de operaciones realizadas
    posicion_encontrada = -1    # -1 significa que no se encontró

    izquierda = 0                 # Inicio de la parte donde buscamos
    derecha = tamanio_input - 1   # Final de la parte donde buscamos

    while izquierda <= derecha:
        iteraciones += 1

        mitad = (izquierda + derecha) // 2 # El operador // hace división entera, descartando decimales
        elemento_mitad = lista[mitad]

        if elemento_mitad == numero_buscado:
            posicion_encontrada = mitad
            break
        elif elemento_mitad < numero_buscado:
            izquierda = mitad + 1   # Descartamos la mitad izquierda
        else:
            derecha = mitad - 1     # Descartamos la mitad derecha

    return tamanio_input, iteraciones, posicion_encontrada

# Pruebas: cada prueba es una pareja (lista ordenada, número a buscar).
# Las listas tienen tamaño 8, 16 y 32 (potencias de 2).
# Esperamos log2(n) iteraciones: log2(8) = 3, log2(16) = 4 y log2(32) = 5.
lista1 = [-8, 0, 3, 5, 6, 9, 12, 20]
lista2 = [-10, -8, 1, 1, 2, 3, 4, 5, 6, 7, 9, 33, 64, 98, 150, 333]
lista3 = [-50, -40, -30, -20, -10, -8, -5, -1, 0, 1, 2, 3, 4, 5, 6, 7,
          8, 9, 10, 12, 15, 20, 25, 30, 33, 40, 50, 64, 75, 98, 150, 333]
lista_pruebas = [(lista1, 12), (lista2, 150), (lista3, 150)]

for lista, numero_buscado in lista_pruebas:
    resultado_tamanio_input, resultado_iteraciones, resultado_posicion_encontrada = busqueda_binaria(lista, numero_buscado)
    print()
    print("resultado_tamanio_input:", resultado_tamanio_input)
    print("resultado_iteraciones:", resultado_iteraciones)
    print("resultado_posicion_encontrada:", resultado_posicion_encontrada)
