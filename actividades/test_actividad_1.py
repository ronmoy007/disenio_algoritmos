# Pruebas automáticas de la Actividad 1.
#
# Temas que se evalúan:
#   - Variables y tipos de datos (int, float, str, bool, list)
#   - Escribir funciones que reciben parámetros y regresan un valor
#   - Iterar (recorrer) una lista de elementos con un ciclo
#
# El alumno debe crear el archivo actividad_1.py en esta misma carpeta.
# Para correr las pruebas:
#     pytest test_actividad_1.py -v

import ast
import inspect

import pytest

import actividad_1


def obtener(nombre):
    # Busca una variable o función en actividad_1.py.
    # Si no existe, la prueba falla con un mensaje claro.
    if not hasattr(actividad_1, nombre):
        pytest.fail(f"No se encontró '{nombre}' en actividad_1.py. Revisa que el nombre esté escrito exactamente igual.")
    return getattr(actividad_1, nombre)


# ---------------------------------------------------------------------------
# Parte 1: Variables y tipos de datos
# Usamos type(x) is ... en lugar de isinstance, porque en Python
# True y False también cuentan como int, y queremos que sean tipos exactos.
# ---------------------------------------------------------------------------

def test_variable_nombre_materia():
    assert type(obtener("nombre_materia")) is str, "nombre_materia debe ser de tipo str"


def test_variable_numero_alumnos():
    assert type(obtener("numero_alumnos")) is int, "numero_alumnos debe ser de tipo int"


def test_variable_calificacion_minima():
    assert type(obtener("calificacion_minima")) is float, "calificacion_minima debe ser de tipo float"


def test_variable_es_obligatoria():
    assert type(obtener("es_obligatoria")) is bool, "es_obligatoria debe ser de tipo bool"


def test_variable_temas():
    temas = obtener("temas")
    assert type(temas) is list, "temas debe ser de tipo list"
    assert len(temas) >= 3, "temas debe tener al menos 3 elementos"


# ---------------------------------------------------------------------------
# Parte 2: Funciones
# pytest.approx compara números decimales permitiendo una pequeña diferencia,
# porque los float no siempre son exactos (por ejemplo, 0.1 + 0.2 != 0.3).
# ---------------------------------------------------------------------------

def test_area_circulo():
    area_circulo = obtener("area_circulo")
    assert type(area_circulo(1)) is float, "area_circulo debe regresar un float"
    assert area_circulo(1) == pytest.approx(3.14159, rel=1e-3)
    assert area_circulo(2.5) == pytest.approx(19.63495, rel=1e-3)


def test_perimetro_rectangulo():
    perimetro_rectangulo = obtener("perimetro_rectangulo")
    assert perimetro_rectangulo(3, 5) is not None, "perimetro_rectangulo regresó None. ¿Olvidaste usar return?"
    assert perimetro_rectangulo(3, 5) == 16
    assert perimetro_rectangulo(2.5, 1.5) == pytest.approx(8.0)


def test_celsius_a_fahrenheit():
    celsius_a_fahrenheit = obtener("celsius_a_fahrenheit")
    assert type(celsius_a_fahrenheit(100)) is float, "celsius_a_fahrenheit debe regresar un float"
    assert celsius_a_fahrenheit(100) == pytest.approx(212.0)
    assert celsius_a_fahrenheit(-40) == pytest.approx(-40.0)


def test_es_par():
    es_par = obtener("es_par")
    assert type(es_par(4)) is bool, "es_par debe regresar un bool (True o False)"
    assert es_par(4) == True
    assert es_par(7) == False


def test_saludar():
    saludar = obtener("saludar")
    assert type(saludar("Ana")) is str, "saludar debe regresar un str"
    assert saludar("Ana") == "Hola, Ana!"


# ---------------------------------------------------------------------------
# Parte 3: Iterar listas
# ---------------------------------------------------------------------------

def test_sumar_lista():
    sumar_lista = obtener("sumar_lista")
    assert sumar_lista([1, 2, 3, 4]) == 10
    assert sumar_lista([]) == 0, "La suma de una lista vacía debe ser 0"


def test_promedio():
    promedio = obtener("promedio")
    assert type(promedio([8, 9, 10])) is float, "promedio debe regresar un float"
    assert promedio([7, 8, 10, 9]) == pytest.approx(8.5)


def test_numero_mayor():
    numero_mayor = obtener("numero_mayor")
    assert numero_mayor([3, 17, 8, 2]) == 17
    assert numero_mayor([-5, -3, -9]) == -3, "Revisa tu función cuando todos los números son negativos"


def test_contar_letras_a():
    contar_letras_a = obtener("contar_letras_a")
    letras = ["A", "B", "A", "C", "D", "A", "E", "A", "F", "G", "A", "B"]
    assert contar_letras_a(letras) == 5
    assert contar_letras_a(["B", "C", "D"]) == 0
    assert contar_letras_a(["a", "A", "a"]) == 1, "Solo se cuenta la A mayúscula"


def test_contar_pares():
    contar_pares = obtener("contar_pares")
    assert contar_pares([1, 2, 3, 4, 5, 6]) == 3
    assert contar_pares([1, 3, 5]) == 0


def test_filtrar_positivos():
    filtrar_positivos = obtener("filtrar_positivos")
    assert type(filtrar_positivos([1, -2, 3])) is list, "filtrar_positivos debe regresar una list"
    assert filtrar_positivos([4, -1, 0, 7, -3, 2]) == [4, 7, 2]


# ---------------------------------------------------------------------------
# Parte 4: Revisar que las funciones de la Parte 3 usen un ciclo
# El objetivo de la actividad es practicar cómo recorrer una lista,
# así que se revisa el código de cada función:
#   - Debe tener un ciclo (for o while).
#   - No debe usar atajos de Python que ya hacen el recorrido por nosotros.
# ---------------------------------------------------------------------------

FUNCIONES_CON_CICLO = [
    "sumar_lista",
    "promedio",
    "numero_mayor",
    "contar_letras_a",
    "contar_pares",
    "filtrar_positivos",
]

FUNCIONES_PROHIBIDAS = ["sum", "max", "min", "sorted", "filter"]


@pytest.mark.parametrize("nombre_funcion", FUNCIONES_CON_CICLO)
def test_funcion_usa_ciclo(nombre_funcion):
    funcion = obtener(nombre_funcion)
    codigo = inspect.getsource(funcion)
    arbol = ast.parse(codigo)

    tiene_ciclo = False
    atajos_usados = []

    for nodo in ast.walk(arbol):
        if isinstance(nodo, (ast.For, ast.While)):
            tiene_ciclo = True

        if isinstance(nodo, ast.Call):
            if isinstance(nodo.func, ast.Name) and nodo.func.id in FUNCIONES_PROHIBIDAS:
                atajos_usados.append(nodo.func.id + "()")
            if isinstance(nodo.func, ast.Attribute) and nodo.func.attr == "count":
                atajos_usados.append(".count()")

    assert tiene_ciclo, f"{nombre_funcion} debe usar un ciclo for o while para recorrer la lista"
    assert atajos_usados == [], f"{nombre_funcion} no debe usar {', '.join(atajos_usados)}; recorre la lista con un ciclo"

