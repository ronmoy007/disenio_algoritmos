# Actividad 1: Variables, tipos de datos, funciones y ciclos

## Objetivo

En esta actividad vas a practicar:

- Crear **variables** de distintos **tipos de datos** (`int`, `float`, `str`, `bool`, `list`)
- Escribir **funciones** que reciben parámetros y **regresan** un valor con `return`
- **Recorrer una lista** con un ciclo `for` o `while`

Tu trabajo se va a calificar automáticamente con `pytest`, así que es muy importante
que sigas **exactamente** los nombres y la estructura de este documento.

---

## Estructura requerida

Crea un archivo llamado **`actividad_1.py`** en la **misma carpeta** que `test_actividad_1.py`:

```
actividad_1/
├── instrucciones_actividad_1.md
├── test_actividad_1.py
└── actividad_1.py        ← este archivo lo creas tú
```

### Reglas

1. El archivo debe llamarse exactamente `actividad_1.py`.
2. Los nombres de las variables y funciones deben ser **exactamente** los que se piden
   (minúsculas, con guion bajo `_`, sin acentos).
3. Las funciones deben **regresar** el resultado con `return`. Si solo usas `print`, la prueba falla.
4. **No uses `input()`** en tu archivo, porque las pruebas se quedarían esperando.
5. Puedes usar `print` para probar tu código, pero no es necesario.

---

## Parte 1: Variables y tipos de datos

Crea las siguientes variables **fuera de cualquier función** (al inicio del archivo).
Tú eliges el valor; lo que se revisa es el **tipo de dato**.

| Variable | Tipo | Ejemplo |
|---|---|---|
| `nombre_materia` | `str` | `"Diseño de algoritmos"` |
| `numero_alumnos` | `int` | `35` |
| `calificacion_minima` | `float` | `6.0` |
| `es_obligatoria` | `bool` | `True` |
| `temas` | `list` con **al menos 3** elementos | `["variables", "funciones", "ciclos"]` |

> **Ojo:** `6` es `int` y `6.0` es `float`. Para Python son tipos distintos.

---

## Parte 2: Funciones

### `area_circulo(radio)`
Recibe el radio de un círculo y regresa su área como **`float`**.
Fórmula: `área = π × radio²`. Puedes usar `math.pi` (escribe `import math` al inicio del archivo).

```python
area_circulo(1)     # 3.14159...
area_circulo(2.5)   # 19.63495...
```

### `perimetro_rectangulo(base, altura)`
Recibe la base y la altura de un rectángulo y regresa su perímetro.
Fórmula: `perímetro = 2 × base + 2 × altura`.

```python
perimetro_rectangulo(3, 5)       # 16
perimetro_rectangulo(2.5, 1.5)   # 8.0
```

### `celsius_a_fahrenheit(celsius)`
Recibe una temperatura en grados Celsius y regresa su equivalente en Fahrenheit como **`float`**.
Fórmula: `fahrenheit = celsius × 9 / 5 + 32`.

```python
celsius_a_fahrenheit(100)   # 212.0
celsius_a_fahrenheit(-40)   # -40.0
```

### `es_par(numero)`
Recibe un número entero y regresa **`True`** si es par o **`False`** si es impar.
Pista: el operador `%` da el residuo de una división. Por ejemplo, `7 % 2` es `1`.

```python
es_par(4)   # True
es_par(7)   # False
```

### `saludar(nombre)`
Recibe un nombre y regresa un **`str`** con el saludo. El formato debe ser exactamente igual,
incluyendo la coma, el espacio y el signo de admiración:

```python
saludar("Ana")   # "Hola, Ana!"
```

---

## Parte 3: Recorrer listas

**Todas las funciones de esta parte deben usar un ciclo `for` o `while`.**
Las pruebas revisan tu código, y **no puedes usar** estos atajos de Python:
`sum()`, `max()`, `min()`, `sorted()`, `filter()` ni `.count()`.
Sí puedes usar `len()` y `.append()`.

### `sumar_lista(numeros)`
Recibe una lista de números y regresa la suma de todos ellos.
Si la lista está vacía, regresa `0`.

```python
sumar_lista([1, 2, 3, 4])   # 10
sumar_lista([])             # 0
```

### `promedio(numeros)`
Recibe una lista de números y regresa su promedio como **`float`**.

```python
promedio([7, 8, 10, 9])   # 8.5
```

### `numero_mayor(numeros)`
Recibe una lista de números y regresa el número más grande.
Tu función también debe funcionar si **todos los números son negativos**.

```python
numero_mayor([3, 17, 8, 2])   # 17
numero_mayor([-5, -3, -9])    # -3
```

### `contar_letras_a(lista_letras)`
Recibe una lista de letras y regresa **cuántas veces aparece la letra `"A"`**.
Solo cuenta la `"A"` **mayúscula**; la `"a"` minúscula no cuenta.

```python
letras = ["A", "B", "A", "C", "D", "A", "E", "A", "F", "G", "A", "B"]
contar_letras_a(letras)            # 5
contar_letras_a(["a", "A", "a"])   # 1
```

### `contar_pares(numeros)`
Recibe una lista de números enteros y regresa **cuántos** son pares.

```python
contar_pares([1, 2, 3, 4, 5, 6])   # 3
contar_pares([1, 3, 5])            # 0
```

### `filtrar_positivos(numeros)`
Recibe una lista de números y regresa una **nueva lista** solo con los números mayores que 0,
en el mismo orden en que aparecen. El `0` **no** es positivo.

```python
filtrar_positivos([4, -1, 0, 7, -3, 2])   # [4, 7, 2]
```

---

## Cómo revisar tu trabajo

1. Crea un entorno virtual e instala pytest (solo la primera vez).
   Abre una terminal en la **carpeta principal del repositorio** y ejecuta:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate        # En Windows: .venv\Scripts\activate
   python3 -m pip install pytest
   ```
   > Si al usar `pip install pytest` directamente te aparece el error
   > `externally-managed-environment`, es por esto: tu sistema no permite instalar
   > paquetes de forma global y hay que usar un entorno virtual.
2. Cada vez que abras una terminal nueva, activa el entorno virtual
   (verás `(.venv)` al inicio de la línea), entra a la carpeta `actividades` y corre las pruebas:
   ```bash
   source .venv/bin/activate        # En Windows: .venv\Scripts\activate
   cd actividades
   pytest test_actividad_1.py -v
   ```
3. Cada prueba aparece como `PASSED` (correcta) o `FAILED` (incorrecta).
   Si una prueba falla, lee el mensaje de error: te dice qué se esperaba y qué regresó tu función.

Al final verás un resumen como este:

```
======================== 22 passed in 0.05s ========================
```

¡Tu objetivo es que **todas** las pruebas pasen!

