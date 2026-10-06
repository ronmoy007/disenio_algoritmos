# Soluciones NO válidas de ejercicios_leetcode.py
#
# Todas estas soluciones FUNCIONAN: dan el resultado correcto.
# Pero NINGUNA cumple las restricciones del ejercicio, porque:
#   - usan memoria extra O(n): una lista auxiliar, un set o un diccionario
#     que crece con el tamaño de la entrada, o
#   - tardan O(n²): un ciclo dentro de otro ciclo, o
#   - modifican la lista cuando no se vale (por ejemplo, ordenándola).
#
# Sirven para ver que el problema SÍ tiene solución, y para entender
# por qué el reto está en resolverlo con las restricciones.
#
# ---------------------------------------------------------------------------
# Dos herramientas de Python que usamos aquí
# ---------------------------------------------------------------------------
#
# set (conjunto): guarda valores SIN repetir. Preguntar "¿está x?" es muy rápido.
#     vistos = set()          # set vacío
#     vistos.add(5)           # agrega el 5
#     5 in vistos             # True
#     7 in vistos             # False
#
# dict (diccionario): guarda parejas clave -> valor.
#     conteo = {}             # diccionario vacío
#     conteo[3] = 1           # la clave 3 tiene el valor 1
#     conteo[3] = conteo[3] + 1
#     conteo[3]               # 2
#     3 in conteo             # True  (pregunta por las CLAVES)
#
# Ambos ocupan memoria O(n) si guardamos en ellos los n elementos de la lista.


# ---------------------------------------------------------------------------
# Ejercicio 1: Missing Number (número faltante)
# Restricciones: tiempo O(n), memoria O(1).
# ---------------------------------------------------------------------------

# No válida A: buscar cada valor de 0 a n en la lista.
# Tiempo O(n²): "valor in nums" recorre toda la lista, y lo hacemos n + 1 veces.
def numero_faltante_dos_ciclos(nums):
    for valor in range(len(nums) + 1):
        if valor not in nums:
            return valor

# No válida B: guardar los números en un set.
# Tiempo O(n), pero memoria O(n) por el set.
def numero_faltante_con_set(nums):
    vistos = set()
    for numero in nums:
        vistos.add(numero)

    for valor in range(len(nums) + 1):
        if valor not in vistos:
            return valor


# ---------------------------------------------------------------------------
# Ejercicio 2: Best Time to Buy and Sell Stock (mejor ganancia)
# Restricciones: tiempo O(n), memoria O(1).
# ---------------------------------------------------------------------------

# No válida: probar todas las parejas (día de compra, día de venta posterior).
# Memoria O(1), pero tiempo O(n²) por los dos ciclos anidados.
def mejor_ganancia_dos_ciclos(precios):
    mejor = 0

    for compra in range(len(precios)):
        for venta in range(compra + 1, len(precios)):  # Solo días DESPUÉS de la compra
            ganancia = precios[venta] - precios[compra]
            if ganancia > mejor:
                mejor = ganancia

    return mejor

# Ojo, esta otra NI SIQUIERA funciona (aunque es O(n) y O(1)):
#     return max(precios) - min(precios)
# Con [2, 4, 1] daría 4 - 1 = 3, pero el 1 está DESPUÉS del 4: no se puede
# comprar a 1 y vender a 4. La respuesta correcta es 2.


# ---------------------------------------------------------------------------
# Ejercicio 3: Majority Element (elemento mayoritario)
# Restricciones: tiempo O(n), memoria O(1).
# ---------------------------------------------------------------------------

# No válida A: contar cuántas veces aparece cada número con un diccionario.
# Tiempo O(n), pero memoria O(n) por el diccionario.
def elemento_mayoritario_con_diccionario(nums):
    conteo = {}

    for numero in nums:
        if numero in conteo:
            conteo[numero] = conteo[numero] + 1
        else:
            conteo[numero] = 1

    for numero in conteo:
        if conteo[numero] > len(nums) / 2:
            return numero

