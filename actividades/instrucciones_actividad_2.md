# Actividad 2: Recursividad

## Objetivo

En esta actividad vas a practicar:

- Escribir **funciones recursivas**, es decir, funciones que **se llaman a sí mismas**
- Encontrar el **caso base** y el **caso recursivo** de un problema

Tu trabajo se va a calificar automáticamente con `pytest`, así que es muy importante
que sigas **exactamente** los nombres y la estructura de este documento.

---

## Estructura requerida

Crea un archivo llamado **`actividad_2.py`** en la **misma carpeta** que `test_actividad_2.py`:

```
actividades/
├── instrucciones_actividad_2.md
├── test_actividad_2.py
└── actividad_2.py        ← este archivo lo creas tú
```

### Reglas

1. El archivo debe llamarse exactamente `actividad_2.py`.
2. Los nombres de las funciones deben ser **exactamente** los que se piden
   (minúsculas, con guion bajo `_`, sin acentos).
3. Las funciones deben **regresar** el resultado con `return`. Si solo usas `print`, la prueba falla.
4. **Todas las funciones deben ser recursivas**: dentro de cada una debes llamar a la misma función.
5. **No puedes usar ciclos** (`for` ni `while`) dentro de las funciones que se califican.
6. **No puedes usar atajos de Python** que ya resuelven el problema:
   `pow()`, el operador `**` ni `math.factorial()`.
7. **No uses `input()`** en tu archivo, porque las pruebas se quedarían esperando.
8. **Sí puedes** crear funciones auxiliares (de ayuda) si te sirven.

---

## Antes de empezar: ¿qué es la recursión?

Una función es **recursiva** cuando **se llama a sí misma** para resolver una versión
**más pequeña** del mismo problema.

Toda función recursiva tiene **dos partes**:

1. **Caso base:** el problema más pequeño posible, cuya respuesta ya conocemos **sin hacer
   cuentas**. Aquí la función **regresa** un valor y **no** se vuelve a llamar.
2. **Caso recursivo:** la función se llama a sí misma con un problema **un poco más pequeño**
   y usa esa respuesta para construir la suya.

> **Sin caso base, la función se llamaría a sí misma para siempre.**
> Python la detiene con el error `RecursionError: maximum recursion depth exceeded`.
> Si ves ese error, revisa tu caso base.

### La receta: 3 preguntas para escribir cualquier función recursiva

Cada vez que te enfrentes a un ejercicio de esta actividad, contesta estas 3 preguntas
**en papel** antes de escribir código:

| # | Pregunta | Para qué sirve |
|---|---|---|
| 1 | ¿Cuál es el caso **más pequeño** del problema y cuál es su respuesta? | Ese es tu **caso base** |
| 2 | Si **alguien más** ya me diera la respuesta del problema un poco más pequeño, ¿cómo la uso para obtener la mía? | Ese es tu **caso recursivo** |
| 3 | ¿Cada llamada se **acerca** al caso base? | Así te aseguras de que la función **termina** |

La pregunta 2 es la más importante. El truco de la recursión es **confiar** en que la
llamada a la función con el problema más pequeño ya funciona, y solo pensar en **un paso**.

---

## Ejemplo resuelto: `suma_hasta(n)` (no se califica)

**Problema:** sumar todos los números enteros desde `0` hasta `n`.

```python
suma_hasta(4)   # 0 + 1 + 2 + 3 + 4 = 10
```

### Paso 1: contestar las 3 preguntas

1. **¿Caso más pequeño?** `suma_hasta(0)`. La suma de 0 hasta 0 es **0**. No hay que calcular nada.
2. **¿Cómo uso la respuesta del problema más pequeño?** Observa:

   ```
   suma_hasta(4) = 4 + 3 + 2 + 1 + 0
                 = 4 + (3 + 2 + 1 + 0)
                 = 4 + suma_hasta(3)
   ```

   Es decir: **`suma_hasta(n) = n + suma_hasta(n - 1)`**.
3. **¿Me acerco al caso base?** Sí: cada llamada usa `n - 1`, así que `n` baja
   (4, 3, 2, 1, 0) hasta llegar a `0`.

