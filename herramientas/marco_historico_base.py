"""BASE para la sesión del marco histórico (se separó de la Clase 21 el 19 nov 2026).
Contiene Hilbert, Gödel, línea de tiempo, problema de la parada, Collatz, von Neumann y pseudoaleatorios;
falta recortarle lo que ya se vio en la Clase 21 (autómatas y máquina de Turing).

Original: Clase 21 · Jueves 19 de noviembre de 2026 · Aula.
De David Hilbert a John von Neumann: autómatas, lenguajes formales, máquina de Turing y pseudoaleatorios.

    python3 herramientas/clase_21.py sesiones/11_19/Clase_21_19_Nov_2026_Automatas_Turing_Pseudoaleatorios.pptx
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from presentaciones import *  # noqa: E402,F403

m = Mazo()
BLANCO_CINTA = "□"


def cinta(formas, x, y, simbolos, cabeza=None, lado=0.42, tam=15, resalte=AMBAR_CL, borde_res=AMBAR):
    """Dibuja una cinta; la celda bajo el cabezal va resaltada."""
    for i, s in enumerate(simbolos):
        es_cabeza = i == cabeza
        caja_texto(formas, x + i * lado, y, lado, lado, s, tam, MARINO if s != BLANCO_CINTA else GRIS,
                   resalte if es_cabeza else BLANCO, borde_res if es_cabeza else "CBD5E1", es_cabeza,
                   fuente=MONO, redondeo=0, grosor=2 if es_cabeza else 1)


def encabezados(formas, x, y, columnas, alto=0.36, relleno=MARINO, color=BLANCO, tam=11):
    """columnas: lista de (texto, ancho)."""
    xx = x
    for t, w in columnas:
        caja_texto(formas, xx, y, w, alto, t, tam, color, relleno, None, True, redondeo=0)
        xx += w


def renglon(formas, x, y, celdas, alto=0.36, relleno=BLANCO, tam=12, fuente=SANS, colores=None,
            negritas=None, alinear=None):
    xx = x
    for k, (t, w) in enumerate(celdas):
        c = (colores or {}).get(k, TEXTO)
        caja_texto(formas, xx, y, w, alto, t, tam, c, relleno, BORDE, (negritas or {}).get(k, False),
                   alinear=(alinear or {}).get(k, "c"),
                   fuente=MONO if fuente == MONO or k in (fuente if isinstance(fuente, tuple) else ()) else SANS,
                   redondeo=0)
        xx += w


# =====================================================================================
# 1 · Portada
l = m.oscura(notas=(
    "Hoy cerramos la unidad 1 del programa (1.3 Autómatas y lenguajes formales, 1.4 Máquina de Turing), "
    "que dejé para el final a propósito: ahora que ya programan, la teoría se entiende mejor. "
    "La pregunta de toda la clase: ¿qué puede calcular una máquina y qué no?"))
texto(l.shapes, 0.8, 2.0, 7.0, 1.4, "¿Qué puede calcular\nuna máquina?", 40, BLANCO, True)
texto(l.shapes, 0.8, 3.55, 7.0, 0.5, "De David Hilbert a John von Neumann: autómatas, lenguajes\n"
      "formales, máquina de Turing y números pseudoaleatorios", 16, "CBD5E1")
texto(l.shapes, 0.8, 4.45, 7.0, 0.3, "Clase 21 · Jueves 19 de noviembre de 2026 · Aula", 16, GRIS)
hitos = [("1900", "David Hilbert", "¿se puede decidir todo?"), ("1931", "Kurt Gödel", "hay verdades sin prueba"),
         ("1936", "Alan Turing", "qué es calcular"), ("1945", "John von Neumann", "el programa en memoria"),
         ("1956", "Stephen Kleene", "expresiones regulares"), ("Hoy", "Pseudoazar", "random no es al azar")]
for i, (a, quien, idea) in enumerate(hitos):
    y = 1.35 + i * 0.78
    caja(l.shapes, 8.05, y, 4.75, 0.64, PIZARRA, None, 0.08)
    caja(l.shapes, 8.05, y, 0.09, 0.64, ACENTOS[i], None, 0)
    texto(l.shapes, 8.3, y + 0.2, 0.65, 0.25, a, 12, ACENTOS[i], True)
    texto(l.shapes, 8.95, y + 0.2, 2.1, 0.25, quien, 12.5, BLANCO, True)
    texto(l.shapes, 10.95, y + 0.23, 1.75, 0.2, idea, 10, GRIS, alinear="r")

# =====================================================================================
# 2 · Noticia tech: ataque a Optimizely
l = m.lamina("Noticia tech", "Esta semana: un ataque a Optimizely, una herramienta que usan miles de sitios web, "
             "metió código malicioso en los sitios de 178 organizaciones. Entre ellas, HSBC México.", notas=(
    "Optimizely es una plataforma de «pruebas A/B»: le muestra dos versiones de una página a distintos visitantes "
    "para ver cuál funciona mejor. Para eso, sus clientes cargan en su sitio un archivo JavaScript de Optimizely. "
    "El atacante aprovechó una falla de Optimizely y modificó esos archivos: los sitios afectados no fueron "
    "hackeados directamente, el código malicioso llegó por un proveedor en el que confiaban. Eso se llama "
    "ataque a la cadena de suministro. Lo documentó el investigador de seguridad Scott Helme (Report URI): "
    "188 de 1,611 archivos revisados tenían el código; para el 16 de noviembre casi todos ya estaban limpios. "
    "Los pagos en formularios de proveedores externos (Stripe, Adyen) quedaron fuera de su alcance. "
    "La idea 1 es una explicación general de cómo funciona un skimmer, no el código exacto de este ataque."))
datos = [("15 – 16 NOV", "Qué pasó", "Aprovecharon una falla de Optimizely (sirve para probar versiones de una "
          "página) y alteraron el archivo que sus clientes cargan en su sitio.", BLANCO),
         ("A QUIÉN", "178 organizaciones", "CNN, BBC, IKEA, Zoom, Salesforce y HSBC, incluido su portal en "
          "México. Los sitios no fueron hackeados: el código llegó por su proveedor.", AMBAR_CL),
         ("QUÉ ROBABA", "Un skimmer", "Código que copia lo que escribes en un formulario de pago: número de "
          "tarjeta, vencimiento y código de seguridad.", ROJO_CL),
         ("HOY · 19 NOV", "Y no es el único", "Se filtraron datos de clientes de Visa, Mastercard y JPMorgan "
          "por otro proveedor. En México, los ataques a bancos subieron 70 % en un año.", AZUL_CL)]
for i, (e, t, c, f) in enumerate(datos):
    tarjeta(l.shapes, 0.55 + i * 3.08, 1.6, 2.9, 2.1, t, c, relleno=f, color_titulo=MARINO, etiqueta=e,
            tam=11)
texto(l.shapes, 0.55, 3.9, 12, 0.3, "Dos ideas de hoy que están dentro de un hackeo", 13, AZUL, True)
g1 = m.grupo(l)
tarjeta(g1.shapes, 0.55, 4.25, 6.0, 2.0, "1 · Reconocer patrones es un autómata",
        "Para robar tarjetas, el código malicioso tiene que reconocer qué texto **parece** un número de tarjeta "
        "(16 dígitos). Ese patrón se escribe con una **expresión regular**. Del otro lado, los antivirus buscan "
        "código malicioso igual: con patrones.", tam=11.5)
g2 = m.grupo(l)
tarjeta(g2.shapes, 6.75, 4.25, 6.0, 2.0, "2 · La seguridad depende del azar",
        "La llave que cifra tu conexión con el banco sale de números «al azar». Si alguien adivina la "
        "**semilla**, adivina la llave. Por eso en seguridad no basta lo **pseudoaleatorio** (lo vemos en "
        "la sección 4).", tam=11.5)
texto(l.shapes, 0.55, 6.5, 12.2, 0.2, "Fuentes: Scott Helme / Report URI, BleepingComputer, The Record, The Hacker "
      "News, Publimetro y Excélsior (17 nov 2026); PYMNTS (19 nov 2026); Kaspersky vía El CEO.", 9, GRIS)
m.clic(l, g1)
m.clic(l, g2)

# =====================================================================================
# 4 · Objetivo
l = m.lamina("Objetivo de la sesión", "Entender qué es, con precisión, un algoritmo: qué puede calcular "
             "una máquina, qué no, y por qué tu computadora no puede inventar el azar.")
obj = [("1", "La pregunta", "David Hilbert (matemático alemán) quería un método que decidiera cualquier verdad. Kurt Gödel (lógico austriaco) encontró un límite."),
       ("2", "Autómatas y lenguajes formales", "La máquina más simple: sólo recuerda en qué estado va."),
       ("3", "Máquina de Turing", "Una cinta, un cabezal y reglas: la definición de «calcular». "
        "Y un problema que ningún programa puede resolver."),
       ("4", "von Neumann y el azar", "El programa guardado en memoria y los números pseudoaleatorios.")]
for i, (n, t, c) in enumerate(obj):
    x = 0.55 + i * 3.08
    caja(l.shapes, x, 1.6, 2.9, 3.4, FONDO, BORDE)
    caja(l.shapes, x, 1.6, 2.9, 0.09, ACENTOS[i], None, 0)
    texto(l.shapes, x + 0.2, 1.85, 2.5, 0.6, n, 34, ACENTOS[i], True)
    texto(l.shapes, x + 0.2, 2.6, 2.5, 0.6, t, 15, MARINO, True)
    texto(l.shapes, x + 0.2, 3.3, 2.5, 1.6, c, 12, TEXTO)
caja(l.shapes, 0.55, 5.3, 12.2, 1.2, MARINO, None)
texto(l.shapes, 0.8, 5.47, 11.7, 0.9, "Programa de la materia · Unidad 1: 1.3 Autómatas y lenguajes formales · "
      "1.4 Máquina de Turing. Lo dejamos para ahora a propósito: ya que programan, la teoría se entiende "
      "mucho mejor.", 14, BLANCO)

# =====================================================================================
# 5 · Recuerda la Clase 2
l = m.lamina("¿Qué es un algoritmo? Lo que dijimos en la Clase 2", "Una definición que funciona… "
             "hasta que alguien pregunta qué significa «claras».", notas=(
    "Preguntar al grupo: ¿quién decide si un paso es lo bastante claro? ¿«Sazona al gusto» es un paso? "
    "Hasta 1936 no existía una definición matemática de algoritmo; hoy la vamos a construir."))
caja(l.shapes, 0.55, 1.6, 12.2, 1.25, PIZARRA, None)
texto(l.shapes, 0.85, 1.83, 11.6, 0.9, "«Una lista ordenada de instrucciones **claras** y **finitas** que "
      "podemos seguir para resolver un problema.»", 22, BLANCO)
preg = [("¿Qué es «clara»?", "«Agrega sal al gusto» es clara para tu mamá, no para una máquina. "
         "¿Dónde está la línea?"),
        ("¿Qué es «seguir»?", "¿Quién la sigue: una persona, una computadora, un mecanismo? ¿Con qué memoria?"),
        ("¿Siempre termina?", "Ya viste ciclos while que nunca terminan. ¿Se puede saber antes de correrlos?")]
grupos = []
for i, (t, c) in enumerate(preg):
    g = m.grupo(l)
    tarjeta(g.shapes, 0.55 + i * 4.12, 3.1, 3.96, 1.75, t, c, tam=13, tam_titulo=15)
    grupos.append(g)
g = m.grupo(l)
caja(g.shapes, 0.55, 5.1, 12.2, 1.4, AMBAR_CL, None)
texto(g.shapes, 0.8, 5.3, 11.7, 1.0, "Hasta 1936 **nadie** había definido «algoritmo» con precisión matemática. "
      "La definición salió de una pregunta sobre los límites de las matemáticas, cuando todavía "
      "no existían las computadoras.", 15, "78350F")
for g_ in grupos + [g]:
    m.clic(l, g_)

# =====================================================================================
# 6 · Separador 1
m.separador("1 de 4", "La pregunta", "¿Existe un procedimiento mecánico que decida si cualquier "
            "afirmación matemática es verdadera?", ACENTOS[0])

# =====================================================================================
# 7 · Línea de tiempo
l = m.lamina("Línea de tiempo: una pregunta que se vuelve computadora", "Cada clic, un paso de la historia. "
             "Fíjate en el orden: primero la teoría, luego las máquinas.", notas=(
    "Recorrer rápido. Lo importante es la dirección: una pregunta de lógica (Hilbert) lleva a definir qué es "
    "calcular (Turing) y eso a la computadora con programa almacenado (von Neumann)."))
linea = [("1900", "David Hilbert", "matemático alemán",
          "En el Congreso Internacional de Matemáticos (París) presenta una lista de 23 problemas sin resolver "
          "y pide bases firmes para las matemáticas."),
         ("1928", "Entscheidungsproblem", "alemán: «problema de la decisión»",
          "No es una publicación: es una **pregunta** que David Hilbert y Wilhelm Ackermann (matemático alemán) "
          "plantean en su libro de lógica: ¿existe un método mecánico que decida si cualquier fórmula es verdadera?"),
         ("1931", "Kurt Gödel", "lógico austriaco",
          "Publica en un artículo sus **teoremas de incompletitud**: en un sistema de reglas para la aritmética "
          "hay verdades que no se pueden demostrar."),
         ("1936", "Alonzo Church y Alan Turing", "lógico estadounidense · matemático inglés",
          "Cada uno, en su propio artículo, define con precisión qué es «calcular» y responde al "
          "Entscheidungsproblem: ese método general **no existe**."),
         ("1943 – 1959", "Los autómatas finitos", "varios autores",
          "Warren McCulloch y Walter Pitts (neurocientífico y lógico) modelan neuronas; Stephen Kleene (matemático) "
          "inventa las **expresiones regulares**; Michael Rabin y Dana Scott formalizan los autómatas."),
         ("1945", "John von Neumann", "matemático húngaro-estadounidense",
          "Escribe el reporte del **EDVAC** (una de las primeras computadoras electrónicas): el programa se guarda "
          "en la memoria, igual que los datos."),
         ("1946", "Cuadrados medios (algoritmo)", "de John von Neumann",
          "Un **algoritmo** para generar números que parecen al azar. Es el antepasado del random de Python.")]
for i, (a, t, perfil, c) in enumerate(linea):
    g = m.grupo(l)
    y = 1.55 + i * 0.72
    col = ACENTOS[i % 6] if ACENTOS[i % 6] != "FBBF24" else AMBAR
    caja(g.shapes, 0.55, y, 12.2, 0.64, FONDO, BORDE)
    caja(g.shapes, 0.55, y, 0.08, 0.64, col, None, 0)
    texto(g.shapes, 0.75, y + 0.18, 1.25, 0.3, a, 13 if len(a) < 6 else 11.5, col, True)
    texto(g.shapes, 2.0, y + 0.08, 3.2, 0.3, t, 12.5 if len(t) < 24 else 11.5, MARINO, True)
    texto(g.shapes, 2.0, y + 0.36, 3.2, 0.25, perfil, 10, TENUE)
    texto(g.shapes, 5.25, y + 0.06, 7.35, 0.55, c, 10.5, TEXTO, ancla="m")
    m.clic(l, g)

# =====================================================================================
# 8 · Hilbert
l = m.lamina("1900 – 1928 · David Hilbert: el sueño de una máquina de decidir",
             "El matemático más influyente de su época quería que las matemáticas fueran como un juego con "
             "reglas exactas.", notas=(
    "Congreso de París 1900: presentó 10 problemas en la conferencia y la versión publicada tuvo 23. "
    "1928: con Ackermann plantea el Entscheidungsproblem (problema de la decisión). "
    "1930, Königsberg: «Wir müssen wissen. Wir werden wissen.» Está en su tumba en Gotinga."))
tarjeta(l.shapes, 0.55, 1.55, 4.0, 2.55, "David Hilbert · 1862–1943",
        "Matemático alemán. En 1900 presentó los problemas que guiarían las matemáticas del siglo XX. "
        "Su plan de trabajo (el «programa de Hilbert», no es software): escribir las matemáticas con "
        "axiomas y reglas, y revisarlas mecánicamente.",
        etiqueta="UNIVERSIDAD DE GOTINGA", tam=12)
caja(l.shapes, 0.55, 4.3, 4.0, 1.75, MARINO, None)
texto(l.shapes, 0.8, 4.5, 3.6, 0.8, "«Debemos saber.\nSabremos.»", 22, BLANCO, True)
texto(l.shapes, 0.8, 5.45, 3.6, 0.5, "David Hilbert, discurso de 1930. Está escrito en su tumba.", 11, GRIS)
texto(l.shapes, 4.85, 1.55, 7.9, 0.3, "1928 · El Entscheidungsproblem («problema de la decisión»)", 14, AZUL, True)
texto(l.shapes, 4.85, 1.85, 7.9, 0.2, "Una pregunta que David Hilbert y Wilhelm Ackermann plantearon en su libro de lógica:", 11, TENUE)
pasos = [("ENTRADA", "una afirmación matemática\ncualquiera", FONDO, MARINO),
         ("PROCEDIMIENTO", "pasos mecánicos,\nsin ingenio", AZUL_CL, AZUL_OSC),
         ("SALIDA", "SÍ es verdadera / NO\n… y siempre termina", VERDE_CL, VERDE)]
for i, (t, c, f, col) in enumerate(pasos):
    x = 4.85 + i * 2.7
    caja(l.shapes, x, 2.2, 2.3, 1.45, f, BORDE)
    texto(l.shapes, x + 0.1, 2.32, 2.1, 0.3, t, 12, col, True, "c")
    texto(l.shapes, x + 0.1, 2.7, 2.1, 0.9, c, 12, TEXTO, alinear="c")
    if i < 2:
        flecha(l.shapes, x + 2.33, 2.92, x + 2.67, 2.92, TENUE, 2)
g = m.grupo(l)
caja(g.shapes, 4.85, 3.85, 7.9, 2.2, FONDO, BORDE)
texto(g.shapes, 5.1, 4.0, 7.4, 0.3, "Dicho en Python, David Hilbert pedía esta función:", 13, AZUL, True)
codigo(g.shapes, 5.1, 4.4, 7.4, 0.95, 'def es_verdadera(afirmacion):\n    # ... pasos mecánicos que nunca fallan ...', 12, etiqueta=None)
texto(g.shapes, 5.1, 5.48, 7.4, 0.5, "Que para **cualquier** afirmación regrese True o False, **siempre** "
      "termine y **nunca** se equivoque.", 12, TEXTO)
m.clic(l, g)

# =====================================================================================
# 9 · Demostrar vs probar con ejemplos
l = m.lamina("Demostrar no es lo mismo que probar con ejemplos", "Una demostración cubre todos los casos; "
             "los ejemplos sólo cubren los que probaste. Lo mismo pasa con tu código.", notas=(
    "Conexión con la plataforma: pasar las pruebas visibles no garantiza pasar las ocultas. "
    "Cita de Dijkstra (1969/1970, Notes on Structured Programming): las pruebas muestran la presencia de "
    "errores, no su ausencia."))
tarjeta(l.shapes, 0.55, 1.55, 3.9, 2.25, "Con ejemplos", "2 + 4 = 6 ✓   8 + 10 = 18 ✓\n100 + 36 = 136 ✓\n\n"
        "Convence, pero ¿y los infinitos casos que no probaste?", tam=13)
caja(l.shapes, 4.65, 1.55, 3.9, 2.25, VERDE_CL, None)
texto(l.shapes, 4.85, 1.68, 3.5, 0.3, "Con una demostración", 13, VERDE, True)
texto(l.shapes, 4.85, 2.05, 3.5, 1.7, "Un razonamiento paso a paso que vale para **todos** los "
      "casos, sin tener que probarlos uno por uno.\n\nEn la siguiente lámina: «la suma de dos pares es par».",
      13, "14532D")
tarjeta(l.shapes, 8.75, 1.55, 4.0, 2.25, "Axiomas + reglas = teoremas", "Se parte de afirmaciones aceptadas "
        "(axiomas) y se avanza con reglas lógicas. David Hilbert quería que revisar una prueba fuera **mecánico**, "
        "como seguir un algoritmo.", tam=12)
g = m.grupo(l)
caja(g.shapes, 0.55, 4.05, 12.2, 2.45, MARINO, None)
texto(g.shapes, 0.85, 4.25, 11.6, 0.3, "Tu código en la plataforma", 13, "93C5FD", True)
texto(g.shapes, 0.85, 4.65, 5.7, 1.7, "Pasar las pruebas visibles es «probar con ejemplos». Por eso existen "
      "las **pruebas ocultas**: los casos que no se te ocurrieron (lista vacía, un solo elemento, empates…).",
      14, BLANCO)
texto(g.shapes, 6.9, 4.65, 5.6, 1.2, "«Las pruebas pueden mostrar la presencia de errores, pero nunca su "
      "ausencia.»", 17, "FDE68A", True)
texto(g.shapes, 6.9, 5.85, 5.6, 0.3, "Edsger W. Dijkstra (científico de la computación neerlandés), 1970", 11, GRIS)
m.clic(l, g)

# =====================================================================================
# 9b · Demostración paso a paso: concreto → general
l = m.lamina("Paso a paso: la suma de dos números pares siempre es par",
             "Cada paso, primero con números concretos (8 y 6) y enseguida el mismo paso con letras, "
             "para que valga para todos.", notas=(
    "Cada renglón tiene dos clics: primero el paso con 8 y 6, luego el mismo paso con letras. Hacer notar que es "
    "exactamente el mismo paso, sólo que con una letra en lugar del número. Pregunta: ¿por qué usamos k y j y "
    "no la misma letra? (porque los dos pares pueden ser distintos; con la misma letra sólo probaríamos a + a)."))
cols_dem = [("Paso", 0.7), ("Con números: 8 y 6", 3.05), ("Con letras: a y b cualesquiera", 3.25),
            ("¿Qué hicimos?", 5.2)]
encabezados(l.shapes, 0.55, 1.6, cols_dem, 0.4, tam=12)
dem = [("8 = 2 · 4", "a = 2 · k", "Un número es **par** si se puede escribir como 2 por un entero. "
        "Con letras, k es ese entero: no sabemos cuánto vale, sólo que es entero."),
       ("6 = 2 · 3", "b = 2 · j", "Lo mismo con el segundo número. Usamos otra letra (j) porque puede ser "
        "un par distinto."),
       ("8 + 6 = 2·4 + 2·3", "a + b = 2k + 2j", "Sumamos, cambiando cada número por su forma «2 por algo»."),
       ("= 2 · (4 + 3)", "= 2 · (k + j)", "Sacamos el 2 como factor común: 2·4 + 2·3 es lo mismo que 2·(4 + 3)."),
       ("4 + 3 = 7 es entero\n⇒ 14 = 2 · 7 es par ✓", "k + j es entero\n⇒ a + b = 2 · (entero) es par ✓",
        "Entero + entero da un entero: el resultado cumple la definición de par.")]
anchos_dem = [w for _, w in cols_dem]
x_dem = [0.55 + sum(anchos_dem[:k]) for k in range(4)]
for i in range(len(dem)):
    renglon(l.shapes, 0.55, 2.0 + i * 0.7, [(str(i + 1), 0.7), ("", 3.05), ("", 3.25), ("", 5.2)], 0.7,
            tam=13, negritas={0: True})
for i, (conc, gen, que) in enumerate(dem):
    y = 2.0 + i * 0.7
    g = m.grupo(l)
    caja_texto(g.shapes, x_dem[1], y, 3.05, 0.7, conc, 13, AMBAR, AMBAR_CL, BORDE, True, redondeo=0)
    texto(g.shapes, x_dem[3] + 0.12, y + 0.05, 5.0, 0.6, que, 10.5, TEXTO, ancla="m")
    m.clic(l, g)
    g = m.grupo(l)
    caja_texto(g.shapes, x_dem[2], y, 3.25, 0.7, gen, 13, VERDE, VERDE_CL, BORDE, True, redondeo=0)
    m.clic(l, g)
g = m.grupo(l)
caja(g.shapes, 0.55, 5.65, 12.2, 0.9, MARINO, None)
texto(g.shapes, 0.85, 5.75, 11.6, 0.7, "Con números sólo demostramos que 8 + 6 es par. Con letras hicimos **los "
      "mismos pasos**, pero k y j representan **cualquier** entero: por eso vale para todos los pares, incluso "
      "los que nadie ha escrito.", 13.5, BLANCO, ancla="m")
m.clic(l, g)

# =====================================================================================
# 10 · Gödel
l = m.lamina("1931 · Kurt Gödel: hay verdades que no se pueden demostrar",
             "A los 25 años respondió una parte de la pregunta de David Hilbert… y la respuesta fue «no».", notas=(
    "Gödel, «Über formal unentscheidbare Sätze der Principia Mathematica und verwandter Systeme I», "
    "Monatshefte für Mathematik und Physik, 1931. La frase G es una analogía, no la prueba formal. "
    "El truco real: codificar fórmulas como números (numeración de Gödel), igual que tu computadora "
    "guarda letras como números."))
tarjeta(l.shapes, 0.55, 1.55, 3.9, 2.4, "Kurt Gödel · 1906–1978", "Lógico y matemático austriaco; después "
        "trabajó en Princeton (EE. UU.), donde fue gran amigo de Albert Einstein. «Incompletitud»: al sistema "
        "le faltan pruebas para algunas verdades.",
        etiqueta="UNIVERSIDAD DE VIENA", tam=12)
caja(l.shapes, 4.65, 1.55, 8.1, 1.05, PIZARRA, None)
texto(l.shapes, 4.9, 1.75, 7.6, 0.7, "G:  «Esta afirmación no se puede demostrar.»", 22, "FDE68A", True)
g1 = m.grupo(l)
tarjeta(g1.shapes, 4.65, 2.8, 8.1, 1.15, "¿Por qué G sería verdadera, pero sin prueba?", "Sólo hay dos "
        "posibilidades: G se puede demostrar, o no. En la siguiente lámina revisamos cada una, paso a paso.",
        relleno=AZUL_CL, borde=None, color_titulo=AZUL_OSC, tam=12.5)
g3 = m.grupo(l)
tarjeta(g3.shapes, 0.55, 4.2, 4.0, 2.3, "El truco: todo es un número", "Gödel convirtió cada fórmula en un "
        "número. Así una fórmula puede «hablar» de otras fórmulas… y de sí misma. "
        "Tu computadora hace lo mismo: la letra «A» es el 65.", tam=12)
tarjeta(g3.shapes, 4.75, 4.2, 3.9, 2.3, "Qué SÍ dijo", "En cualquier sistema de reglas lo bastante fuerte "
        "para la aritmética (y sin contradicciones) hay afirmaciones verdaderas que **no se pueden "
        "demostrar dentro de él**.", relleno=VERDE_CL, borde=None, color_titulo=VERDE, tam=12)
tarjeta(g3.shapes, 8.85, 4.2, 3.9, 2.3, "Qué NO dijo", "Que nada se pueda demostrar, que las matemáticas "
        "estén mal o que «todo es relativo». Sólo encontró un **límite** de los sistemas formales (axiomas + reglas, como los que quería David Hilbert).",
        relleno=ROJO_CL, borde=None, color_titulo=ROJO, tam=12)
for g_ in (g1, g3):
    m.clic(l, g_)

# =====================================================================================
# 10b · La lógica de G, paso a paso
l = m.lamina("Paso a paso: ¿por qué G es verdadera, pero no tiene prueba?",
             "Primero con un ejemplo cotidiano (un árbitro que nunca miente) y enseguida el mismo paso con el "
             "sistema de Kurt Gödel.", notas=(
    "Cada renglón tiene dos clics: primero el árbitro, luego el sistema. La idea clave: sólo hay dos casos "
    "(se demuestra o no se demuestra); el primero lleva a algo imposible, así que queda el segundo. "
    "Es el mismo esquema que la demostración por contradicción que veremos con Alan Turing. "
    "«El sistema no demuestra mentiras» es una suposición razonable: un sistema que demuestra cosas falsas no sirve."))
cols_g = [("Paso", 2.0), ("Con un árbitro que nunca miente", 5.1), ("Con el sistema de Kurt Gödel", 5.1)]
encabezados(l.shapes, 0.55, 1.6, cols_g, 0.4, tam=12)
filas_g = [("La frase", "«El árbitro nunca dirá que esta frase es verdadera.»",
            "G: «Esta afirmación no se puede demostrar.»", BLANCO),
           ("La regla", "El árbitro nunca miente: si dice «verdadera», es verdadera.",
            "El sistema no demuestra mentiras: lo que demuestra, es verdadero.", BLANCO),
           ("Caso 1 · supón…", "…que el árbitro dice: «la frase es verdadera».",
            "…que el sistema sí demuestra G.", ROJO_CL),
           ("⇒ entonces", "Ya lo dijo, así que la frase («nunca lo dirá») es falsa: el árbitro mintió. "
            "**Imposible** ✗", "Ya se demostró, así que G («no se puede demostrar») es falsa: el sistema "
            "demostró una mentira. **Imposible** ✗", ROJO_CL),
           ("Caso 2 · queda…", "…que el árbitro nunca lo dice.", "…que G no se puede demostrar.", VERDE_CL),
           ("⇒ entonces", "Justo lo que dice la frase: es **verdadera**, y el árbitro nunca lo dirá ✓",
            "Justo lo que dice G: G es **verdadera**, pero **no tiene prueba** ✓", VERDE_CL)]
for i in range(len(filas_g)):
    renglon(l.shapes, 0.55, 2.0 + i * 0.6, [("", 2.0), ("", 5.1), ("", 5.1)], 0.6)
for i, (paso, conc, gen, f) in enumerate(filas_g):
    y = 2.0 + i * 0.6
    g = m.grupo(l)
    caja_texto(g.shapes, 0.55, y, 2.0, 0.6, paso, 12, MARINO, f, BORDE, True, redondeo=0)
    caja_texto(g.shapes, 2.55, y, 5.1, 0.6, conc, 11.5, TEXTO, f, BORDE, alinear="l", redondeo=0)
    m.clic(l, g)
    g = m.grupo(l)
    caja_texto(g.shapes, 7.65, y, 5.1, 0.6, gen, 11.5, TEXTO, f, BORDE, alinear="l", redondeo=0)
    m.clic(l, g)
g = m.grupo(l)
caja(g.shapes, 0.55, 5.8, 12.2, 0.75, MARINO, None)
texto(g.shapes, 0.85, 5.85, 11.6, 0.65, "Sólo había dos casos y el primero es imposible. Queda el segundo: hay una "
      "afirmación **verdadera** que el sistema **nunca podrá demostrar**. Eso es la incompletitud.", 14, BLANCO,
      ancla="m")
m.clic(l, g)

# =====================================================================================
# 11 · Separador 2
m.separador("2 de 4", "Autómatas y lenguajes formales", "Antes de la máquina de Turing, la máquina más "
            "simple que existe: sólo recuerda en qué estado va.", ACENTOS[1], notas=(
    "Históricamente los autómatas finitos se formalizaron después de Turing (1943–1959), pero son más simples "
    "y por eso los vemos primero."))

# =====================================================================================
# 12 · Lenguajes formales
l = m.lamina("Lenguajes formales: reglas exactas, cero ambigüedad",
             "Un lenguaje formal es un conjunto de cadenas que se arman con un alfabeto y reglas precisas.",
             notas=("El español es ambiguo: «Vi a Juan con el telescopio» (¿quién tenía el telescopio?). "
                    "Un lenguaje formal no lo es. Python es un lenguaje formal: el intérprete acepta o "
                    "rechaza tu archivo; SyntaxError significa que tu texto no pertenece al lenguaje."))
defs = [("Alfabeto  Σ", "El **conjunto de símbolos** que se pueden usar. No tiene que ser el abecedario: "
         "puede ser {0, 1}, los dígitos, o hasta eventos como {tarjeta, empujar}. Σ (sigma, letra griega) es "
         "sólo su nombre.", "Σ = {0, 1}"),
        ("Cadena", "Símbolos del alfabeto puestos uno tras otro, como un str de Python. Puede ser vacía "
         "(cero símbolos).", '"0110"   "1"   ""'),
        ("Lenguaje", "El conjunto de cadenas que cumplen una regla. Puede tener una infinidad de cadenas.",
         "L = { cadenas con una cantidad par de 1 }")]
for i, (t, c, e) in enumerate(defs):
    x = 0.55 + i * 4.12
    tarjeta(l.shapes, x, 1.55, 3.96, 2.3, t, c, tam=12, tam_titulo=16)
    texto(l.shapes, x + 0.18, 3.35, 3.6, 0.4, e, 13 if i < 2 else 12, AZUL_OSC, fuente=MONO if i < 2 else SANS)
g = m.grupo(l)
tarjeta(g.shapes, 0.55, 4.05, 6.0, 2.45, "El español es ambiguo", "«Vi a Juan con el telescopio».\n"
        "¿Quién tenía el telescopio: tú o Juan?\n\nLas personas lo resolvemos por contexto. "
        "Una máquina no puede.", relleno=AMBAR_CL, borde=None, color_titulo=AMBAR, tam=13)
g2 = m.grupo(l)
caja(g2.shapes, 6.75, 4.05, 6.0, 2.45, PIZARRA, None)
texto(g2.shapes, 7.0, 4.17, 5.5, 0.3, "Python es un lenguaje formal", 14, "93C5FD", True)
texto(g2.shapes, 7.0, 4.55, 5.5, 0.4, "if x > 3 print(x)", 15, "CE9178", fuente=MONO)
texto(g2.shapes, 7.0, 4.98, 5.5, 0.4, "SyntaxError: expected ':'", 13, "F87171", fuente=MONO)
texto(g2.shapes, 7.0, 5.45, 5.5, 1.0, "Un **SyntaxError** quiere decir: «esa cadena no pertenece al lenguaje». "
      "Lo decide una máquina, sin entender qué querías hacer.", 13, "E2E8F0")
m.clic(l, g)
m.clic(l, g2)

# =====================================================================================
# 12b · Qué es un autómata, para qué sirve y cómo se lee
l = m.lamina("¿Qué es un autómata finito y para qué sirve?",
             "Una máquina imaginaria (un modelo en papel, no un aparato) con muy poca memoria.", notas=(
    "Insistir en que es un modelo: se dibuja y se razona con él, como un diagrama de flujo. "
    "El doble círculo es lo que más confunde: NO detiene la lectura. Pasar por él a la mitad de la cadena no "
    "cuenta; sólo importa en qué estado quedas cuando ya no hay símbolos. "
    "Los autómatas que sólo controlan (torniquete, semáforo) a veces no tienen doble círculo."))
caja(l.shapes, 0.55, 1.55, 12.2, 1.05, MARINO, None)
texto(l.shapes, 0.85, 1.62, 11.6, 0.9, "Un **autómata finito** lee una cadena **símbolo por símbolo**, de izquierda "
      "a derecha, y con cada símbolo **cambia de estado** según reglas fijas. No puede regresar, ni escribir, ni "
      "guardar nada más que **el estado en que va**.", 14.5, BLANCO, ancla="m")
g1 = m.grupo(l)
tarjeta(g1.shapes, 0.55, 2.8, 6.0, 1.45, "Finalidad 1 · Reconocer (decir SÍ o NO)",
        "¿Esta cadena cumple la regla? Al terminar de leer responde **acepta** o **rechaza**. "
        "Ej.: ¿es un número entero válido? ¿tiene forma de CURP?", relleno=VERDE_CL, borde=None,
        color_titulo=VERDE, tam=12)
g2 = m.grupo(l)
tarjeta(g2.shapes, 6.75, 2.8, 6.0, 1.45, "Finalidad 2 · Controlar (reaccionar a eventos)",
        "Modelar algo que cambia de situación según lo que pasa: un torniquete, un semáforo, un pedido. "
        "Aquí importa en qué estado está, no aceptar.", relleno=AZUL_CL, borde=None, color_titulo=AZUL_OSC, tam=12)
texto(l.shapes, 0.55, 4.4, 12, 0.3, "Cómo se lee el dibujo", 13, AZUL, True)
leyenda = [("Círculo = estado", "Una **situación** en la que puede estar la máquina. Lleva un nombre que "
            "dice qué recuerda: «par», «bloqueado»."),
           ("Flecha con símbolo = transición", "«Si estoy aquí y leo este símbolo, me paso allá». "
            "Si la flecha regresa al mismo círculo, me quedo donde estoy."),
           ("Flecha sin origen = inicio", "Marca el estado donde empieza, antes de leer el primer símbolo. "
            "Siempre hay exactamente uno."),
           ("Doble círculo = aceptación", "Si **al terminar** de leer estás aquí, la respuesta es **SÍ**. "
            "Pasar por él a la mitad no cuenta.")]
grupos_leyenda = []
for i, (t, c) in enumerate(leyenda):
    g = m.grupo(l)
    grupos_leyenda.append(g)
    x = 0.55 + i * 3.08
    caja(g.shapes, x, 4.75, 2.9, 1.8, FONDO, BORDE)
    cx, cy = x + 1.45, 5.12
    if i == 0:
        estado(g.shapes, cx, cy, 0.25, "A", tam=11)
    elif i == 1:
        estado(g.shapes, x + 0.55, cy, 0.22, "A", tam=10)
        estado(g.shapes, x + 2.35, cy, 0.22, "B", tam=10)
        flecha(g.shapes, x + 0.79, cy, x + 2.11, cy, MARINO, 2)
        texto(g.shapes, cx - 0.3, cy - 0.3, 0.6, 0.25, "1", 12, AZUL, True, "c", fuente=MONO)
    elif i == 2:
        flecha(g.shapes, x + 0.55, cy, x + 1.18, cy, MARINO, 2)
        estado(g.shapes, cx, cy, 0.25, "A", tam=11)
    else:
        estado(g.shapes, cx, cy, 0.25, "A", True, VERDE_CL, VERDE, 11)
    texto(g.shapes, x + 0.15, 5.42, 2.6, 0.25, t, 11, MARINO, True)
    texto(g.shapes, x + 0.15, 5.7, 2.6, 0.8, c, 10, TEXTO)
for g_ in [g1, g2] + grupos_leyenda:
    m.clic(l, g_)

# =====================================================================================
# 13 · Torniquete
l = m.lamina("El autómata más simple: el torniquete del Metro",
             "No sabe cuánta gente ha pasado ni qué hora es. Sólo sabe en qué estado está.", notas=(
    "Dibujarlo en el pizarrón con el grupo. Preguntar: ¿qué pasa si empujo estando bloqueado? (se queda "
    "bloqueado). ¿Y si paso la tarjeta dos veces? (se queda desbloqueado; en la vida real se cobra dos veces). "
    "La flecha corta que entra a «Bloqueado» marca el estado inicial."))
estado(l.shapes, 2.6, 3.85, 0.8, "Bloqueado", relleno=ROJO_CL, borde=ROJO, tam=14)
estado(l.shapes, 6.6, 3.85, 0.8, "Desbloqueado", relleno=VERDE_CL, borde=VERDE, tam=12.5)
flecha(l.shapes, 0.6, 3.85, 1.78, 3.85, MARINO, 2)
texto(l.shapes, 0.5, 3.45, 1.2, 0.3, "inicio", 11, TENUE, alinear="c")
flecha(l.shapes, 3.35, 3.55, 5.85, 3.55, MARINO, 2)
texto(l.shapes, 3.4, 3.1, 2.4, 0.35, "pasa la tarjeta", 13, AZUL, True, "c")
flecha(l.shapes, 5.85, 4.15, 3.35, 4.15, MARINO, 2)
texto(l.shapes, 3.4, 4.23, 2.4, 0.35, "empujas y pasas", 13, AZUL, True, "c")
bucle(l.shapes, 2.6, 3.85, 0.8, angulo=90, rb=0.45, color=ROJO)
texto(l.shapes, 1.4, 1.75, 2.4, 0.55, "empujas\n(no pasa)", 12, ROJO, True, "c")
bucle(l.shapes, 6.6, 3.85, 0.8, angulo=90, rb=0.45, color=VERDE)
texto(l.shapes, 5.3, 1.75, 2.6, 0.55, "tarjeta otra vez\n(sigue abierto)", 12, VERDE, True, "c")
encabezados(l.shapes, 8.3, 1.65, [("Estado actual", 1.6), ("Entrada", 1.4), ("Nuevo estado", 1.45)])
filas = [("Bloqueado", "tarjeta", "Desbloqueado"), ("Bloqueado", "empujar", "Bloqueado"),
         ("Desbloqueado", "empujar", "Bloqueado"), ("Desbloqueado", "tarjeta", "Desbloqueado")]
for i, f in enumerate(filas):
    renglon(l.shapes, 8.3, 2.01 + i * 0.4, list(zip(f, (1.6, 1.4, 1.45))), 0.4, tam=12)
texto(l.shapes, 8.3, 3.75, 4.45, 0.3, "Tabla de transiciones: la misma información, sin dibujo.", 11, TENUE)
g = m.grupo(l)
caja(g.shapes, 0.55, 5.1, 12.2, 1.4, MARINO, None)
texto(g.shapes, 0.85, 5.28, 11.6, 1.1, "Es un autómata para **controlar** (finalidad 2): no tiene doble círculo porque no "
      "responde sí o no. Su alfabeto son eventos: {tarjeta, empujar}. Su única memoria es **el estado actual**, "
      "como una variable bandera que sólo puede tomar dos valores.", 15, BLANCO)
m.clic(l, g)

# =====================================================================================
# 14 · Partes del AFD + paridad
l = m.lamina("Las cinco piezas de un autómata finito",
             "Ejemplo: acepta las cadenas de 0 y 1 que tienen una cantidad par de unos.", notas=(
    "Doble círculo = estado de aceptación: si al terminar de leer la cadena estás ahí, la cadena se acepta. "
    "La cadena vacía tiene cero unos, y cero es par: se acepta."))
estado(l.shapes, 2.0, 3.75, 0.7, "par", True, VERDE_CL, VERDE, 16)
estado(l.shapes, 5.6, 3.75, 0.7, "impar", False, BLANCO, AZUL_OSC, 16)
flecha(l.shapes, 0.55, 3.75, 1.3, 3.75, MARINO, 2)
texto(l.shapes, 0.4, 3.35, 1.0, 0.3, "inicio", 11, TENUE, alinear="c")
flecha(l.shapes, 2.62, 3.45, 4.98, 3.45, MARINO, 2)
texto(l.shapes, 3.4, 3.05, 0.8, 0.35, "1", 16, AZUL, True, "c", fuente=MONO)
flecha(l.shapes, 4.98, 4.05, 2.62, 4.05, MARINO, 2)
texto(l.shapes, 3.4, 4.1, 0.8, 0.35, "1", 16, AZUL, True, "c", fuente=MONO)
bucle(l.shapes, 2.0, 3.75, 0.7, "0", 90, rb=0.42)
bucle(l.shapes, 5.6, 3.75, 0.7, "0", 90, rb=0.42)
piezas = [("1 · Estados", "par, impar"), ("2 · Alfabeto", "Σ = {0, 1}: los símbolos que lee"), ("3 · Estado inicial", "par (la flecha que entra)"),
          ("4 · Aceptación", "par (doble círculo): si terminas aquí, acepta"), ("5 · Transiciones", "con 1 cambias; con 0 te quedas")]
for i, (t, c) in enumerate(piezas):
    g = m.grupo(l)
    caja(g.shapes, 7.2, 1.55 + i * 0.75, 5.55, 0.65, FONDO, BORDE)
    caja(g.shapes, 7.2, 1.55 + i * 0.75, 0.08, 0.65, ACENTOS[i], None, 0)
    texto(g.shapes, 7.45, 1.72 + i * 0.75, 2.2, 0.3, t, 13, MARINO, True)
    texto(g.shapes, 9.6, 1.73 + i * 0.75, 3.1, 0.3, c, 12.5, TEXTO)
    m.clic(l, g)
g = m.grupo(l)
caja(g.shapes, 0.55, 5.45, 12.2, 1.05, AZUL_CL, None)
texto(g.shapes, 0.8, 5.6, 11.7, 0.8, "El **lenguaje** del autómata = todas las cadenas que acepta: "
      '"", "0", "11", "1001", "0110"…   Rechaza "1", "111", "1011"…', 14, AZUL_OSC)
m.clic(l, g)

# =====================================================================================
# 15 · Traza "1001"
l = m.lamina("Prueba de escritorio de un autómata: \"1001\"",
             "Igual que en la Clase 17: un renglón por paso. Aquí la única «variable» es el estado.", notas=(
    "Pedir que la hagan ellos con \"1011\" antes de mostrar la siguiente lámina: termina en impar, se rechaza."))
estado(l.shapes, 1.6, 3.05, 0.55, "par", True, VERDE_CL, VERDE, 14)
estado(l.shapes, 4.4, 3.05, 0.55, "impar", False, BLANCO, AZUL_OSC, 14)
flecha(l.shapes, 0.45, 3.05, 1.05, 3.05, MARINO, 2)
flecha(l.shapes, 2.1, 2.83, 3.9, 2.83, MARINO, 2)
flecha(l.shapes, 3.9, 3.27, 2.1, 3.27, MARINO, 2)
texto(l.shapes, 2.7, 2.45, 0.6, 0.3, "1", 14, AZUL, True, "c", fuente=MONO)
texto(l.shapes, 2.7, 3.32, 0.6, 0.3, "1", 14, AZUL, True, "c", fuente=MONO)
bucle(l.shapes, 1.6, 3.05, 0.55, "0", 90, rb=0.36)
bucle(l.shapes, 4.4, 3.05, 0.55, "0", 90, rb=0.36)
texto(l.shapes, 0.55, 3.95, 5.2, 0.3, "Cadena de entrada", 12, TENUE, True)
cinta(l.shapes, 0.55, 4.3, list("1001"), None, 0.6, 20)
cols = [("Paso", 0.9), ("Lee", 1.2), ("Estado antes", 2.0), ("Estado después", 2.2)]
encabezados(l.shapes, 6.3, 1.6, cols, 0.42, tam=12)
traza = [("0", "—", "—", "par (inicio)"), ("1", "1", "par", "impar"), ("2", "0", "impar", "impar"),
         ("3", "0", "impar", "impar"), ("4", "1", "impar", "par")]
for i, f in enumerate(traza):
    g = m.grupo(l)
    renglon(g.shapes, 6.3, 2.02 + i * 0.5, list(zip(f, (0.9, 1.2, 2.0, 2.2))), 0.5, tam=14,
            colores={3: AZUL}, negritas={3: True})
    m.clic(l, g)
g = m.grupo(l)
caja(g.shapes, 6.3, 4.75, 6.3, 0.85, VERDE_CL, None)
texto(g.shapes, 6.5, 4.9, 5.9, 0.6, "Terminó en **par** (doble círculo) ⇒ \"1001\" **se acepta**. Tiene dos unos.", 14, "14532D")
m.clic(l, g)
g = m.grupo(l)
caja(g.shapes, 0.55, 5.85, 12.05, 0.7, AMBAR_CL, None)
texto(g.shapes, 0.8, 6.02, 11.6, 0.4, "Tu turno: haz la tabla para \"1011\". ¿Se acepta o se rechaza?", 14, "78350F", True)
m.clic(l, g)

# =====================================================================================
# 16 · El autómata en Python
l = m.lamina("El autómata en Python: un for, un if y una variable de estado",
             "Ya sabes escribirlo: recorrer la cadena símbolo por símbolo y actualizar el estado.", notas=(
    "La variable estado es una bandera: el programa no guarda cuántos unos lleva, sólo si van pares o impares. "
    "Nombre según la regla del curso: regresa True/False, así que empieza con es_."))
codigo(l.shapes, 0.55, 1.55, 7.0, 3.6, '''def es_cantidad_par_unos(cadena):
    estado = "par"
    for simbolo in cadena:
        if simbolo == "1":
            if estado == "par":
                estado = "impar"
            else:
                estado = "par"
    return estado == "par"''', 14)
tarjeta(l.shapes, 7.8, 1.55, 4.95, 1.1, "Llamadas", "", tam=12)
texto(l.shapes, 8.0, 1.95, 4.6, 0.6, 'es_cantidad_par_unos("1001")  → True\nes_cantidad_par_unos("1011")  → False',
      11.5, AZUL_OSC, fuente=MONO)
g = m.grupo(l)
tarjeta(g.shapes, 7.8, 2.85, 4.95, 2.3, "¿Dónde está cada pieza?", "Estado inicial → línea 2\n"
        "Leer símbolo por símbolo → línea 3\nTransiciones → líneas 4 a 8\nAceptación → línea 9\n"
        "Con un 0 no hay if: el estado se queda igual.", tam=12.5)
m.clic(l, g)
g = m.grupo(l)
caja(g.shapes, 0.55, 5.4, 12.2, 1.1, MARINO, None)
texto(g.shapes, 0.85, 5.55, 11.6, 0.85, "No importa si la cadena tiene 4 símbolos o 4 millones: la función "
      "sólo usa **una variable** de memoria. Eso es lo que hace «finito» al autómata: memoria O(1).",
      15, BLANCO)
m.clic(l, g)

# =====================================================================================
# 16b · Mismo problema: diagrama de flujo vs autómata
def figura(formas, tipo, x, y, w, h, contenido, relleno=BLANCO, borde=AZUL_OSC, tam=11):
    s = caja(formas, x, y, w, h, relleno, borde, 0, forma=tipo, grosor=1.5)
    tf = s.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.04)
    tf.margin_top = tf.margin_bottom = Inches(0.01)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    for k, linea in enumerate(contenido.split("\n")):
        p_ = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
        p_.alignment = PP_ALIGN.CENTER
        r_ = p_.add_run(); r_.text = linea
        _fuente(r_, tam, MARINO, False, SANS)
    return s


from presentaciones import _fuente  # noqa: E402
l = m.lamina("Mismo problema, dos dibujos: diagrama de flujo y autómata",
             "¿La cadena tiene una cantidad par de unos? A la izquierda, como en la Clase 15; a la derecha, como hoy.",
             notas=("Recorrer los dos con \"1001\". En el diagrama de flujo el dedo pasa por acciones (asignar, leer, "
                    "comparar); en el autómata sólo salta de un círculo a otro con cada símbolo. "
                    "El autómata es más compacto porque el «leer el siguiente símbolo» y el «¿quedan símbolos?» "
                    "están implícitos: siempre se lee uno por flecha y se termina cuando se acaba la cadena."))
caja(l.shapes, 0.55, 1.55, 6.0, 5.0, FONDO, BORDE)
texto(l.shapes, 0.75, 1.62, 5.6, 0.3, "Diagrama de flujo (Clase 15)", 13, AZUL, True)
cxf = 2.6
figura(l.shapes, MSO_SHAPE.FLOWCHART_TERMINATOR, 1.6, 1.98, 2.0, 0.38, "Inicio", AZUL_CL)
figura(l.shapes, MSO_SHAPE.FLOWCHART_PROCESS, 1.3, 2.55, 2.6, 0.4, 'estado = "par"')
figura(l.shapes, MSO_SHAPE.FLOWCHART_DECISION, 1.3, 3.13, 2.6, 0.62, "¿quedan símbolos?", AMBAR_CL, AMBAR, 10.5)
figura(l.shapes, MSO_SHAPE.FLOWCHART_DATA, 1.3, 3.95, 2.6, 0.4, "leer el siguiente símbolo")
figura(l.shapes, MSO_SHAPE.FLOWCHART_DECISION, 1.3, 4.55, 2.6, 0.6, '¿es "1"?', AMBAR_CL, AMBAR)
figura(l.shapes, MSO_SHAPE.FLOWCHART_PROCESS, 1.3, 5.35, 2.6, 0.42, "cambiar par ↔ impar")
figura(l.shapes, MSO_SHAPE.FLOWCHART_TERMINATOR, 4.3, 3.19, 2.1, 0.5, "Fin: acepta\nsi estado = par", AZUL_CL, tam=10)
for y1, y2 in ((2.36, 2.55), (2.95, 3.13), (3.75, 3.95), (4.35, 4.55), (5.15, 5.35)):
    flecha(l.shapes, cxf, y1, cxf, y2, MARINO, 1.5)
texto(l.shapes, cxf + 0.08, 3.74, 0.4, 0.2, "sí", 10, VERDE, True)
texto(l.shapes, cxf + 0.08, 5.14, 0.4, 0.2, "sí", 10, VERDE, True)
flecha(l.shapes, 3.9, 3.44, 4.3, 3.44, MARINO, 1.5)
texto(l.shapes, 3.9, 3.2, 0.4, 0.2, "no", 10, ROJO, True, "c")
flecha(l.shapes, 1.3, 5.56, 0.85, 5.56, MARINO, 1.5, punta=False)
flecha(l.shapes, 1.3, 4.85, 0.85, 4.85, MARINO, 1.5, punta=False)
texto(l.shapes, 0.85, 4.6, 0.45, 0.2, "no", 10, ROJO, True, "c")
flecha(l.shapes, 0.85, 5.56, 0.85, 3.44, MARINO, 1.5, punta=False)
flecha(l.shapes, 0.85, 3.44, 1.3, 3.44, MARINO, 1.5)
texto(l.shapes, 0.75, 5.95, 5.6, 0.5, "Las figuras son **acciones**: asignar, leer, comparar. 7 figuras.", 12, TEXTO)
g = m.grupo(l)
caja(g.shapes, 6.75, 1.55, 6.0, 5.0, FONDO, BORDE)
texto(g.shapes, 6.95, 1.62, 5.6, 0.3, "Autómata (hoy)", 13, AZUL, True)
estado(g.shapes, 8.4, 3.85, 0.6, "par", True, VERDE_CL, VERDE, 15)
estado(g.shapes, 11.3, 3.85, 0.6, "impar", False, BLANCO, AZUL_OSC, 15)
flecha(g.shapes, 7.0, 3.85, 7.8, 3.85, MARINO, 2)
flecha(g.shapes, 8.95, 3.6, 10.75, 3.6, MARINO, 2)
texto(g.shapes, 9.55, 3.22, 0.6, 0.3, "1", 15, AZUL, True, "c", fuente=MONO)
flecha(g.shapes, 10.75, 4.1, 8.95, 4.1, MARINO, 2)
texto(g.shapes, 9.55, 4.15, 0.6, 0.3, "1", 15, AZUL, True, "c", fuente=MONO)
bucle(g.shapes, 8.4, 3.85, 0.6, "0", 90, rb=0.38)
bucle(g.shapes, 11.3, 3.85, 0.6, "0", 90, rb=0.38)
texto(g.shapes, 6.95, 5.95, 5.6, 0.5, "Los círculos son **situaciones** (estados); las flechas, **lo que se lee**. "
      "2 círculos.", 12, TEXTO)
m.clic(l, g)

# =====================================================================================
# 16c · Parecidos y diferencias
l = m.lamina("Diagrama de flujo vs autómata: parecidos y diferencias",
             "Los dos dibujan un algoritmo, pero cuentan cosas distintas.", notas=(
    "El diagrama de flujo es general: sirve para cualquier programa. El autómata es un caso especial, con "
    "memoria mínima, y por eso se puede analizar a fondo (por ejemplo, saber exactamente qué cadenas acepta)."))
caja(l.shapes, 0.55, 1.55, 12.2, 1.05, VERDE_CL, None)
texto(l.shapes, 0.8, 1.62, 11.7, 0.3, "En qué se parecen", 13, VERDE, True)
texto(l.shapes, 0.8, 1.95, 11.7, 0.6, "Los dos describen un algoritmo con un dibujo · se siguen paso a paso con el "
      "dedo · son deterministas (misma entrada, mismo recorrido) · los dos se traducen a Python con for e if.",
      12.5, "14532D")
cols_fa = [("", 2.6), ("Diagrama de flujo", 4.8), ("Autómata finito", 4.8)]
encabezados(l.shapes, 0.55, 2.8, cols_fa, 0.4, tam=12)
dif = [("Una figura es…", "una **acción**: «haz esto»", "una **situación**: «estoy aquí»"),
       ("Una flecha dice…", "cuál es el siguiente paso (o sí / no de una condición)",
        "a dónde voy **si leo** cierto símbolo"),
       ("Memoria", "todas las variables que necesites", "**sólo** el estado actual"),
       ("Termina…", "al llegar a «Fin»", "cuando se acaba la cadena"),
       ("Resultado", "cualquier cosa: números, texto, listas…", "SÍ o NO (acepta o rechaza), o el estado final"),
       ("Se usa para…", "diseñar cualquier programa", "reconocer patrones y controlar sistemas con estados")]
for i, (a_, b_, c_) in enumerate(dif):
    g = m.grupo(l)
    renglon(g.shapes, 0.55, 3.2 + i * 0.55, [(a_, 2.6), (b_, 4.8), (c_, 4.8)], 0.55, tam=12,
            negritas={0: True}, colores={0: AZUL_OSC}, alinear={1: "l", 2: "l"})
    m.clic(l, g)

# =====================================================================================
# 17 · Validar un entero + regex + léxico
l = m.lamina("Un autómata útil: ¿es un número entero válido?",
             "Signo opcional y luego uno o más dígitos: \"-42\", \"+7\" y \"2026\" sí; \"4-2\", \"+\" y \"\" no.",
             notas=("Este es el tipo de autómata que corre cuando un formulario te dice «formato inválido». "
                    "Recorrer cada cadena en el diagrama con el grupo antes de revelar."))
estado(l.shapes, 1.3, 3.15, 0.55, "inicio", False, BLANCO, AZUL_OSC, 12)
estado(l.shapes, 3.9, 2.3, 0.55, "signo", False, BLANCO, AZUL_OSC, 12)
estado(l.shapes, 6.5, 3.15, 0.6, "dígitos", True, VERDE_CL, VERDE, 12)
estado(l.shapes, 3.9, 4.7, 0.55, "error", False, ROJO_CL, ROJO, 12)
flecha(l.shapes, 0.3, 3.15, 0.75, 3.15, MARINO, 2)
flecha(l.shapes, 1.78, 2.85, 3.38, 2.45, MARINO, 2)
texto(l.shapes, 2.05, 2.3, 1.0, 0.3, "+  −", 13, AZUL, True, "c", fuente=MONO)
flecha(l.shapes, 1.86, 3.15, 5.9, 3.15, MARINO, 2)
texto(l.shapes, 3.3, 3.18, 1.6, 0.3, "dígito", 12, AZUL, True, "c")
flecha(l.shapes, 4.42, 2.5, 6.0, 2.9, MARINO, 2)
texto(l.shapes, 4.75, 2.3, 1.2, 0.3, "dígito", 12, AZUL, True, "c")
bucle(l.shapes, 6.5, 3.15, 0.6, "dígito", 90, rb=0.38, tam=12, fuente=SANS)
flecha(l.shapes, 1.6, 3.62, 3.4, 4.5, ROJO, 1.5, punteada=True)
flecha(l.shapes, 6.0, 3.55, 4.42, 4.5, ROJO, 1.5, punteada=True)
texto(l.shapes, 4.55, 4.1, 2.6, 0.5, "cualquier otro símbolo\n(y ahí se queda)", 11, ROJO, alinear="c")
encabezados(l.shapes, 7.75, 1.6, [("Cadena", 1.3), ("Termina en", 1.6), ("¿Válida?", 2.1)], 0.38)
casos = [('"-42"', "dígitos", "✓ sí", VERDE), ('"2026"', "dígitos", "✓ sí", VERDE),
         ('"+"', "signo", "✗ no (falta dígito)", ROJO), ('"4-2"', "error", "✗ no", ROJO),
         ('""', "inicio", "✗ no (vacía)", ROJO)]
for i, (c, t, v, col) in enumerate(casos):
    g = m.grupo(l)
    renglon(g.shapes, 7.75, 1.98 + i * 0.44, [(c, 1.3), (t, 1.6), (v, 2.1)], 0.44, tam=12,
            colores={2: col}, negritas={2: True}, fuente=(0,))
    m.clic(l, g)
g = m.grupo(l)
caja(g.shapes, 0.55, 5.35, 6.0, 1.2, PIZARRA, None)
texto(g.shapes, 0.8, 5.47, 5.6, 0.25, "Expresión regular (Stephen Kleene, matemático estadounidense, 1956)", 11, GRIS, True)
texto(g.shapes, 0.8, 5.8, 5.6, 0.4, "^[+-]?[0-9]+$", 22, "CE9178", fuente=MONO)
texto(g.shapes, 3.85, 5.9, 2.6, 0.5, "el mismo autómata en\nuna línea (ver siguiente)", 11, "CBD5E1")
caja(g.shapes, 6.75, 5.35, 6.0, 1.2, FONDO, BORDE)
texto(g.shapes, 6.95, 5.47, 5.6, 0.25, "Análisis léxico (Clase 4): el intérprete corta tu código en piezas", 11, AZUL, True)
texto(g.shapes, 6.95, 5.8, 5.6, 0.7, "total = precio * 2   →   [nombre total] [=] [nombre precio] [*] "
      "[número 2]", 11.5, AZUL_OSC, fuente=MONO)
m.clic(l, g)

# =====================================================================================
# 17b · Una expresión regular es un autómata
l = m.lamina("Una expresión regular es un autómata escrito en una línea",
             "Stephen Kleene (matemático estadounidense) demostró en 1956: toda expresión regular equivale a un "
             "autómata finito.", notas=(
    "Teorema de Kleene. Ir pieza por pieza: cada clic ilumina una parte de la expresión y la parte del autómata "
    "que le corresponde. Cuando usas una expresión regular en un programa (por ejemplo, el módulo re de Python), "
    "el programa la convierte en un autómata y luego recorre tu texto símbolo por símbolo, igual que nuestro for."))
piezas_re = [("^", GRIS), ("[+-]?", AMBAR), ("[0-9]", AZUL), ("+", VERDE), ("$", MORADO)]
caja(l.shapes, 0.55, 1.6, 7.0, 0.95, PIZARRA, None)
tb = texto(l.shapes, 0.8, 1.78, 6.5, 0.6, "", 30, alinear="c")
p_ = tb.text_frame.paragraphs[0]
from presentaciones import _fuente
for t_, col_ in piezas_re:
    r_ = p_.add_run(); r_.text = t_ + " "
    _fuente(r_, 30, {"B45309": "FBBF24", "2563EB": "60A5FA", "15803D": "4ADE80", "6D28D9": "C4B5FD"}.get(col_, col_),
            True, MONO)
encabezados(l.shapes, 0.55, 2.75, [("Pieza", 1.2), ("Se lee", 2.6), ("En el autómata", 3.2)], 0.38, tam=11.5)
filas_re = [("^", "aquí empieza la cadena", "el estado **inicio** (la flecha que entra)", GRIS),
            ("[+-]?", "un + o un −, **opcional** (el ? = 0 o 1 vez)", "la flecha inicio → signo; también "
             "se puede saltar", AMBAR),
            ("[0-9]", "**un** dígito, del 0 al 9", "la flecha que llega a **dígitos**", AZUL),
            ("+", "**una o más** veces lo anterior", "el **bucle** de dígitos: otro dígito y te quedas", VERDE),
            ("$", "aquí termina la cadena", "al acabar debes estar en el **doble círculo**", MORADO)]
for i, (pz, lee, aut, col_) in enumerate(filas_re):
    renglon(l.shapes, 0.55, 3.13 + i * 0.46, [("", 1.2), ("", 2.6), ("", 3.2)], 0.46)
# autómata de la derecha
caja(l.shapes, 7.8, 1.6, 4.95, 3.83, FONDO, BORDE)
estado(l.shapes, 8.6, 3.95, 0.42, "inicio", False, BLANCO, AZUL_OSC, 10.5)
estado(l.shapes, 10.2, 2.75, 0.42, "signo", False, BLANCO, AZUL_OSC, 10.5)
estado(l.shapes, 11.95, 3.95, 0.47, "dígitos", True, VERDE_CL, VERDE, 10.5)
flecha(l.shapes, 7.9, 3.95, 8.18, 3.95, MARINO, 2)
flecha(l.shapes, 8.95, 3.7, 9.82, 2.98, MARINO, 2)
flecha(l.shapes, 9.02, 3.95, 11.48, 3.95, MARINO, 2)
flecha(l.shapes, 10.58, 2.95, 11.55, 3.68, MARINO, 2)
bucle(l.shapes, 11.95, 3.95, 0.47, angulo=90, rb=0.3)
texto(l.shapes, 7.95, 4.95, 4.7, 0.4, "(sin dibujar el estado de error)", 10, TENUE, alinear="c")
etiquetas_aut = [("^", 7.85, 3.4, GRIS), ("+ −", 8.7, 2.95, AMBAR), ("[0-9]", 9.75, 4.03, AZUL),
                 ("[0-9]", 10.75, 2.85, AZUL), ("+", 11.5, 2.65, VERDE), ("$", 11.5, 4.45, MORADO)]
for i, (pz, lee, aut, col_) in enumerate(filas_re):
    g = m.grupo(l)
    y = 3.13 + i * 0.46
    caja_texto(g.shapes, 0.55, y, 1.2, 0.46, pz, 15, col_, BLANCO, BORDE, True, fuente=MONO, redondeo=0)
    texto(g.shapes, 1.85, y + 0.04, 2.45, 0.4, lee, 10.5, TEXTO, ancla="m")
    texto(g.shapes, 4.45, y + 0.04, 3.05, 0.4, aut, 10.5, TEXTO, ancla="m")
    for et, ex, ey, ec in etiquetas_aut:
        if ec == col_:
            caja_texto(g.shapes, ex, ey, 0.9, 0.32, et, 12, BLANCO, ec, None, True, fuente=MONO, redondeo=0.2)
    m.clic(l, g)
g = m.grupo(l)
caja(g.shapes, 0.55, 5.6, 12.2, 0.95, MARINO, None)
texto(g.shapes, 0.85, 5.68, 11.6, 0.8, "La CURP: **[A-Z]{4}** quiere decir «exactamente 4 letras» ({n} = n veces): "
      "4 estados en fila, uno por letra. Toda la CURP es un autómata de 19 estados en fila (más el de error). "
      "Otros símbolos: «*» = cero o más veces · «[ ]» = uno de los símbolos de adentro.", 12.5, BLANCO, ancla="m")
m.clic(l, g)

# =====================================================================================
# 3 · Vistazo al mundo laboral
l = m.lamina("Vistazo al mundo laboral", "Lo que acabamos de ver se usa todos los días en el trabajo, aunque "
             "nadie le diga «autómata».", notas=(
    "Para que vean que el tema no es sólo historia. Diseñar la máquina de estados de un pedido es una "
    "pregunta clásica en entrevistas de diseño de sistemas. Las expresiones regulares se usan en "
    "validación de formularios, análisis de logs y limpieza de datos."))
cards = [("Validar datos", "¿La CURP, el RFC o el correo tienen el formato correcto? Se revisa con una "
          "**expresión regular** (un patrón que describe cómo debe verse un texto). Por dentro, es un autómata."),
         ("Pedidos y pagos", "Un pedido pasa por estados: creado → pagado → enviado → entregado "
          "(o cancelado). Apps de comida, bancos y paqueterías los modelan así."),
         ("Compiladores y editores", "El primer paso de un compilador (Clase 4) es un autómata que corta "
          "tu código en piezas. VS Code lo usa para colorear tu código."),
         ("Juegos, cajeros y semáforos", "Un enemigo que patrulla, persigue o huye; un cajero que pide "
          "tarjeta, NIP y monto: estados y transiciones.")]
for i, (t, c) in enumerate(cards):
    tarjeta(l.shapes, 0.55 + i * 3.08, 1.55, 2.9, 2.15, t, c, tam=11.5)
caja(l.shapes, 0.55, 3.95, 12.2, 1.55, PIZARRA, None, 0.08)
texto(l.shapes, 0.8, 4.08, 11.7, 0.2, "Ejemplo real: formato de la CURP (simplificado) como expresión regular · léela pieza por pieza, como en la lámina anterior", 11, GRIS, True)
texto(l.shapes, 0.8, 4.42, 11.7, 0.4, "^[A-Z]{4}[0-9]{6}[HM][A-Z]{5}[A-Z0-9][0-9]$", 22, "CE9178", fuente=MONO)
texto(l.shapes, 0.8, 4.98, 11.7, 0.4, "4 letras · 6 dígitos de la fecha · sexo · 5 letras (estado y consonantes) · "
      "homoclave · dígito verificador", 12, "CBD5E1")
caja(l.shapes, 0.55, 5.7, 12.2, 0.9, AZUL_CL, None)
texto(l.shapes, 0.8, 5.85, 11.7, 0.6, "En entrevistas: **«Diseña los estados de un pedido de Uber Eats»** "
      "o **«Valida este formato sin usar librerías»**. Las dos se resuelven con lo de hoy.", 13, AZUL_OSC)

# =====================================================================================
# 18 · Límite del autómata finito + jerarquía
l = m.lamina("Lo que un autómata finito NO puede hacer",
             "¿Están balanceados los paréntesis de \"(()(()))\"? Para saberlo hay que contar, y contar sin "
             "límite necesita memoria sin límite.", notas=(
    "Con k estados sólo puedes contar hasta k niveles de anidación. Siempre existe una cadena con más "
    "niveles. Por eso Python usa una pila (autómata de pila) para revisar paréntesis y bloques. "
    "Chomsky, 1956: jerarquía de lenguajes."))
tarjeta(l.shapes, 0.55, 1.6, 4.6, 2.2, "Con 3 estados cuento hasta 2 niveles",
        "estado «0 abiertos», «1 abierto», «2 abiertos»…\nCon \"(((\" ya no me alcanzan los estados. "
        "Y siempre habrá una cadena con un nivel más que mis estados.", tam=12.5)
g = m.grupo(l)
tarjeta(g.shapes, 0.55, 4.0, 4.6, 2.5, "La salida: darle memoria", "Un **autómata de pila** puede apilar "
        "cada «(» y quitar una con cada «)». Una **máquina de Turing** tiene una cinta infinita: "
        "puede escribir, borrar y regresar.", relleno=AZUL_CL, borde=None, color_titulo=AZUL_OSC, tam=12.5)
m.clic(l, g)
niveles = [("Máquina de Turing", "cinta infinita · lee, escribe y regresa", "cualquier algoritmo", "EDE9FE", MORADO),
           ("Autómata de pila", "estados + una pila", "paréntesis, la gramática de Python", "DBEAFE", AZUL_OSC),
           ("Autómata finito", "sólo estados", "CURP, correos, tokens, torniquete", "DCFCE7", VERDE)]
for i, (t, mem, ej, f, col) in enumerate(niveles):
    g = m.grupo(l)
    x = 5.45 + i * 0.45
    y = 1.6 + i * 0.95
    caja(g.shapes, x, y, 7.3 - i * 0.9, 4.9 - i * 1.4, f, col, 0.1, grosor=1.5)
    texto(g.shapes, x + 0.2, y + 0.12, 6.8 - i * 0.9, 0.3, t, 14, col, True)
    texto(g.shapes, x + 0.2, y + 0.42, 6.8 - i * 0.9, 0.3, f"Memoria: {mem}. Ej.: {ej}.", 11, TEXTO)
    m.clic(l, g)
texto(l.shapes, 5.45, 6.6, 7.3, 0.2, "Jerarquía de Chomsky (Noam Chomsky, lingüista estadounidense, 1956), simplificada: clasifica los lenguajes "
      "según la memoria que necesita la máquina. Cada una reconoce todo lo de las de adentro y más.", 10, TENUE)

# =====================================================================================
# 19 · Separador 3
m.separador("3 de 4", "La máquina de Turing", "Una cinta, un cabezal y una tabla de reglas. Con eso se puede "
            "calcular todo lo que tu laptop calcula.", ACENTOS[2])

# =====================================================================================
# 20 · Turing 1936
l = m.lamina("1936 · Alan Turing: ¿qué hace una persona cuando calcula?",
             "Para demostrar que algo NO se puede calcular, primero tenía que definir qué es calcular.", notas=(
    "On Computable Numbers, with an Application to the Entscheidungsproblem. Recibido el 28 de mayo de 1936, "
    "publicado en Proceedings of the London Mathematical Society (1936-37). Turing tenía 23-24 años. "
    "En esa época «computer» era el nombre de un puesto de trabajo: personas que hacían cálculos a mano. "
    "Church llegó al mismo resultado meses antes con el cálculo lambda; ambas definiciones resultaron equivalentes."))
tarjeta(l.shapes, 0.55, 1.55, 4.0, 2.75, "Alan Turing · 1912–1954", "Matemático inglés. A los 24 años publicó el "
        "artículo «On Computable Numbers…» («Sobre los números computables»). En la Segunda Guerra Mundial "
        "ayudó a descifrar Enigma, la máquina con que el ejército alemán cifraba sus mensajes. El premio más "
        "importante de la computación es el Premio Turing.", etiqueta="UNIVERSIDAD DE CAMBRIDGE", tam=12)
caja(l.shapes, 0.55, 4.5, 4.0, 2.0, AMBAR_CL, None)
texto(l.shapes, 0.8, 4.65, 3.5, 1.8, "Dato: en 1936 una **«computadora»** era una **persona** cuyo trabajo "
      "era hacer cálculos a mano, siguiendo reglas.", 13, "78350F")
texto(l.shapes, 4.85, 1.55, 7.9, 0.3, "Su idea: quitarle a esa persona todo lo que no sea mecánico", 14, AZUL, True)
red = [("Papel cuadriculado", "→ una cinta dividida en celdas, tan larga como haga falta"),
       ("Ve un cuadro a la vez", "→ un cabezal que lee una celda"),
       ("Escribe o borra un símbolo", "→ el cabezal escribe"),
       ("Mueve la vista a un lado", "→ se mueve una celda a la izquierda o a la derecha"),
       ("«Estado de ánimo» finito", "→ un estado (como en el autómata)"),
       ("Sigue instrucciones", "→ una tabla: estado + símbolo ⇒ qué hacer")]
for i, (a, b) in enumerate(red):
    g = m.grupo(l)
    y = 1.98 + i * 0.73
    caja(g.shapes, 4.85, y, 7.9, 0.62, FONDO, BORDE)
    texto(g.shapes, 5.05, y + 0.18, 3.0, 0.3, a, 12.5, MARINO, True)
    texto(g.shapes, 8.0, y + 0.18, 4.7, 0.3, b, 12, TEXTO)
    m.clic(l, g)

# =====================================================================================
# 21 · Componentes
l = m.lamina("Las piezas de una máquina de Turing", "La diferencia con el autómata: puede escribir y "
             "regresar. Su memoria (la cinta) no tiene límite.")
cinta(l.shapes, 2.2, 2.25, [BLANCO_CINTA, "1", "0", "1", "1", BLANCO_CINTA, BLANCO_CINTA, BLANCO_CINTA], 2, 0.75, 24)
texto(l.shapes, 1.3, 2.45, 0.8, 0.4, "···", 24, GRIS, alinear="c")
texto(l.shapes, 8.25, 2.45, 0.8, 0.4, "···", 24, GRIS, alinear="c")
s = l.shapes.add_shape(MSO_SHAPE.ISOSCELES_TRIANGLE, Inches(3.82), Inches(1.6), Inches(0.5), Inches(0.45))
s.rotation = 180; s.fill.solid(); s.fill.fore_color.rgb = rgb(AMBAR); s.line.fill.background(); s.shadow.inherit = False
caja_texto(l.shapes, 4.5, 1.6, 2.6, 0.45, "estado: derecha", 13, MARINO, AMBAR_CL, AMBAR, True, fuente=MONO)
texto(l.shapes, 9.3, 2.0, 3.4, 1.2, "□ = celda en blanco.\nLa celda amarilla es la que está leyendo el cabezal.", 12, TENUE)
piezas = [("Cinta", "Celdas con un símbolo cada una. Infinita hacia los dos lados: es la memoria."),
          ("Cabezal", "Lee la celda actual, escribe un símbolo y se mueve una celda (← o →)."),
          ("Estado", "Como en el autómata: en qué parte del trabajo va. Hay un estado especial, alto: ahí la máquina se detiene."),
          ("Tabla de reglas", "estado + símbolo leído ⇒ qué escribir, hacia dónde moverse y el estado nuevo.")]
for i, (t, c) in enumerate(piezas):
    tarjeta(l.shapes, 0.55 + i * 3.08, 3.55, 2.9, 1.75, t, c, tam=12, tam_titulo=15)
caja(l.shapes, 0.55, 5.55, 12.2, 0.95, MARINO, None)
texto(l.shapes, 0.85, 5.72, 11.6, 0.7, "Es determinista: para cada estado y símbolo hay **exactamente una** regla. "
      "Misma cinta inicial ⇒ mismos pasos ⇒ mismo resultado. Siempre.", 15, BLANCO)

# =====================================================================================
# 22 · Reglas sumar 1 + traza
l = m.lamina("Ejemplo: sumar 1 a un número binario", "1011 (once) + 1 = 1100 (doce). Igual que 199 + 1 = 200: "
             "los 1 del final se vuelven 0 y se «lleva» uno.", notas=(
    "Repaso express de binario: 1011 = 8 + 0 + 2 + 1 = 11. Primero la máquina camina a la derecha hasta el "
    "blanco; luego regresa sumando con acarreo. Cada clic es un paso; la celda amarilla es la del cabezal."))
caja(l.shapes, 0.55, 1.55, 4.55, 5.0, FONDO, BORDE)
texto(l.shapes, 0.75, 1.68, 4.2, 0.3, "Tabla de reglas", 13, AZUL, True)
encabezados(l.shapes, 0.7, 2.05, [("Estado", 1.15), ("Lee", 0.6), ("Escribe", 0.85), ("Mueve", 0.7), ("Nuevo", 0.95)], 0.34, tam=10.5)
reglas = [("derecha", "0", "0", "→", "derecha"), ("derecha", "1", "1", "→", "derecha"),
          ("derecha", "□", "□", "←", "sumar"), ("sumar", "1", "0", "←", "sumar"),
          ("sumar", "0", "1", "—", "alto"), ("sumar", "□", "1", "—", "alto")]
for i, f in enumerate(reglas):
    renglon(l.shapes, 0.7, 2.39 + i * 0.4, list(zip(f, (1.15, 0.6, 0.85, 0.7, 0.95))), 0.4, tam=11.5,
            relleno=BLANCO if i < 3 else "F5F3FF", fuente=MONO)
texto(l.shapes, 0.75, 4.9, 4.2, 1.6, "**derecha**: camina hasta el final del número.\n**sumar**: regresa; "
      "cada 1 se vuelve 0 y se «lleva» uno (acarreo) hasta encontrar un 0 o un blanco, que se vuelve 1.", 11.5, TEXTO)
encabezados(l.shapes, 5.35, 1.55, [("Paso", 0.6), ("Estado", 1.05), ("Cinta", 3.25), ("Qué hace", 2.5)], 0.34, tam=10.5)
B = BLANCO_CINTA
pasos = [("0", "derecha", [B, "1", "0", "1", "1", B], 1, "inicio"),
         ("1", "derecha", [B, "1", "0", "1", "1", B], 2, "lee 1 · →"),
         ("2", "derecha", [B, "1", "0", "1", "1", B], 3, "lee 0 · →"),
         ("3", "derecha", [B, "1", "0", "1", "1", B], 4, "lee 1 · →"),
         ("4", "derecha", [B, "1", "0", "1", "1", B], 5, "lee 1 · →"),
         ("5", "sumar", [B, "1", "0", "1", "1", B], 4, "lee □ · ← a sumar"),
         ("6", "sumar", [B, "1", "0", "1", "0", B], 3, "lee 1 · escribe 0 · ←"),
         ("7", "sumar", [B, "1", "0", "0", "0", B], 2, "lee 1 · escribe 0 · ←"),
         ("8", "alto", [B, "1", "1", "0", "0", B], 2, "lee 0 · escribe 1 · alto")]
for i, (p, e, c, cab, q) in enumerate(pasos):
    g = m.grupo(l)
    y = 1.89 + i * 0.5
    renglon(g.shapes, 5.35, y, [(p, 0.6), (e, 1.05), ("", 3.25), (q, 2.5)], 0.5, tam=11,
            colores={1: AZUL if e != "alto" else VERDE}, negritas={1: True}, fuente=(1,))
    cinta(g.shapes, 5.35 + 0.6 + 1.05 + 0.2, y + 0.07, c, cab, 0.36, 12)
    m.clic(l, g)
g = m.grupo(l)
caja(g.shapes, 5.35, 6.42, 7.4, 0.5, VERDE_CL, None)
texto(g.shapes, 5.55, 6.53, 7.0, 0.3, "Resultado en la cinta: **1100** = 8 + 4 = 12 ✓", 13, "14532D")
m.clic(l, g)

# =====================================================================================
# 23 · Simulador en Python
l = m.lamina("Una máquina de Turing en Python", "Las reglas son un diccionario. El while es la máquina: "
             "lee, escribe, se mueve y cambia de estado hasta llegar a «alto».", notas=(
    "Precondición: la cinta empieza y termina con un blanco, y el cabezal empieza en la posición 1. "
    "Lo importante: si cambio el diccionario, el MISMO while ejecuta otra máquina. Las reglas (el programa) "
    "son datos. Esa es la máquina universal de Turing y la idea de von Neumann."))
codigo(l.shapes, 0.55, 1.55, 7.6, 4.95, '''reglas = {
    "derecha": {"0": ["0", 1, "derecha"],
                "1": ["1", 1, "derecha"],
                " ": [" ", -1, "sumar"]},
    "sumar":   {"1": ["0", -1, "sumar"],
                "0": ["1", 0, "alto"],
                " ": ["1", 0, "alto"]},
}

def ejecutar_maquina_turing(lista_cinta, reglas):
    estado = "derecha"
    posicion = 1
    while estado != "alto":
        simbolo = lista_cinta[posicion]
        regla = reglas[estado][simbolo]
        lista_cinta[posicion] = regla[0]
        posicion = posicion + regla[1]
        estado = regla[2]
    return lista_cinta''', 12.5)
tarjeta(l.shapes, 8.4, 1.55, 4.35, 1.5, "Llamada", "", tam=11)
texto(l.shapes, 8.6, 1.92, 4.0, 1.0, 'cinta = [" ", "1", "0", "1", "1", " "]\n'
      'ejecutar_maquina_turing(cinta, reglas)\n→ [" ", "1", "1", "0", "0", " "]', 10.5, AZUL_OSC, fuente=MONO)
g = m.grupo(l)
tarjeta(g.shapes, 8.4, 3.25, 4.35, 1.5, "regla = [escribe, mueve, nuevo]", "mueve: 1 = derecha, −1 = izquierda, "
        "0 = no se mueve. El blanco □ es \" \".", tam=11.5)
m.clic(l, g)
g = m.grupo(l)
caja(g.shapes, 8.4, 4.95, 4.35, 1.55, MARINO, None)
texto(g.shapes, 8.6, 5.08, 4.0, 1.4, "Cambia el diccionario y el **mismo while** ejecuta **otra** máquina. "
      "El programa también es un dato.", 14, BLANCO)
m.clic(l, g)

# =====================================================================================
# 24 · Church-Turing + Turing-completo
l = m.lamina("La tesis de Church–Turing", "Alonzo Church (lógico estadounidense) y Alan Turing: todo lo que se "
             "puede calcular con un algoritmo, lo puede calcular una máquina de Turing.", notas=(
    "Es una tesis, no un teorema: no se puede demostrar porque «algoritmo» en sentido intuitivo no es un objeto "
    "matemático. Pero nadie ha encontrado un contraejemplo en 90 años. "
    "PowerPoint: Tom Wildenhain, 2017. Magic: Churchill, Biderman y Herrick, 2019."))
caja(l.shapes, 0.55, 1.75, 12.2, 1.25, MARINO, None)
texto(l.shapes, 0.85, 1.85, 11.6, 1.05, "Tu laptop, tu celular, Python y una máquina de Turing pueden calcular "
      "**exactamente las mismas cosas** (si tienen memoria suficiente); cambia la velocidad. Es una **tesis** y no "
      "un teorema: no se puede demostrar, pero en 90 años nadie ha encontrado un caso que la contradiga.", 15, BLANCO)
texto(l.shapes, 0.55, 3.2, 12, 0.3, "«Turing-completo»: puede simular cualquier máquina de Turing. Algunos "
      "lo son sin querer:", 13, AZUL, True)
tc = [("Python, Java, C", "Con variables, if y while ya basta."), ("Excel", "Desde 2021, con LAMBDA: una función para crear tus propias funciones."),
      ("Minecraft", "Con circuitos de redstone se han construido computadoras completas."),
      ("PowerPoint", "Sólo con animaciones al hacer clic (Tom Wildenhain, estudiante de Carnegie Mellon, 2017)."),
      ("Magic: The Gathering", "Un juego de cartas, demostrado en 2019.")]
for i, (t, c) in enumerate(tc):
    g = m.grupo(l)
    tarjeta(g.shapes, 0.55 + i * 2.46, 3.6, 2.3, 2.0, t, c, tam=11.5, tam_titulo=13.5)
    m.clic(l, g)
g = m.grupo(l)
caja(g.shapes, 0.55, 5.8, 12.2, 0.75, AZUL_CL, None)
texto(g.shapes, 0.8, 5.95, 11.7, 0.5, "**Máquina universal**: una máquina de Turing que lee de la cinta las "
      "reglas de otra y la imita. Es la idea de tu computadora: un solo aparato, cualquier programa.", 13, AZUL_OSC)
m.clic(l, g)

# =====================================================================================
# 25 · Problema de la parada
l = m.lamina("El problema de la parada", "La plataforma corta tu código a los 10 segundos. ¿Por qué no revisa "
             "antes si tu while es infinito?", notas=(
    "Pregunta abierta al grupo antes del clic. Respuesta: porque es imposible escribir ese revisor para "
    "cualquier programa. No es falta de ingenio: está demostrado (Turing, 1936)."))
tarjeta(l.shapes, 0.55, 1.55, 6.0, 2.0, "Lo que nos gustaría tener", "Una función que, sin ejecutar el "
        "programa, diga si va a terminar:", tam=13)
texto(l.shapes, 0.75, 2.6, 5.7, 0.8, "es_ejecucion_finita(programa, entrada)\n→ True si termina, False si se cicla",
      12, AZUL_OSC, fuente=MONO)
tarjeta(l.shapes, 6.75, 1.55, 6.0, 2.0, "Sería útil", "Los editores te avisarían de ciclos infinitos, la "
        "plataforma no tendría que esperar 10 s y muchos bugs se detectarían solos.", tam=13)
g = m.grupo(l)
caja(g.shapes, 0.55, 3.8, 12.2, 2.7, MARINO, None)
texto(g.shapes, 0.85, 4.0, 11.6, 0.9, "Alan Turing, 1936: **esa función no puede existir.**", 28, "FDE68A", True)
texto(g.shapes, 0.85, 4.8, 11.6, 1.5, "No es que nadie la haya podido programar todavía: está demostrado que "
      "es imposible. Puedes revisar casos particulares, pero no hay un revisor que funcione para todos los "
      "programas. Por eso la plataforma, igual que tu sistema operativo, sólo puede poner un límite de tiempo.",
      15, BLANCO)
m.clic(l, g)

# =====================================================================================
# 26 · Demostración por contradicción
l = m.lamina("¿Por qué no puede existir? Una demostración por contradicción",
             "Por contradicción: suponer lo contrario y llegar a algo imposible. Supongamos que sí existe "
             "es_ejecucion_finita…", notas=(
    "Paso a paso. Suponer que existe es_ejecucion_finita. Construyo contradecir, que hace lo contrario de lo que "
    "la función predice. Le paso a contradecir su propio código. Cualquier respuesta es incorrecta. "
    "Es la misma autorreferencia de Gödel: «esta frase no se puede demostrar»."))
codigo(l.shapes, 0.55, 1.55, 6.6, 3.0, '''def contradecir(programa):
    if es_ejecucion_finita(programa, programa):
        while True:
            print("no termino")
    else:
        return "terminé"

contradecir(contradecir)''', 14)
texto(l.shapes, 0.55, 4.75, 6.6, 1.7, "Un programa es texto, así que puede ser la **entrada** de otro programa (la "
      "plataforma recibe tu código como texto). **contradecir** pregunta qué haría un programa si recibiera su "
      "propio código… y hace **lo contrario**. La última línea se lo pregunta **a sí misma**.", 14, TEXTO)
g1 = m.grupo(l)
tarjeta(g1.shapes, 7.4, 1.55, 5.35, 1.45, "Si la función responde True («termina»)", "contradecir entra al "
        "while True y nunca termina. **Se equivocó.**", relleno=ROJO_CL, borde=None, color_titulo=ROJO, tam=13)
g2 = m.grupo(l)
tarjeta(g2.shapes, 7.4, 3.15, 5.35, 1.45, "Si responde False («se cicla»)", "contradecir regresa "
        "\"terminé\": sí terminó. **Se equivocó otra vez.**", relleno=ROJO_CL, borde=None, color_titulo=ROJO, tam=13)
g3 = m.grupo(l)
caja(g3.shapes, 7.4, 4.75, 5.35, 1.75, VERDE_CL, None)
texto(g3.shapes, 7.6, 4.9, 4.95, 1.5, "Cualquier respuesta es incorrecta ⇒ la suposición era falsa ⇒ "
      "**es_ejecucion_finita no puede existir**. Así, Alan Turing respondió a David Hilbert: no hay un "
      "procedimiento que decida todo.", 13, "14532D")
for g_ in (g1, g2, g3):
    m.clic(l, g_)

# =====================================================================================
# 27 · Collatz
l = m.lamina("¿Termina o no? La conjetura de Collatz (1937)",
             "Si n es par, divídelo entre 2; si es impar, multiplícalo por 3 y súmale 1. ¿Siempre llegas a 1?",
             notas=("Conjetura de Collatz (Lothar Collatz, 1937). Se ha comprobado por computadora para todos los "
                    "números hasta más de 20 dígitos (≈ 2^68), pero no hay demostración. Nadie sabe si "
                    "contar_pasos_collatz termina para todo n. Ejemplo perfecto de que «¿termina?» puede ser "
                    "dificilísimo aun en 7 renglones."))
codigo(l.shapes, 0.55, 1.55, 6.3, 3.3, '''def contar_pasos_collatz(n):
    pasos = 0
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        pasos = pasos + 1
    return pasos''', 14)
g = m.grupo(l)
tarjeta(g.shapes, 7.1, 1.55, 5.65, 1.5, "contar_pasos_collatz(6) → 8", "6 → 3 → 10 → 5 → 16 → 8 → 4 → 2 → 1",
        tam=13)
m.clic(l, g)
g = m.grupo(l)
tarjeta(g.shapes, 7.1, 3.25, 5.65, 1.6, "contar_pasos_collatz(27) → 111", "Sube hasta 9,232 antes de bajar a 1. "
        "Con un número tan chico, 111 vueltas del while.", tam=13)
m.clic(l, g)
g = m.grupo(l)
caja(g.shapes, 0.55, 5.1, 12.2, 1.4, MARINO, None)
texto(g.shapes, 0.85, 5.27, 11.6, 1.1, "La propuso Lothar Collatz (matemático alemán). Es una **conjetura**: algo que "
      "parece cierto, pero nadie ha demostrado. Con computadoras se ha comprobado para números de **más de 20 "
      "dígitos**, y siempre llega a 1. Siete renglones de Python, y «¿termina?» sigue sin respuesta.", 14, BLANCO)
m.clic(l, g)

# =====================================================================================
# 28 · Gödel y Turing
l = m.lamina("Kurt Gödel y Alan Turing: la misma idea en dos mundos", "Autorreferencia (algo que habla de sí mismo) revela un límite.")
col = [("Kurt Gödel · 1931", "Matemáticas", "«Esta afirmación no se puede demostrar.»",
        "Hay verdades que un sistema de reglas no puede demostrar.", "FEF3C7", AMBAR),
       ("Alan Turing · 1936", "Computación", "contradecir(contradecir)",
        "Hay preguntas que ningún programa puede responder siempre.", "EDE9FE", MORADO)]
for i, (t, area, frase, res, f, c) in enumerate(col):
    x = 0.55 + i * 6.2
    caja(l.shapes, x, 1.55, 6.0, 2.6, f, None)
    texto(l.shapes, x + 0.25, 1.7, 5.5, 0.3, f"{t} · {area}", 14, c, True)
    texto(l.shapes, x + 0.25, 2.15, 5.5, 0.7, frase, 18, MARINO, True, fuente=MONO if i else SANS)
    texto(l.shapes, x + 0.25, 3.05, 5.5, 0.9, res, 14, TEXTO)
encabezados(l.shapes, 0.55, 4.4, [("Palabra", 2.5), ("Significa", 9.7)], 0.36)
vocab = [("Computable", "Existe un algoritmo que calcula el resultado."),
         ("Decidible", "Existe un algoritmo que, para cualquier entrada, termina y responde sí o no."),
         ("Indecidible", "No existe ese algoritmo: el problema de la parada es el ejemplo más famoso."),
         ("Respuesta a Hilbert", "No hay un procedimiento mecánico que decida todas las verdades (Alonzo Church y Alan Turing, 1936).")]
for i, (a, b) in enumerate(vocab):
    g = m.grupo(l)
    renglon(g.shapes, 0.55, 4.76 + i * 0.44, [(a, 2.5), (b, 9.7)], 0.44, tam=12.5, negritas={0: True},
            colores={0: AZUL_OSC}, alinear={1: "l"})
    m.clic(l, g)

# =====================================================================================
# 29 · Separador 4
m.separador("4 de 4", "von Neumann y el azar", "La máquina universal se vuelve aparato. Y una pregunta "
            "incómoda: si todo es determinista, ¿de dónde sale random?", ACENTOS[3])

# =====================================================================================
# 30 · von Neumann
l = m.lamina("1945 · John von Neumann: el programa vive en la memoria",
             "La máquina universal de Alan Turing, convertida en un diseño de ingeniería.", notas=(
    "First Draft of a Report on the EDVAC, 30 de junio de 1945, Moore School (Universidad de Pensilvania). "
    "Matiz: el diseño fue colaborativo; J. Presper Eckert y John Mauchly (creadores del ENIAC) también lo "
    "idearon, y se molestaron porque el reporte salió sólo con el nombre de von Neumann. "
    "Antes, el ENIAC se «programaba» reconectando cables."))
tarjeta(l.shapes, 0.55, 1.55, 4.0, 2.5, "John von Neumann · 1903–1957", "Matemático y físico húngaro-estadounidense, "
        "en Princeton. En 1945 escribió el reporte del EDVAC (una de las primeras computadoras electrónicas). "
        "Conoció a Alan Turing en Princeton.",
        etiqueta="«FIRST DRAFT … EDVAC» · 30 JUN 1945", tam=12)
tarjeta(l.shapes, 0.55, 4.25, 4.0, 2.25, "Antes: cables", "El ENIAC (1945, la primera computadora electrónica "
        "de uso general) se «programaba» reconectando cables a mano: cambiar de programa tomaba días. Ahora: cargar otro archivo.", relleno=AMBAR_CL,
        borde=None, color_titulo=AMBAR, tam=12)
caja(l.shapes, 4.85, 1.55, 7.9, 3.3, FONDO, BORDE)
caja_texto(l.shapes, 5.1, 1.8, 3.5, 2.75, "", 12, relleno=AZUL_CL, borde=AZUL)
texto(l.shapes, 5.25, 1.9, 3.2, 0.3, "CPU (procesador)", 14, AZUL_OSC, True, "c")
caja_texto(l.shapes, 5.3, 2.35, 3.1, 0.85, "Unidad de control\nlee la siguiente instrucción", 11.5, MARINO, BLANCO, AZUL)
caja_texto(l.shapes, 5.3, 3.4, 3.1, 0.85, "Unidad aritmética y lógica\nsuma, compara…", 11.5, MARINO, BLANCO, AZUL)
caja_texto(l.shapes, 9.4, 1.8, 3.1, 1.85, "**Memoria**\n\ninstrucciones\n(el programa)\n+ datos", 12, MARINO, VERDE_CL, VERDE)
caja_texto(l.shapes, 9.4, 3.85, 3.1, 0.7, "Entrada / salida", 12, MARINO, BLANCO, "94A3B8")
flecha(l.shapes, 8.65, 2.5, 9.35, 2.5, MARINO, 2)
flecha(l.shapes, 9.35, 2.95, 8.65, 2.95, MARINO, 2)
flecha(l.shapes, 8.65, 4.2, 9.35, 4.2, MARINO, 2)
g = m.grupo(l)
caja(g.shapes, 4.85, 5.05, 7.9, 1.45, MARINO, None)
texto(g.shapes, 5.1, 5.18, 7.4, 1.25, "Ciclo: **buscar** la instrucción → **decodificarla** → **ejecutarla** → "
      "repetir, miles de millones de veces por segundo. Tu archivo .py también es texto en memoria: "
      "el intérprete (Clase 4) es un programa que lee otro programa.", 13.5, BLANCO)
m.clic(l, g)

# =====================================================================================
# 31 · Determinismo
l = m.lamina("Todo algoritmo es determinista", "Misma entrada + mismo estado inicial ⇒ mismos pasos ⇒ mismo "
             "resultado. Entonces, ¿cómo funciona random?", notas=(
    "Demostración en vivo: pedir que todos corran el código en la ventana de Python de la plataforma. "
    "Todos obtendrán 1, 3, 5, 5, 6. Sin random.seed, Python toma la semilla de una fuente del sistema "
    "operativo (que mezcla, entre otras cosas, la hora y eventos del hardware), por eso parece distinto cada vez."))
codigo(l.shapes, 0.55, 1.55, 6.3, 2.6, '''import random

random.seed(2026)
for i in range(5):
    print(random.randint(1, 6))''', 15)
g = m.grupo(l)
caja(g.shapes, 7.1, 1.55, 5.65, 2.6, "0B1220", None)
texto(g.shapes, 7.35, 1.68, 5.2, 0.25, "Salida · en tu computadora y en la de todos", 11, GRIS, True)
texto(g.shapes, 7.35, 2.05, 5.2, 2.0, "1\n3\n5\n5\n6", 16, "D4D4D4", fuente=MONO)
texto(g.shapes, 9.2, 2.6, 3.4, 1.0, "Córrelo en la ventana de Python de la plataforma.", 12, "FDE68A")
m.clic(l, g)
g = m.grupo(l)
tarjeta(g.shapes, 0.55, 4.4, 6.0, 2.1, "Pseudoaleatorio", "Los números **parecen** al azar, pero salen de una "
        "**fórmula** que empieza en una **semilla** (seed). Misma semilla ⇒ misma lista, siempre.", tam=13,
        tam_titulo=15)
m.clic(l, g)
g = m.grupo(l)
tarjeta(g.shapes, 6.75, 4.4, 6.0, 2.1, "¿Y si no pongo semilla?", "Python toma una del sistema operativo "
        "(que mezcla la hora y ruido del hardware). Por eso cada vez sale distinto, pero la fórmula sigue "
        "siendo la misma.", tam=13, tam_titulo=15)
m.clic(l, g)

# =====================================================================================
# 32 · Cuadrados medios
l = m.lamina("1946 · Cuadrados medios: el algoritmo de John von Neumann",
             "Algoritmo para números «al azar»: eleva al cuadrado, rellena a 8 dígitos y toma los 4 de en medio. Repite.", notas=(
    "Para las simulaciones del proyecto Manhattan necesitaban millones de números al azar (método Monte Carlo). "
    "La frase es de 1951: «Anyone who considers arithmetical methods of producing random digits is, of course, "
    "in a state of sin.» La semilla 2500 se atora para siempre: 2500² = 06250000."))
encabezados(l.shapes, 0.55, 1.6, [("Paso", 0.8), ("Número", 1.4), ("Al cuadrado (8 dígitos)", 2.6), ("Los 4 de en medio", 2.2)], 0.4)
cm = [("0", "1234", "01522756", "5227"), ("1", "5227", "27321529", "3215"), ("2", "3215", "10336225", "3362"),
      ("3", "3362", "11303044", "3030"), ("4", "3030", "09180900", "1809")]
for i, (p, n, c, r) in enumerate(cm):
    g = m.grupo(l)
    y = 2.0 + i * 0.48
    renglon(g.shapes, 0.55, y, [(p, 0.8), (n, 1.4), ("", 2.6), (r, 2.2)], 0.48, tam=14, fuente=(1, 3),
            colores={3: AZUL}, negritas={3: True})
    tb = texto(g.shapes, 2.75, y + 0.11, 2.6, 0.3, "", 14, alinear="c")
    p_ = tb.text_frame.paragraphs[0]
    for t_, col_ in ((c[:2], GRIS), (c[2:6], AZUL), (c[6:], GRIS)):
        r_ = p_.add_run(); r_.text = t_
        _ = col_
        from presentaciones import _fuente
        _fuente(r_, 14, col_, col_ == AZUL, MONO)
    m.clic(l, g)
texto(l.shapes, 0.55, 4.5, 7.0, 0.3, "Secuencia: 5227, 3215, 3362, 3030, 1809… parecen al azar.", 13, TEXTO)
g = m.grupo(l)
tarjeta(g.shapes, 0.55, 4.95, 7.0, 1.55, "El problema: se atora", "Con la semilla 2500: 2500² = 06250000 → 2500 → "
        "2500 → 2500… para siempre. Tarde o temprano, toda secuencia así se repite.",
        relleno=ROJO_CL, borde=None, color_titulo=ROJO, tam=13)
m.clic(l, g)
g = m.grupo(l)
caja(g.shapes, 7.8, 1.6, 4.95, 4.9, MARINO, None)
texto(g.shapes, 8.1, 1.9, 4.4, 2.7, "«Quien considere métodos aritméticos para producir dígitos aleatorios "
      "está, por supuesto, en estado de pecado.»", 19, "FDE68A", True)
texto(g.shapes, 8.1, 4.75, 4.4, 1.6, "John von Neumann, 1951. Él mismo los usaba: sabía que no eran azar, "
      "pero eran rápidos y suficientes para sus simulaciones.", 12.5, "CBD5E1")
m.clic(l, g)

# =====================================================================================
# 33 · Generador congruencial en Python
l = m.lamina("Un generador pseudoaleatorio en Python", "Algoritmo «congruencial lineal» de Derrick Lehmer (matemático estadounidense, 1949): "
             "multiplica, suma y toma el residuo.", notas=(
    "Con números chicos (m = 16) se ve el ciclo: después de 16 números se repite. Python usa el Mersenne "
    "Twister (Matsumoto y Nishimura, 1997), que se repite después de 2¹⁹⁹³⁷ − 1 números: un número de "
    "más de 6,000 dígitos. Lehmer propuso el método congruencial en 1949."))
codigo(l.shapes, 0.55, 1.55, 7.2, 3.1, '''def generar_lista_pseudoaleatoria(semilla, cantidad):
    lista_numeros = []
    x = semilla
    for i in range(cantidad):
        x = (5 * x + 3) % 16
        lista_numeros.append(x)
    return lista_numeros''', 13.5)
tarjeta(l.shapes, 8.0, 1.55, 4.75, 1.4, "Llamada", "", tam=12)
texto(l.shapes, 8.2, 1.95, 4.4, 0.9, "generar_lista_pseudoaleatoria(7, 18)", 11.5, AZUL_OSC, fuente=MONO)
g = m.grupo(l)
caja(g.shapes, 0.55, 4.9, 12.2, 0.75, FONDO, BORDE)
nums = [6, 1, 8, 11, 10, 5, 12, 15, 14, 9, 0, 3, 2, 13, 4, 7, 6, 1]
for i, n in enumerate(nums):
    caja_texto(g.shapes, 0.75 + i * 0.66, 5.03, 0.58, 0.5, str(n), 15, MARINO if i < 16 else ROJO,
               BLANCO if i < 16 else ROJO_CL, BORDE if i < 16 else ROJO, i >= 16, fuente=MONO, redondeo=0.05)
m.clic(l, g)
g = m.grupo(l)
tarjeta(g.shapes, 8.0, 3.15, 4.75, 1.5, "Se repite", "Después de 16 números vuelve a empezar: 6, 1, 8… "
        "Con % 16 sólo hay 16 resultados posibles.", relleno=ROJO_CL, borde=None, color_titulo=ROJO, tam=12)
m.clic(l, g)
g = m.grupo(l)
caja(g.shapes, 0.55, 5.85, 12.2, 0.65, MARINO, None)
texto(g.shapes, 0.8, 5.98, 11.7, 0.45, "El random de Python usa el algoritmo Mersenne Twister (Makoto Matsumoto y Takuji "
      "Nishimura, matemáticos japoneses, 1997). También se repite… después de 2¹⁹⁹³⁷ − 1 números (más de 6,000 dígitos).", 14, BLANCO)
m.clic(l, g)

# =====================================================================================
# 34 · Azar de verdad
l = m.lamina("¿Y el azar de verdad?", "Un algoritmo no puede crear azar. Sólo puede simularlo… o medirlo "
             "del mundo físico.", notas=(
    "Minecraft: la misma semilla genera el mismo mundo (en la misma versión). Cloudflare: una pared de unas "
    "100 lámparas de lava en su oficina de San Francisco; una cámara la fotografía y la imagen se usa como "
    "fuente de entropía (LavaRand). Para contraseñas y llaves, Python tiene el módulo secrets, que usa la "
    "fuente del sistema operativo."))
az = [("Juegos: la semilla es el mundo", "En Minecraft, la misma semilla genera el mismo mundo. Los "
       "speedrunners (compiten por terminar un juego lo más rápido posible) estudian el generador para repetir la suerte.", AZUL_CL, AZUL_OSC),
      ("Seguridad: semilla adivinada = hackeo", "Si alguien adivina la semilla de tus contraseñas o llaves, "
       "adivina todas. Para eso se usa ruido físico, no una fórmula.", ROJO_CL, ROJO),
      ("Lámparas de lava", "Cloudflare (empresa que protege millones de sitios web) fotografía una pared de ~100 lámparas de lava y usa la imagen como "
       "fuente de azar para cifrar conexiones.", AMBAR_CL, AMBAR),
      ("Física cuántica", "Chips que miden fenómenos cuánticos, impredecibles por naturaleza. En 2026 ya se "
       "fabrican en silicio, del tamaño de una uña.", MORADO_CL, MORADO)]
for i, (t, c, f, col) in enumerate(az):
    g = m.grupo(l)
    tarjeta(g.shapes, 0.55 + (i % 2) * 6.2, 1.55 + (i // 2) * 2.05, 6.0, 1.85, t, c, relleno=f, borde=None,
            color_titulo=col, tam=13, tam_titulo=15)
    m.clic(l, g)
caja(l.shapes, 0.55, 5.75, 12.2, 0.75, MARINO, None)
texto(l.shapes, 0.8, 5.9, 11.7, 0.5, "Pseudoaleatorio: rápido y repetible (juegos, simulaciones). Aleatorio "
      "físico: impredecible (criptografía).", 14, BLANCO)

# =====================================================================================
# 35 · Práctica (índice)
l = m.lamina("Práctica", "En tu cuaderno. Primero resuelve; después revisamos con un clic.")
ej = [("1", "¿Acepta o rechaza?", "Con el autómata de la cantidad par de unos."),
      ("2", "Diseña un autómata", "Binarios que terminan en 0 (los números pares)."),
      ("3", "Ejecuta la máquina de Turing", "Sumar 1 a 0111."),
      ("4", "Cuadrados medios (algoritmo)", "Tres números con la semilla 2026, con el algoritmo de John von Neumann."),
      ("5", "¿Termina o no?", "Tres ciclos while.")]
for i, (n, t, c) in enumerate(ej):
    y = 1.6 + i * 0.97
    caja(l.shapes, 0.55, y, 12.2, 0.82, FONDO, BORDE)
    texto(l.shapes, 0.8, y + 0.17, 0.6, 0.5, n, 24, ACENTOS[i] if ACENTOS[i] != "FBBF24" else AMBAR, True)
    texto(l.shapes, 1.5, y + 0.25, 4.5, 0.4, t, 16, MARINO, True)
    texto(l.shapes, 6.0, y + 0.27, 6.6, 0.4, c, 14, TEXTO)

# =====================================================================================
# 36 · Ejercicios 1 y 2
l = m.lamina("Ejercicios 1 y 2 · Autómatas", "1: sigue el autómata de la cantidad par de unos. "
             "2: dibuja uno nuevo con dos estados.", notas=(
    "Ej. 2: el autómata sólo necesita recordar el último símbolo leído. Inicio en «termina en 1» "
    "(la cadena vacía no termina en 0). Con 0 vas a «termina en 0»; con 1, a «termina en 1»."))
encabezados(l.shapes, 0.55, 1.6, [("Cadena", 1.6), ("Unos", 1.0), ("Termina en", 1.5), ("Resultado", 1.6)], 0.4)
e1 = [('"0000"', "0", "par", "✓ acepta", VERDE), ('"111"', "3", "impar", "✗ rechaza", ROJO),
      ('""', "0", "par", "✓ acepta", VERDE), ('"1010"', "2", "par", "✓ acepta", VERDE),
      ('"1011"', "3", "impar", "✗ rechaza", ROJO)]
for i, (c, u, t, r, col) in enumerate(e1):
    renglon(l.shapes, 0.55, 2.0 + i * 0.46, [(c, 1.6), ("", 1.0), ("", 1.5), ("", 1.6)], 0.46, tam=13, fuente=(0,))
    g = m.grupo(l)
    texto(g.shapes, 2.15, 2.12 + i * 0.46, 1.0, 0.3, u, 13, TEXTO, alinear="c")
    texto(g.shapes, 3.15, 2.12 + i * 0.46, 1.5, 0.3, t, 13, TEXTO, alinear="c")
    texto(g.shapes, 4.65, 2.12 + i * 0.46, 1.6, 0.3, r, 13, col, True, "c")
    m.clic(l, g)
tarjeta(l.shapes, 6.75, 1.6, 6.0, 1.3, "Ejercicio 2", "Diseña un autómata que acepte los binarios que "
        "terminan en 0: \"10\", \"110\", \"0\" sí; \"1\", \"101\", \"\" no.", tam=12.5)
g = m.grupo(l)
caja(g.shapes, 6.75, 3.1, 6.0, 3.4, FONDO, BORDE)
estado(g.shapes, 8.2, 4.6, 0.65, "termina\nen 1", False, BLANCO, AZUL_OSC, 11)
estado(g.shapes, 11.3, 4.6, 0.65, "termina\nen 0", True, VERDE_CL, VERDE, 11)
flecha(g.shapes, 6.95, 4.6, 7.55, 4.6, MARINO, 2)
flecha(g.shapes, 8.85, 4.35, 10.65, 4.35, MARINO, 2)
texto(g.shapes, 9.5, 4.0, 0.5, 0.3, "0", 14, AZUL, True, "c", fuente=MONO)
flecha(g.shapes, 10.65, 4.85, 8.85, 4.85, MARINO, 2)
texto(g.shapes, 9.5, 4.9, 0.5, 0.3, "1", 14, AZUL, True, "c", fuente=MONO)
bucle(g.shapes, 8.2, 4.6, 0.65, "1", 90, rb=0.3)
bucle(g.shapes, 11.3, 4.6, 0.65, "0", 90, rb=0.3)
texto(g.shapes, 6.95, 5.7, 5.6, 0.75, "Sólo necesita recordar **el último símbolo**. Empieza en «termina en 1» "
      "porque la cadena vacía no termina en 0.", 11.5, TEXTO)
m.clic(l, g)

# =====================================================================================
# 37 · Ejercicios 3 y 4
l = m.lamina("Ejercicios 3 y 4 · Turing y von Neumann", "3: usa la tabla de reglas de sumar 1. "
             "4: el algoritmo de cuadrados medios con la semilla 2026.")
caja(l.shapes, 0.55, 1.55, 6.0, 4.95, FONDO, BORDE)
texto(l.shapes, 0.75, 1.68, 5.6, 0.3, "Ejercicio 3 · 0111 + 1", 14, AZUL, True)
encabezados(l.shapes, 0.7, 2.05, [("Paso", 0.55), ("Estado", 1.0), ("Cinta", 2.65), ("Hace", 1.5)], 0.32, tam=10)
e3 = [("0", "derecha", [B, "0", "1", "1", "1", B], 1, "inicio"),
      ("4", "derecha", [B, "0", "1", "1", "1", B], 5, "llegó a □"),
      ("5", "sumar", [B, "0", "1", "1", "1", B], 4, "regresa"),
      ("6", "sumar", [B, "0", "1", "1", "0", B], 3, "1 → 0"),
      ("7", "sumar", [B, "0", "1", "0", "0", B], 2, "1 → 0"),
      ("8", "sumar", [B, "0", "0", "0", "0", B], 1, "1 → 0"),
      ("9", "alto", [B, "1", "0", "0", "0", B], 1, "0 → 1 · alto")]
for i, (p, e, c, cab, q) in enumerate(e3):
    g = m.grupo(l)
    y = 2.37 + i * 0.45
    renglon(g.shapes, 0.7, y, [(p, 0.55), (e, 1.0), ("", 2.65), (q, 1.5)], 0.45, tam=10.5,
            colores={1: AZUL if e != "alto" else VERDE}, negritas={1: True}, fuente=(1,))
    cinta(g.shapes, 0.7 + 0.55 + 1.0 + 0.2, y + 0.07, c, cab, 0.32, 11)
    m.clic(l, g)
g = m.grupo(l)
texto(g.shapes, 0.75, 5.55, 5.6, 0.3, "0111 (siete) + 1 = **1000** (ocho). Los pasos 1 a 3 sólo caminan a la "
      "derecha.", 11.5, "14532D")
m.clic(l, g)
caja(l.shapes, 0.7, 5.9, 5.7, 0.5, BLANCO, BORDE)
texto(l.shapes, 0.82, 5.96, 5.5, 0.4, "**derecha**: con 0 o 1, deja igual y →; con □, ← y pasa a sumar.\n"
      "**sumar**: con 1, escribe 0 y ←; con 0 o □, escribe 1 y alto.", 10, TEXTO)
caja(l.shapes, 6.75, 1.55, 6.0, 4.95, FONDO, BORDE)
texto(l.shapes, 6.95, 1.68, 5.6, 0.3, "Ejercicio 4 · Semilla 2026", 14, AZUL, True)
encabezados(l.shapes, 6.9, 2.05, [("Número", 1.4), ("Al cuadrado", 2.2), ("En medio", 2.05)], 0.36, tam=11)
e4 = [("2026", "04104676", "1046"), ("1046", "01094116", "0941"), ("0941", "00885481", "8854")]
for i, (n, c, r) in enumerate(e4):
    renglon(l.shapes, 6.9, 2.41 + i * 0.5, [(n if i == 0 else "", 1.4), ("", 2.2), ("", 2.05)], 0.5, tam=14, fuente=(0,))
    g = m.grupo(l)
    if i:
        texto(g.shapes, 6.9, 2.53 + i * 0.5, 1.4, 0.3, n, 14, MARINO, alinear="c", fuente=MONO)
    texto(g.shapes, 8.3, 2.53 + i * 0.5, 2.2, 0.3, c, 14, TEXTO, alinear="c", fuente=MONO)
    texto(g.shapes, 10.5, 2.53 + i * 0.5, 2.05, 0.3, r, 14, AZUL, True, "c", fuente=MONO)
    m.clic(l, g)
g = m.grupo(l)
texto(g.shapes, 6.95, 4.15, 5.6, 2.2, "Números: **1046, 941, 8854**.\n\nOjo con 941: al cuadrado da 885,481, "
      "que tiene 6 dígitos. Por eso se rellena con ceros a la izquierda hasta tener 8: 00885481.", 12.5, TEXTO)
m.clic(l, g)

# =====================================================================================
# 38 · Ejercicio 5
l = m.lamina("Ejercicio 5 · ¿Termina o no?", "Haz la prueba de escritorio unos cuantos pasos. "
             "¿Puedes asegurar que termina?")
progs = [("a", "n = 10\nwhile n > 0:\n    n = n - 3", "✓ Termina", "10, 7, 4, 1, −2: en cuanto n ≤ 0 se detiene.", VERDE_CL, VERDE),
         ("b", "n = 10\nwhile n != 0:\n    n = n - 3", "✗ No termina", "10, 7, 4, 1, −2, −5… nunca vale "
          "exactamente 0. Un != en vez de > es un bug clásico.", ROJO_CL, ROJO),
         ("c", "contar_pasos_collatz(n)\n# para cualquier n ≥ 1", "? Nadie sabe", "Para todo número que se ha "
          "probado, sí termina. Pero no hay demostración.", AMBAR_CL, AMBAR)]
for i, (k, cod, r, ex, f, col) in enumerate(progs):
    x = 0.55 + i * 4.12
    texto(l.shapes, x, 1.6, 3.96, 0.3, f"Programa {k}", 14, MARINO, True)
    codigo(l.shapes, x, 1.95, 3.96, 1.55, cod, 13, etiqueta=None)
    g = m.grupo(l)
    caja(g.shapes, x, 3.7, 3.96, 2.1, f, None)
    texto(g.shapes, x + 0.2, 3.85, 3.56, 0.4, r, 17, col, True)
    texto(g.shapes, x + 0.2, 4.35, 3.56, 1.4, ex, 12.5, TEXTO)
    m.clic(l, g)
caja(l.shapes, 0.55, 6.0, 12.2, 0.55, AZUL_CL, None)
texto(l.shapes, 0.8, 6.1, 11.7, 0.35, "La a y la b se ven casi iguales. Para casos particulares sí se puede "
      "saber; lo imposible es un revisor que funcione para todos.", 12.5, AZUL_OSC)

# =====================================================================================
# 39 · Para llevar
l = m.oscura()
texto(l.shapes, 0.8, 0.55, 11, 0.6, "Para llevar", 30, BLANCO, True)
llevar = [("David Hilbert y Kurt Gödel", "Hilbert quería decidir todo mecánicamente; Gödel probó que hay verdades sin prueba."),
          ("Lenguaje formal", "Alfabeto (símbolos permitidos) + reglas exactas. Python es uno: SyntaxError = «no pertenece»."),
          ("Autómata finito", "Estados y transiciones; su única memoria es el estado. Toda expresión regular es uno."),
          ("Máquina de Turing", "Cinta + cabezal + estado + reglas. Calcula todo lo que tu laptop calcula."),
          ("Problema de la parada", "Ningún programa decide si cualquier programa termina."),
          ("John von Neumann y el azar", "El programa vive en memoria. random es pseudoaleatorio: fórmula + semilla.")]
for i, (t, c) in enumerate(llevar):
    x = 0.8 + (i % 3) * 3.95
    y = 1.6 + (i // 3) * 2.05
    caja(l.shapes, x, y, 3.75, 1.8, PIZARRA, None, 0.08)
    texto(l.shapes, x + 0.22, y + 0.2, 3.3, 0.3, t, 14, ACENTOS[i], True)
    texto(l.shapes, x + 0.22, y + 0.6, 3.3, 1.1, c, 12.5, "E2E8F0")
texto(l.shapes, 0.8, 5.95, 11.7, 0.8, "Un algoritmo es lo que puede hacer una máquina de Turing. Y saber "
      "qué NO puede hacer es tan importante como saber programar.", 16, "CBD5E1", alinear="c")

# =====================================================================================
salida = Path(sys.argv[1])
salida.parent.mkdir(parents=True, exist_ok=True)
m.guardar(str(salida))
Path(sys.argv[2] if len(sys.argv) > 2 else salida.with_suffix(".notas.json")).write_text(json.dumps(m.notas, ensure_ascii=False, indent=1))
print(len(m.prs.slides), "láminas ·", m.clics_totales(), "clics →", salida)