# No válida B: ordenar y tomar el elemento de en medio.
# Si un número ocupa más de la mitad de la lista, al ordenarla siempre cae en el centro:
#     [2, 2, 1, 1, 1, 2, 2]  ->  ordenada: [1, 1, 1, 2, 2, 2, 2]  ->  centro: 2
# Tiempo O(n log n) (ordenar) y memoria O(n) (sorted crea una lista nueva).
def elemento_mayoritario_ordenando(nums):
    ordenada = sorted(nums)
    return ordenada[len(ordenada) // 2]


# ---------------------------------------------------------------------------
# Ejercicio 4: Move Zeroes (mover los ceros al final)
# Restricciones: modificar nums, tiempo O(n), memoria O(1).
# ---------------------------------------------------------------------------

# No válida A: armar una lista auxiliar sin ceros y luego copiarla en nums.
# Tiempo O(n), pero memoria O(n) por la lista auxiliar.
def mover_ceros_lista_auxiliar(nums):
    sin_ceros = []
    for numero in nums:
        if numero != 0:
            sin_ceros.append(numero)

    for i in range(len(nums)):
        if i < len(sin_ceros):
            nums[i] = sin_ceros[i]
        else:
            nums[i] = 0

# No válida B: cada vez que hay un 0, quitarlo y ponerlo al final.
# Memoria O(1), pero tiempo O(n²): nums.remove(0) recorre la lista para
# encontrar el 0 y recorre los elementos para "recorrerlos" un lugar.
def mover_ceros_remove(nums):
    cantidad_ceros = 0
    for numero in nums:
        if numero == 0:
            cantidad_ceros += 1

    for _ in range(cantidad_ceros):
        nums.remove(0)    # Quita el primer 0 que encuentre
        nums.append(0)    # Y lo pone al final


# ---------------------------------------------------------------------------
# Ejercicio 5: Two Sum II (dos números que suman un objetivo, lista ordenada)
# Restricciones: tiempo O(n), memoria O(1).
# ---------------------------------------------------------------------------

# No válida A: probar todas las parejas.
# Memoria O(1), pero tiempo O(n²).
def dos_sumas_dos_ciclos(nums, objetivo):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == objetivo:
                return [i, j]

# No válida B: guardar en un diccionario los números ya vistos y su posición.
# Para cada número, el que necesitamos es "objetivo - numero". Si ya lo vimos, terminamos.
# Tiempo O(n), pero memoria O(n) por el diccionario. Además no aprovecha
# que la lista está ordenada. (Esta es la solución del "Two Sum" original, LeetCode 1.)
def dos_sumas_con_diccionario(nums, objetivo):
    posiciones = {}  # numero -> posición donde lo vimos

    for i in range(len(nums)):
        necesito = objetivo - nums[i]
        if necesito in posiciones:
            return [posiciones[necesito], i]
        posiciones[nums[i]] = i


# ---------------------------------------------------------------------------
# Ejercicio 6: Find the Duplicate Number (encontrar el número repetido)
# Restricciones: NO modificar nums, memoria O(1), tiempo mejor que O(n²).
# ---------------------------------------------------------------------------

# No válida A: comparar cada par.
# No modifica nums y usa memoria O(1), pero tiempo O(n²).
def encontrar_repetido_dos_ciclos(nums):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] == nums[j]:
                return nums[i]

# No válida B: guardar en un set los números que ya vimos.
# Tiempo O(n), pero memoria O(n) por el set.
def encontrar_repetido_con_set(nums):
    vistos = set()
    for numero in nums:
        if numero in vistos:
            return numero
        vistos.add(numero)