### Paso 2: escribir el código

```python
def suma_hasta(n):
    # Caso base: la suma de 0 a 0 es 0
    if n == 0:
        return 0

    # Caso recursivo: n + (la suma de todos los anteriores)
    return n + suma_hasta(n - 1)
```

### Paso 3: seguir la ejecución paso a paso

Cada **columna** es un **llamado** a la función. Cuando la función se llama a sí misma,
nos movemos una columna a la derecha. Un llamado **se queda esperando** hasta que el
llamado de su derecha le regrese su resultado.

```
llamado 1           | llamado 2           | llamado 3           | llamado 4           | llamado 5
-------------------------------------------------------------------------------------------------------
suma_hasta(4)       |                     |                     |                     |
4 + suma_hasta(3)   | suma_hasta(3)       |                     |                     |
    (esperando...)  | 3 + suma_hasta(2)   | suma_hasta(2)       |                     |
                    |     (esperando...)  | 2 + suma_hasta(1)   | suma_hasta(1)       |
                    |                     |     (esperando...)  | 1 + suma_hasta(0)   | suma_hasta(0)
                    |                     |                     |     (esperando...)  | caso base: regresa 0
                    |                     |                     | 1 + 0 = 1           |
                    |                     |                     | regresa 1           |
                    |                     | 2 + 1 = 3           |                     |
                    |                     | regresa 3           |                     |
                    | 3 + 3 = 6           |                     |                     |
                    | regresa 6           |                     |                     |
4 + 6 = 10          |                     |                     |                     |
regresa 10          |                     |                     |                     |
```

Fíjate en las dos fases:

- **De bajada** (izquierda → derecha): la función se va llamando con problemas cada vez más pequeños.
  Todavía **nadie** ha terminado su cuenta.
- **De subida** (derecha → izquierda): el caso base regresa `0` y cada llamado termina su
  suma con el resultado que le llegó.

**Todos los ejercicios de esta actividad se resuelven con la misma idea.**

---

## Parte 1: Recursión con números

### `factorial(n)`

El **factorial** de un número `n` (se escribe `n!`) es la multiplicación de todos los
enteros desde `1` hasta `n`. Por definición, **`0! = 1`**.

```
5! = 5 × 4 × 3 × 2 × 1 = 120
```

```python
factorial(0)    # 1
factorial(1)    # 1
factorial(4)    # 24
factorial(5)    # 120
factorial(10)   # 3628800
```

**Cómo abordarlo:** es igual que `suma_hasta`, pero multiplicando en lugar de sumar.

```
5! = 5 × 4 × 3 × 2 × 1
   = 5 × (4 × 3 × 2 × 1)
   = 5 × 4!
```

- **Caso base:** `factorial(0)` regresa `1`.
- **Caso recursivo:** `factorial(n)` es `n` multiplicado por `factorial(n - 1)`.

> **Ojo:** el caso base del factorial es `1`, no `0`. Si regresaras `0`, toda la multiplicación
> daría `0`.

---

### `potencia(base, exponente)`

Recibe una `base` y un `exponente` (entero, `0` o mayor) y regresa `base` elevado a `exponente`.
**No puedes usar `**` ni `pow()`**; la idea es construir la potencia con multiplicaciones.

```python
potencia(2, 3)    # 2 × 2 × 2 = 8
potencia(3, 4)    # 3 × 3 × 3 × 3 = 81
potencia(5, 1)    # 5
potencia(7, 0)    # 1   (cualquier número elevado a 0 es 1)
potencia(2, 10)   # 1024
```

**Cómo abordarlo:**

```
2³ = 2 × 2 × 2
   = 2 × (2 × 2)
   = 2 × 2²
```

- **Caso base:** cuando el `exponente` es `0`, el resultado es `1`.
- **Caso recursivo:** `potencia(base, exponente)` es `base` multiplicado por
  `potencia(base, exponente - 1)`.

> **Fíjate:** esta función recibe **dos** parámetros, pero solo **uno** se hace más pequeño
> en cada llamada. La `base` se queda igual; el `exponente` es el que baja hasta `0`.

