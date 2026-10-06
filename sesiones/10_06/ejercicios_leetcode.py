# Ejercicios estilo LeetCode
#
# Todos siguen la misma idea: resolver un problema con listas cumpliendo una
# restricción de TIEMPO y/o de MEMORIA.
#
# Recuerda:
#   - Tiempo O(n): recorres la lista una sola vez (o un número fijo de veces).
#     Dos ciclos anidados son O(n²) y NO cumplen.
#   - Memoria O(1): solo puedes usar unas cuantas variables (contadores, índices, etc.).
#     No se vale crear otra lista, un diccionario ni un set del tamaño de la entrada.
#
# Escribe tu solución en cada función (borra el "pass") y ejecuta este archivo:
#     python3 ejercicios_leetcode.py
# Abajo de todo hay pruebas que imprimen "OK" o "FALLA" para cada ejemplo.


# ---------------------------------------------------------------------------
# Ejercicio 1: Missing Number (Número faltante)
# LeetCode 268: https://leetcode.com/problems/missing-number/
#
# Recibes una lista nums con n números DISTINTOS, todos entre 0 y n.
# Como hay n + 1 valores posibles (0, 1, ..., n) y solo n números, falta exactamente uno.
# Regresa el número que falta.
#
# Restricciones: tiempo O(n), memoria O(1).
#
# Ejemplos:
#   nums = [3, 0, 1]                      ->  2     (n = 3: deberían estar 0, 1, 2, 3; falta el 2)
#   nums = [0, 1]                         ->  2     (n = 2: deberían estar 0, 1, 2; falta el 2)
#   nums = [9, 6, 4, 2, 3, 5, 7, 0, 1]    ->  8
#
# Pista: ¿cuánto suman 0 + 1 + 2 + ... + n? ¿Y cuánto suman los números de nums?
# ---------------------------------------------------------------------------

def numero_faltante(nums):
    pass


# ---------------------------------------------------------------------------
# Ejercicio 2: Best Time to Buy and Sell Stock (Mejor momento para comprar y vender)
# LeetCode 121: https://leetcode.com/problems/best-time-to-buy-and-sell-stock/
#
# Recibes una lista precios, donde precios[i] es el precio de una acción el día i.
# Puedes COMPRAR un día y VENDER otro día POSTERIOR (no puedes vender antes de comprar).
# Regresa la mayor ganancia posible. Si no hay forma de ganar, regresa 0.
#
# Restricciones: tiempo O(n), memoria O(1).
#
# Ejemplos:
#   precios = [7, 1, 5, 3, 6, 4]   ->  5     (compras el día 1 a 1, vendes el día 4 a 6: 6 - 1 = 5)
#   precios = [7, 6, 4, 3, 1]      ->  0     (el precio solo baja: mejor no comprar)
#   precios = [2, 4, 1]            ->  2     (compras a 2 y vendes a 4)
#
# Ojo con el último ejemplo: el precio más bajo (1) está al FINAL, así que no sirve
# restar "el máximo menos el mínimo" de toda la lista.
#
# Pista: recorre la lista una vez guardando dos cosas: el precio más bajo que has visto
# HASTA AHORA y la mejor ganancia que has encontrado HASTA AHORA. En cada día pregúntate:
# "si vendiera hoy, habiendo comprado en el día más barato anterior, ¿cuánto ganaría?"
# ---------------------------------------------------------------------------

def mejor_ganancia(precios):
    pass


# ---------------------------------------------------------------------------
# Ejercicio 3: Majority Element (Elemento mayoritario)
# LeetCode 169: https://leetcode.com/problems/majority-element/
#
# Recibes una lista nums de tamaño n. El elemento mayoritario es el que aparece
# MÁS de n / 2 veces (más de la mitad). Siempre existe. Regrésalo.
#
# Restricciones: tiempo O(n), memoria O(1).
#
# Ejemplos:
#   nums = [3, 2, 3]                  ->  3     (aparece 2 de 3 veces)
#   nums = [2, 2, 1, 1, 1, 2, 2]      ->  2     (aparece 4 de 7 veces)
#   nums = [5]                        ->  5
#   nums = [3, 1, 2, 3, 4, 3, 3]      ->  3     (aparece 4 de 7 veces; los demás son 1, 2 y 4)
#
# Pista: imagina una votación. Guarda un "candidato" y un "contador".
# Si el número actual es igual al candidato, suma un voto; si es distinto, resta uno.
# Si el contador llega a 0, el siguiente número se vuelve el nuevo candidato.
# Como el mayoritario tiene más votos que todos los demás juntos, siempre sobrevive.
# ---------------------------------------------------------------------------

