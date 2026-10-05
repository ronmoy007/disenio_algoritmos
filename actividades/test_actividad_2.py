# Pruebas automáticas de la Actividad 2.
#
# Temas que se evalúan:
#   - Escribir funciones recursivas (que se llaman a sí mismas)
#   - Identificar el caso base y el caso recursivo de un problema
#
# El alumno debe crear el archivo actividad_2.py en esta misma carpeta.
# Para correr las pruebas:
#     pytest test_actividad_2.py -v

import ast
import inspect

import pytest

import actividad_2


def obtener(nombre):
    # Busca una función en actividad_2.py.
    # Si no existe, la prueba falla con un mensaje claro.
    if not hasattr(actividad_2, nombre):
        pytest.fail(f"No se encontró '{nombre}' en actividad_2.py. Revisa que el nombre esté escrito exactamente igual.")
    return getattr(actividad_2, nombre)


# ---------------------------------------------------------------------------
# Parte 1: Recursión con números
# ---------------------------------------------------------------------------

def test_factorial():
    factorial = obtener("factorial")
    assert factorial(5) is not None, "factorial regresó None. ¿Olvidaste usar return?"
    assert factorial(0) == 1, "Por definición, 0! = 1. Revisa tu caso base"
    assert factorial(1) == 1
    assert factorial(4) == 24
    assert factorial(5) == 120
    assert factorial(10) == 3628800


def test_potencia():
    potencia = obtener("potencia")
    assert potencia(2, 3) is not None, "potencia regresó None. ¿Olvidaste usar return?"
    assert potencia(7, 0) == 1, "Cualquier número elevado a 0 es 1. Revisa tu caso base"
    assert potencia(5, 1) == 5
    assert potencia(2, 3) == 8
    assert potencia(3, 4) == 81
    assert potencia(2, 10) == 1024


# ---------------------------------------------------------------------------
# Parte 2: Fibonacci
# ---------------------------------------------------------------------------

def test_fibonacci():
    fibonacci = obtener("fibonacci")
    assert fibonacci(5) is not None, "fibonacci regresó None. ¿Olvidaste usar return?"
    assert fibonacci(0) == 0, "fibonacci(0) debe ser 0. Revisa tus casos base"
    assert fibonacci(1) == 1, "fibonacci(1) debe ser 1. Revisa tus casos base"
    assert fibonacci(2) == 1
    assert fibonacci(6) == 8
    assert fibonacci(10) == 55


def test_fibonacci_primeros_diez():
    fibonacci = obtener("fibonacci")
    serie = []
    for n in range(10):
        serie.append(fibonacci(n))
    assert serie == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]


# ---------------------------------------------------------------------------
# Parte 3: Conjetura de Collatz
# ---------------------------------------------------------------------------

def test_pasos_collatz():
    pasos_collatz = obtener("pasos_collatz")
    assert pasos_collatz(6) is not None, "pasos_collatz regresó None. ¿Olvidaste usar return?"
    assert pasos_collatz(1) == 0, "Si empezamos en 1 no hace falta dar ningún paso. Revisa tu caso base"
    assert pasos_collatz(2) == 1
    assert pasos_collatz(6) == 8
    assert pasos_collatz(7) == 16
    assert pasos_collatz(27) == 111


def test_secuencia_collatz():
    secuencia_collatz = obtener("secuencia_collatz")
    assert type(secuencia_collatz(6)) is list, "secuencia_collatz debe regresar una list"
    assert secuencia_collatz(1) == [1], "La secuencia que empieza en 1 es solo [1]. Revisa tu caso base"
    assert secuencia_collatz(6) == [6, 3, 10, 5, 16, 8, 4, 2, 1]
    assert secuencia_collatz(5) == [5, 16, 8, 4, 2, 1]
    assert secuencia_collatz(16) == [16, 8, 4, 2, 1]


def test_secuencia_collatz_solo_enteros():
    secuencia_collatz = obtener("secuencia_collatz")
    for numero in secuencia_collatz(6):
        assert type(numero) is int, "Todos los números de la secuencia deben ser int. ¿Usaste / en lugar de //?"


# ---------------------------------------------------------------------------
# Parte 4: Revisar que las funciones sean recursivas
# El objetivo de la actividad es practicar la recursión, así que se revisa
# el código de cada función:
#   - Debe llamarse a sí misma.
#   - No debe tener ciclos (for o while).
#   - No debe usar atajos de Python que ya resuelven el problema.
# ---------------------------------------------------------------------------

FUNCIONES_RECURSIVAS = [
    "factorial",
    "potencia",
    "fibonacci",
    "pasos_collatz",
    "secuencia_collatz",
]

FUNCIONES_PROHIBIDAS = ["pow"]


@pytest.mark.parametrize("nombre_funcion", FUNCIONES_RECURSIVAS)
def test_funcion_es_recursiva(nombre_funcion):
    funcion = obtener(nombre_funcion)
    codigo = inspect.getsource(funcion)
    arbol = ast.parse(codigo)

    se_llama_a_si_misma = False
    tiene_ciclo = False
    atajos_usados = []

    for nodo in ast.walk(arbol):
        if isinstance(nodo, (ast.For, ast.While, ast.ListComp, ast.GeneratorExp)):
            tiene_ciclo = True

        if isinstance(nodo, ast.BinOp) and isinstance(nodo.op, ast.Pow):
            atajos_usados.append("el operador **")

        if isinstance(nodo, ast.Call):
            if isinstance(nodo.func, ast.Name) and nodo.func.id == nombre_funcion:
                se_llama_a_si_misma = True
            if isinstance(nodo.func, ast.Name) and nodo.func.id in FUNCIONES_PROHIBIDAS:
                atajos_usados.append(nodo.func.id + "()")
            if isinstance(nodo.func, ast.Attribute) and nodo.func.attr in ("factorial", "pow"):
                atajos_usados.append("math." + nodo.func.attr + "()")

    assert se_llama_a_si_misma, f"{nombre_funcion} debe ser recursiva: dentro de ella debes llamar a {nombre_funcion}(...)"
    assert not tiene_ciclo, f"{nombre_funcion} no debe usar ciclos (for o while); resuélvela con recursión"
    assert atajos_usados == [], f"{nombre_funcion} no debe usar {', '.join(atajos_usados)}; resuélvela con recursión"