---

## Parte 2: Fibonacci

### `fibonacci(n)`

La **serie de Fibonacci** empieza con `0` y `1`, y cada número siguiente es la **suma de los
dos anteriores**:

```
posición n:      0   1   2   3   4   5   6   7   8   9   10
fibonacci(n):    0   1   1   2   3   5   8  13  21  34   55
                         ↑
                       0 + 1 = 1
                             ↑
                           1 + 1 = 2
                                 ↑
                               1 + 2 = 3
```

La función recibe una **posición** `n` y regresa el número de Fibonacci que está en esa posición.

```python
fibonacci(0)    # 0
fibonacci(1)    # 1
fibonacci(2)    # 1   (0 + 1)
fibonacci(6)    # 8   (3 + 5)
fibonacci(10)   # 55  (21 + 34)
```

**Cómo abordarlo:** este ejercicio es diferente a los anteriores en dos cosas.

1. Tiene **dos casos base**: `fibonacci(0)` es `0` y `fibonacci(1)` es `1`.
   (Necesitas los dos, porque para calcular cualquier número hacen falta **dos** anteriores.)
2. El caso recursivo hace **dos llamadas** a la función:

```
fibonacci(n) = fibonacci(n - 1) + fibonacci(n - 2)
```

Así se ve el "árbol" de llamadas de `fibonacci(4)`:

```
                      fibonacci(4)
                     /            \
            fibonacci(3)    +    fibonacci(2)
            /         \           /         \
    fibonacci(2) + fibonacci(1)  fibonacci(1) + fibonacci(0)
     /       \          |             |             |
fib(1) + fib(0)         1             1             0
  |        |
  1        0

fibonacci(4) = 3
```

> **Para pensar (no se califica):** observa que `fibonacci(2)` se calcula **dos veces** en el
> árbol. ¿Qué pasa con el número de llamadas si pides `fibonacci(30)`? ¿Cuál crees que es la
> complejidad (Big O) de este algoritmo? Prueba `fibonacci(35)` en tu computadora y mide cuánto tarda.

---

## Parte 3: Conjetura de Collatz

La **conjetura de Collatz** es un problema famoso de las matemáticas. Empieza con cualquier
número entero positivo `n` y aplica esta regla una y otra vez:

- Si `n` es **par**, divídelo entre 2: el siguiente es `n // 2`.
- Si `n` es **impar**, multiplícalo por 3 y súmale 1: el siguiente es `3 * n + 1`.

La conjetura dice que, **sin importar con qué número empieces, siempre llegas al 1**.
Nadie ha podido demostrar que sea cierto para todos los números... ¡pero tampoco nadie ha
encontrado uno que no llegue al 1!

**Ejemplo empezando en 6:**

```
paso    número   ¿par o impar?   siguiente
  1       6         par          6 // 2     = 3
  2       3        impar         3 * 3 + 1  = 10
  3      10         par          10 // 2    = 5
  4       5        impar         5 * 3 + 1  = 16
  5      16         par          16 // 2    = 8
  6       8         par          8 // 2     = 4
  7       4         par          4 // 2     = 2
  8       2         par          2 // 2     = 1
          1     ← llegamos: se termina
```

Secuencia: `6 → 3 → 10 → 5 → 16 → 8 → 4 → 2 → 1`, en **8 pasos**.

> **Consejo:** las dos funciones de esta parte necesitan calcular "el siguiente número".
> Puedes escribir una **función auxiliar** `siguiente_collatz(n)` (no tiene que ser recursiva)
> que regrese el siguiente número según la regla, y usarla en las dos.
>
> **Ojo:** usa `//`, no `/`. `6 / 2` da `3.0` (un `float`) y la prueba espera `3` (un `int`).

### `pasos_collatz(n)`

Recibe un número entero positivo `n` y regresa **cuántos pasos** se necesitan para llegar a `1`.