def elemento_mayoritario(nums):
    pass


# ---------------------------------------------------------------------------
# Ejercicio 4: Move Zeroes (Mover los ceros al final)
# LeetCode 283: https://leetcode.com/problems/move-zeroes/
#
# Recibes una lista nums. Mueve todos los 0 al final, manteniendo el orden
# de los demás números.
#
# OJO: aquí SÍ debes modificar la lista nums (no crear una nueva).
# La función no regresa nada; las pruebas revisan cómo quedó nums.
#
# Restricciones: tiempo O(n), memoria O(1). No se vale crear otra lista.
#
# Ejemplos:
#   nums = [0, 1, 0, 3, 12]   ->  nums queda como [1, 3, 12, 0, 0]
#   nums = [0]                ->  nums queda como [0]
#   nums = [4, 0, 5, 0, 0, 6] ->  nums queda como [4, 5, 6, 0, 0, 0]
#
# Pista: usa una variable "posicion" que indique dónde va el siguiente número
# distinto de 0. Recorre la lista: cada vez que encuentres un número distinto de 0,
# ponlo en nums[posicion] y avanza posicion. Al final, llena con 0 lo que sobra.
# ---------------------------------------------------------------------------

def mover_ceros(nums):
    pass


# ---------------------------------------------------------------------------
# Ejercicio 5: Two Sum II (Dos números que suman un objetivo, lista ordenada)
# LeetCode 167: https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/
#
# Recibes una lista nums ORDENADA de menor a mayor y un número objetivo.
# Encuentra las dos posiciones cuyos números suman el objetivo y regrésalas
# en una lista [i, j] con i < j. Siempre existe exactamente una respuesta,
# y no puedes usar el mismo elemento dos veces.
#
# (En LeetCode las posiciones empiezan en 1; aquí usamos las de Python, que empiezan en 0.)
#
# Restricciones: tiempo O(n), memoria O(1).
#
# Ejemplos:
#   nums = [2, 7, 11, 15],  objetivo = 9    ->  [0, 1]     (2 + 7 = 9)
#   nums = [2, 3, 4],       objetivo = 6    ->  [0, 2]     (2 + 4 = 6)
#   nums = [-1, 0],         objetivo = -1   ->  [0, 1]     (-1 + 0 = -1)
#
# Pista: pon un índice al inicio (izquierda) y otro al final (derecha).
# Si la suma es muy grande, ¿cuál índice conviene mover? ¿Y si es muy pequeña?
# Aprovecha que la lista está ordenada.
# ---------------------------------------------------------------------------

def dos_sumas_ordenada(nums, objetivo):
    pass


# ---------------------------------------------------------------------------
# Ejercicio 6: Find the Duplicate Number (Encontrar el número repetido)
# LeetCode 287: https://leetcode.com/problems/find-the-duplicate-number/
#
# Recibes una lista nums con n + 1 números enteros, todos entre 1 y n (incluyendo ambos).
# Solo hay UN número repetido, aunque puede aparecer 2 o más veces. Regrésalo.
#
# Restricciones:
#   - NO puedes modificar la lista (no se vale ordenarla ni cambiar sus valores).
#   - Memoria O(1).
#   - Tiempo: mejor que O(n²) (o sea, sin comparar cada par con dos ciclos anidados).
#
# Ejemplos:
#   nums = [1, 3, 4, 2, 2]   ->  2     (n = 4: los números van de 1 a 4)
#   nums = [3, 1, 3, 4, 2]   ->  3
#   nums = [3, 3, 3, 3, 3]   ->  3     (el repetido puede aparecer muchas veces)
#
# Pista: usa búsqueda binaria, pero NO sobre la lista, sino sobre los VALORES posibles
# (de 1 a n). Para un valor "mitad", cuenta cuántos números de nums son <= mitad.
# Si no hubiera repetidos entre 1 y mitad, habría como máximo "mitad" de ellos.
# Si hay MÁS, ¿de qué lado está el repetido?
#
# Reto extra: existe una solución O(n). Busca "Floyd's cycle detection" (la tortuga y la liebre).
# ---------------------------------------------------------------------------

