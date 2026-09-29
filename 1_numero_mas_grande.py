# Encontrar el número más grande de una lista.
#
# ¿Qué hace?
# Recibe una lista de números y devuelve el número más grande.
#
# ¿Cómo lo hace?
# Recorre la lista elemento por elemento, de principio a fin.
# Guarda en una variable el número más grande que ha visto hasta el
# momento; si encuentra uno mayor, lo reemplaza.
# Tiene que revisar TODOS los elementos, porque el más grande podría
# estar en cualquier posición (incluso al final).
#
# Complejidad: O(n) (tiempo lineal)
# Hay un solo ciclo que pasa una vez por cada elemento. Si la lista
# tiene n elementos, se hacen n iteraciones. Si la lista crece al
# doble, las iteraciones también crecen al doble.

def encontrar_numero_mas_grande(lista):
    tamanio_input = len(lista)  # Tamaño de la entrada (n)
    iteraciones = 0             # Contador de operaciones realizadas
    num_mas_grande = 0          # El número más grande visto hasta el momento

    for elemento in lista:
        iteraciones += 1

        if elemento > num_mas_grande:
            num_mas_grande = elemento  # Encontramos uno más grande, lo guardamos

    return tamanio_input, iteraciones, num_mas_grande

# Pruebas: listas de tamaño 6, 7 y 11.
# Esperamos que las iteraciones sean iguales al tamaño: 6, 7 y 11.
lista1 = [5, 9, 3, 5, 6, 0]
lista2 = [33, 6, 1, 98, 3, 1, 3]
lista3 = [1, 2, 333, 4, 5, 64, 6, 7, -8, 9, -10]
lista_pruebas = [lista1, lista2, lista3]

for lista in lista_pruebas:
    resultado_tamanio_input, resultado_iteraciones, resultado_num_mas_grande = encontrar_numero_mas_grande(lista)
    print()
    print("resultado_tamanio_input:", resultado_tamanio_input)
    print("resultado_iteraciones:", resultado_iteraciones)
    print("resultado_num_mas_grande:", resultado_num_mas_grande)