```python
pasos_collatz(1)    # 0    (ya estamos en 1, no hay que dar ningún paso)
pasos_collatz(2)    # 1    (2 → 1)
pasos_collatz(6)    # 8    (6 → 3 → 10 → 5 → 16 → 8 → 4 → 2 → 1)
pasos_collatz(7)    # 16
pasos_collatz(27)   # 111  (¡el 27 sube hasta 9232 antes de bajar!)
```

**Cómo abordarlo:** si ya sabes cuántos pasos le faltan al **siguiente** número,
solo tienes que sumar **1** (el paso que acabas de dar):

```
pasos_collatz(6) = 1 + pasos_collatz(3)
                 = 1 + 1 + pasos_collatz(10)
                 = 1 + 1 + 1 + pasos_collatz(5)
                 ...
                 = 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + pasos_collatz(1)
                 = 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 0
                 = 8
```

- **Caso base:** si `n` es `1`, regresa `0`.
- **Caso recursivo:** `1 +` los pasos que le faltan al siguiente número de la secuencia.

### `secuencia_collatz(n)`

Recibe un número entero positivo `n` y regresa una **lista** con todos los números de la
secuencia, desde `n` hasta `1` (incluyendo ambos).

```python
secuencia_collatz(1)    # [1]
secuencia_collatz(6)    # [6, 3, 10, 5, 16, 8, 4, 2, 1]
secuencia_collatz(5)    # [5, 16, 8, 4, 2, 1]
secuencia_collatz(16)   # [16, 8, 4, 2, 1]
```

**Cómo abordarlo:** es la misma idea que `pasos_collatz`, pero en lugar de **sumar números**,
**unimos listas**. En Python, el operador `+` entre dos listas las pega:

```python
[6] + [3, 10, 5]   # [6, 3, 10, 5]
```

Entonces:

```
secuencia_collatz(4) = [4] + secuencia_collatz(2)
                     = [4] + [2] + secuencia_collatz(1)
                     = [4] + [2] + [1]                  ← caso base
                     = [4, 2, 1]
```

- **Caso base:** si `n` es `1`, regresa la lista `[1]`.
- **Caso recursivo:** la lista `[n]` unida con la secuencia del siguiente número.

---

## Errores comunes

| Lo que ves | Lo que probablemente pasó |
|---|---|
| `RecursionError: maximum recursion depth exceeded` | Falta el caso base, o la llamada recursiva **no se acerca** a él (por ejemplo, llamaste `factorial(n)` en lugar de `factorial(n - 1)`). |
| La prueba dice que tu función regresó `None` | Escribiste `factorial(n - 1)` pero olvidaste el `return` en el caso recursivo: `return n * factorial(n - 1)`. |
| `factorial` siempre regresa `0` | Tu caso base regresa `0` en lugar de `1`. |
| Te sale `3.0` en lugar de `3` | Usaste `/` en lugar de `//`. |
| `"... debe ser recursiva: dentro de ella debes llamar a ..."` | Tu función da el resultado correcto, pero **no se llama a sí misma**. |
| `"... no debe usar ciclos ..."` | Usaste `for` o `while` dentro de la función. Esta actividad es de recursión. |

---

## Cómo revisar tu trabajo

1. Si todavía no tienes el entorno virtual, sigue el paso 1 de las instrucciones de la Actividad 1.
2. Activa el entorno virtual (verás `(.venv)` al inicio de la línea), entra a la carpeta
   `actividades` y corre las pruebas:
   ```bash
   source .venv/bin/activate        # En Windows: .venv\Scripts\activate
   cd actividades
   pytest test_actividad_2.py -v
   ```
3. Cada prueba aparece como `PASSED` (correcta) o `FAILED` (incorrecta).
   Si una prueba falla, lee el mensaje de error: te dice qué se esperaba y qué regresó tu función.

Las pruebas revisan **dos cosas** de cada función:

- Que regrese el **resultado correcto** (`test_factorial`, `test_fibonacci`, ...).
- Que sea **recursiva** y no use ciclos ni atajos (`test_funcion_es_recursiva[factorial]`, ...).

Al final verás un resumen como este:

```
======================== 12 passed in 0.05s ========================
```

¡Tu objetivo es que **todas** las pruebas pasen!