def encontrar_repetido(nums):
    pass


# ---------------------------------------------------------------------------
# Pruebas (no modifiques esta parte)
# ---------------------------------------------------------------------------

def revisar(descripcion, obtenido, esperado):
    if obtenido == esperado:
        print("OK     ", descripcion)
    else:
        print("FALLA  ", descripcion, "-> se esperaba", esperado, "pero se obtuvo", obtenido)

def revisar_mover_ceros(nums, esperado):
    original = list(nums)
    mover_ceros(nums)
    revisar("mover_ceros(" + str(original) + ")", nums, esperado)

print("\nEjercicio 1: numero_faltante")
revisar("numero_faltante([3, 0, 1])", numero_faltante([3, 0, 1]), 2)
revisar("numero_faltante([0, 1])", numero_faltante([0, 1]), 2)
revisar("numero_faltante([9, 6, 4, 2, 3, 5, 7, 0, 1])", numero_faltante([9, 6, 4, 2, 3, 5, 7, 0, 1]), 8)

print("\nEjercicio 2: mejor_ganancia")
revisar("mejor_ganancia([7, 1, 5, 3, 6, 4])", mejor_ganancia([7, 1, 5, 3, 6, 4]), 5)
revisar("mejor_ganancia([7, 6, 4, 3, 1])", mejor_ganancia([7, 6, 4, 3, 1]), 0)
revisar("mejor_ganancia([2, 4, 1])", mejor_ganancia([2, 4, 1]), 2)

print("\nEjercicio 3: elemento_mayoritario")
revisar("elemento_mayoritario([3, 2, 3])", elemento_mayoritario([3, 2, 3]), 3)
revisar("elemento_mayoritario([2, 2, 1, 1, 1, 2, 2])", elemento_mayoritario([2, 2, 1, 1, 1, 2, 2]), 2)
revisar("elemento_mayoritario([5])", elemento_mayoritario([5]), 5)
revisar("elemento_mayoritario([3, 1, 2, 3, 4, 3, 3])", elemento_mayoritario([3, 1, 2, 3, 4, 3, 3]), 3)

print("\nEjercicio 4: mover_ceros")
revisar_mover_ceros([0, 1, 0, 3, 12], [1, 3, 12, 0, 0])
revisar_mover_ceros([0], [0])
revisar_mover_ceros([4, 0, 5, 0, 0, 6], [4, 5, 6, 0, 0, 0])

print("\nEjercicio 5: dos_sumas_ordenada")
revisar("dos_sumas_ordenada([2, 7, 11, 15], 9)", dos_sumas_ordenada([2, 7, 11, 15], 9), [0, 1])
revisar("dos_sumas_ordenada([2, 3, 4], 6)", dos_sumas_ordenada([2, 3, 4], 6), [0, 2])
revisar("dos_sumas_ordenada([-1, 0], -1)", dos_sumas_ordenada([-1, 0], -1), [0, 1])

print("\nEjercicio 6: encontrar_repetido")
revisar("encontrar_repetido([1, 3, 4, 2, 2])", encontrar_repetido([1, 3, 4, 2, 2]), 2)
revisar("encontrar_repetido([3, 1, 3, 4, 2])", encontrar_repetido([3, 1, 3, 4, 2]), 3)
revisar("encontrar_repetido([3, 3, 3, 3, 3])", encontrar_repetido([3, 3, 3, 3, 3]), 3)