# No válida C: ordenar la lista; los repetidos quedan juntos.
#     [3, 1, 3, 4, 2]  ->  ordenada: [1, 2, 3, 3, 4]  ->  nums[2] == nums[3]
# Memoria O(1) y tiempo O(n log n), pero nums.sort() MODIFICA la lista original.
# (Con sorted(nums) no la modificaríamos, pero entonces usaríamos memoria O(n).)
def encontrar_repetido_ordenando(nums):
    nums.sort()
    for i in range(len(nums) - 1):
        if nums[i] == nums[i + 1]:
            return nums[i]


# ---------------------------------------------------------------------------
# Pruebas: todas las soluciones dan el resultado correcto...
# aunque ninguna cumple las restricciones.
# ---------------------------------------------------------------------------

def revisar(descripcion, obtenido, esperado):
    if obtenido == esperado:
        print("OK     ", descripcion)
    else:
        print("FALLA  ", descripcion, "-> se esperaba", esperado, "pero se obtuvo", obtenido)

def revisar_mover_ceros(funcion, nums, esperado):
    original = list(nums)
    funcion(nums)
    revisar(funcion.__name__ + "(" + str(original) + ")", nums, esperado)

print("\nEjercicio 1: numero_faltante")
for funcion in [numero_faltante_dos_ciclos, numero_faltante_con_set]:
    revisar(funcion.__name__ + "([3, 0, 1])", funcion([3, 0, 1]), 2)
    revisar(funcion.__name__ + "([9, 6, 4, 2, 3, 5, 7, 0, 1])", funcion([9, 6, 4, 2, 3, 5, 7, 0, 1]), 8)

print("\nEjercicio 2: mejor_ganancia")
revisar("mejor_ganancia_dos_ciclos([7, 1, 5, 3, 6, 4])", mejor_ganancia_dos_ciclos([7, 1, 5, 3, 6, 4]), 5)
revisar("mejor_ganancia_dos_ciclos([2, 4, 1])", mejor_ganancia_dos_ciclos([2, 4, 1]), 2)

print("\nEjercicio 3: elemento_mayoritario")
for funcion in [elemento_mayoritario_con_diccionario, elemento_mayoritario_ordenando]:
    revisar(funcion.__name__ + "([2, 2, 1, 1, 1, 2, 2])", funcion([2, 2, 1, 1, 1, 2, 2]), 2)
    revisar(funcion.__name__ + "([3, 1, 2, 3, 4, 3, 3])", funcion([3, 1, 2, 3, 4, 3, 3]), 3)

print("\nEjercicio 4: mover_ceros")
for funcion in [mover_ceros_lista_auxiliar, mover_ceros_remove]:
    revisar_mover_ceros(funcion, [0, 1, 0, 3, 12], [1, 3, 12, 0, 0])
    revisar_mover_ceros(funcion, [4, 0, 5, 0, 0, 6], [4, 5, 6, 0, 0, 0])

print("\nEjercicio 5: dos_sumas_ordenada")
for funcion in [dos_sumas_dos_ciclos, dos_sumas_con_diccionario]:
    revisar(funcion.__name__ + "([2, 7, 11, 15], 9)", funcion([2, 7, 11, 15], 9), [0, 1])
    revisar(funcion.__name__ + "([2, 3, 4], 6)", funcion([2, 3, 4], 6), [0, 2])

print("\nEjercicio 6: encontrar_repetido")
for funcion in [encontrar_repetido_dos_ciclos, encontrar_repetido_con_set, encontrar_repetido_ordenando]:
    revisar(funcion.__name__ + "([1, 3, 4, 2, 2])", funcion([1, 3, 4, 2, 2]), 2)
    revisar(funcion.__name__ + "([3, 1, 3, 4, 2])", funcion([3, 1, 3, 4, 2]), 3)

# Prueba de que ordenar MODIFICA la lista original:
lista = [3, 1, 3, 4, 2]
print("\nAntes de encontrar_repetido_ordenando:  ", lista)
encontrar_repetido_ordenando(lista)
print("Después de encontrar_repetido_ordenando:", lista, " <- ¡la lista original cambió!")
