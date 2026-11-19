"""Clase 21 · Jueves 19 de noviembre de 2026 · Aula.
Lenguajes formales, autómatas finitos (y cuándo no alcanzan) y la máquina de Turing.
El marco histórico quedó en herramientas/marco_historico_base.py para la siguiente sesión.

    python3 herramientas/clase_21.py sesiones/11_19/Clase_21_19_Nov_2026_Automatas_Turing_Pseudoaleatorios.pptx
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from presentaciones import *  # noqa: E402,F403

m = Mazo()
m.gifs = []  # (lámina, ruta, x, y, ancho) en pulgadas: se insertan en Keynote con AppleScript para que se animen
RECURSOS = Path(__file__).parent / "recursos"
if not all((RECURSOS / n).exists() for n in ("elevador.gif", "semaforo.gif")):
    import gifs_automatas
    RECURSOS.mkdir(exist_ok=True)
    gifs_automatas.generar_elevador(RECURSOS / "elevador.gif")
    gifs_automatas.generar_semaforo(RECURSOS / "semaforo.gif")
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
    "Hoy vemos la unidad 1 del programa (1.3 Autómatas y lenguajes formales, 1.4 Máquina de Turing), "
    "que dejé para ahora a propósito: ya que programan, la teoría se entiende mejor. "
    "La historia (David Hilbert, Kurt Gödel, Alan Turing, John von Neumann) va en la próxima sesión."))
texto(l.shapes, 0.8, 2.0, 7.0, 1.4, "¿Qué puede calcular\nuna máquina?", 40, BLANCO, True)
texto(l.shapes, 0.8, 3.55, 7.0, 0.5, "Lenguajes formales, autómatas finitos\ny la máquina de Turing", 16, "CBD5E1")
texto(l.shapes, 0.8, 4.45, 7.0, 0.3, "Clase 21 · Jueves 19 de noviembre de 2026 · Aula", 16, GRIS)
agenda = [("1", "Lenguajes formales", "alfabeto, regla, lenguaje"), ("2", "Autómatas finitos", "estados y transiciones"),
          ("3", "Del problema al código", "cómo conviven"), ("4", "Autómata de pila", "cuando contar no tiene tope"),
          ("5", "Máquina de Turing", "cinta, cabezal y reglas"), ("6", "Práctica", "situaciones reales")]
for i, (a, quien, idea) in enumerate(agenda):
    y = 1.35 + i * 0.78
    caja(l.shapes, 8.05, y, 4.75, 0.64, PIZARRA, None, 0.08)
    caja(l.shapes, 8.05, y, 0.09, 0.64, ACENTOS[i], None, 0)
    texto(l.shapes, 8.3, y + 0.2, 0.45, 0.25, a, 12, ACENTOS[i], True)
    texto(l.shapes, 8.75, y + 0.2, 2.2, 0.25, quien, 12.5, BLANCO, True)
    texto(l.shapes, 10.85, y + 0.23, 1.85, 0.2, idea, 10, GRIS, alinear="r")

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
tarjeta(g2.shapes, 6.75, 4.25, 6.0, 2.0, "2 · La defensa también usa estados",
        "Tu banco trata tu tarjeta como una máquina de estados: normal → bajo revisión (compra rara) → "
        "bloqueada (3 NIP incorrectos). Hoy diseñarás la del cajero en la práctica.", tam=11.5)
texto(l.shapes, 0.55, 6.5, 12.2, 0.2, "Fuentes: Scott Helme / Report URI, BleepingComputer, The Record, The Hacker "
      "News, Publimetro y Excélsior (17 nov 2026); PYMNTS (19 nov 2026); Kaspersky vía El CEO.", 9, GRIS)
m.clic(l, g1)
m.clic(l, g2)

# =====================================================================================
# 4 · Objetivo
l = m.lamina("Objetivo de la sesión", "Describir problemas con modelos exactos: qué tiene que recordar una máquina "
             "y qué tan poderosa tiene que ser.")
obj = [("1", "Lenguajes formales", "Alfabeto, cadena y lenguaje: decir con precisión qué va a leer la máquina."),
       ("2", "Autómatas", "Finitos y de pila: qué recuerdan, cuándo alcanza uno finito y cuándo hace falta una pila."),
       ("3", "Del problema al código", "Cómo conviven problema, autómata, diagrama de flujo y Python."),
       ("4", "Máquina de Turing", "Una cinta, un cabezal y reglas: el modelo de todo lo que tu computadora puede hacer.")]
for i, (n, t, c) in enumerate(obj):
    x = 0.55 + i * 3.08
    caja(l.shapes, x, 1.6, 2.9, 3.4, FONDO, BORDE)
    caja(l.shapes, x, 1.6, 2.9, 0.09, ACENTOS[i], None, 0)
    texto(l.shapes, x + 0.2, 1.85, 2.5, 0.6, n, 34, ACENTOS[i], True)
    texto(l.shapes, x + 0.2, 2.6, 2.5, 0.6, t, 15, MARINO, True)
    texto(l.shapes, x + 0.2, 3.3, 2.5, 1.6, c, 12, TEXTO)
caja(l.shapes, 0.55, 5.3, 12.2, 1.2, MARINO, None)
texto(l.shapes, 0.8, 5.47, 11.7, 0.9, "Programa de la materia · Unidad 1: 1.3 Autómatas y lenguajes formales · "
      "1.4 Máquina de Turing. La historia detrás (David Hilbert, Kurt Gödel, Alan Turing, John von Neumann) "
      "la vemos en la próxima sesión, cuando ya dominen las máquinas.", 14, BLANCO)

# =====================================================================================
# 5 · Recuerda la Clase 2
l = m.lamina("¿Qué es un algoritmo? Lo que dijimos en la Clase 2", "Una definición que funciona… "
             "hasta que alguien pregunta qué significa «claras».", notas=(
    "Preguntar al grupo: ¿quién decide si un paso es lo bastante claro? ¿«Sazona al gusto» es un paso? "
    "Hasta 1936 no existía una definición matemática de algoritmo; hoy la vamos a construir."))
caja(l.shapes, 0.55, 1.6, 12.2, 1.25, PIZARRA, None)
texto(l.shapes, 0.85, 1.83, 11.6, 0.9, "«Una lista ordenada de instrucciones **claras** y **finitas** que "
      "podemos seguir para resolver un problema.»", 22, BLANCO)
preg = [("¿Qué es «clara»?", "«Agrega sal al gusto» es clara para el autor de la receta, no para una máquina. "
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
texto(g.shapes, 0.8, 5.3, 11.7, 1.0, "Hasta 1936 nadie lo había definido con precisión. La respuesta es la **máquina "
      "de Turing**, y hoy llegamos a ella paso a paso: primero con máquinas más simples. "
      "La historia de cómo surgió, en la próxima sesión.", 15, "78350F")
for g_ in grupos + [g]:
    m.clic(l, g_)

# =====================================================================================
# S1 · Separador lenguajes
m.separador("1 de 5", "Lenguajes formales", "Antes de construir una máquina hay que decir, sin ambigüedad, "
            "qué va a leer.", ACENTOS[0])

# =====================================================================================
# LFW · Por qué surgen los lenguajes formales
l = m.lamina("¿Por qué surgen los lenguajes formales?",
             "Porque el lenguaje humano es ambiguo, y una máquina no puede adivinar qué quisiste decir.", notas=(
    "Leer los ejemplos en voz alta y pedir las dos interpretaciones. Las personas resolvemos la ambigüedad con el "
    "contexto; una máquina no tiene contexto. Datos: Gottlob Frege, Begriffsschrift (1879). Noam Chomsky, «Three "
    "models for the description of language», IRE Transactions on Information Theory (1956), y el libro Syntactic "
    "Structures (1957). John Backus dirigió FORTRAN en IBM (1957); en 1959 presentó en París una notación para "
    "describir ALGOL; Peter Naur la usó como editor del «Report on the Algorithmic Language ALGOL 60» (1960). "
    "De ahí el nombre BNF: Backus–Naur Form. El detalle histórico de las matemáticas va en la próxima sesión."))
tarjeta(l.shapes, 0.55, 1.55, 4.6, 3.35, "El problema: la ambigüedad", "«Vi a Juan con el telescopio».\n"
        "¿Quién tenía el telescopio: yo o Juan?\n\n«Juan le dijo a Pedro que su perro se escapó».\n"
        "¿El perro de quién?\n\nLo entendemos por contexto. Una máquina, no.", relleno=AMBAR_CL, borde=None,
        color_titulo=AMBAR, tam=12.5, tam_titulo=15)
quienes = [("1879 · Lógica · Gottlob Frege (lógico alemán)", "En su libro Begriffsschrift («Conceptografía») "
            "inventa símbolos y reglas para escribir razonamientos matemáticos sin ninguna ambigüedad.", AZUL_CL, AZUL_OSC),
           ("1956 · Lingüística · Noam Chomsky (lingüista estadounidense)", "En el artículo «Three models for the "
            "description of language» describe la gramática con **reglas de reemplazo** exactas y clasifica los "
            "lenguajes. Lo amplía en su libro Syntactic Structures (1957).", VERDE_CL, VERDE),
           ("1957 – 1960 · Programación · John Backus y Peter Naur", "Backus (IBM, estadounidense) dirige FORTRAN, "
            "uno de los primeros lenguajes de programación. Para el lenguaje **ALGOL 60** (reporte publicado en "
            "1960), él y Naur (programador danés) escriben las reglas con una notación exacta: la **BNF**.",
            MORADO_CL, MORADO)]
grupos_lfw = []
for i, (t, c, f, col) in enumerate(quienes):
    g = m.grupo(l)
    grupos_lfw.append(g)
    tarjeta(g.shapes, 5.35, 1.55 + i * 1.15, 7.4, 1.05, t, c, relleno=f, borde=None, color_titulo=col, tam=11)
g = m.grupo(l)
grupos_lfw.append(g)
caja(g.shapes, 0.55, 5.1, 12.2, 1.45, MARINO, None)
texto(g.shapes, 0.85, 5.18, 11.6, 1.3, "Un **lenguaje formal** tiene reglas tan exactas que una máquina puede decidir, "
      "**sin entender nada**, si un texto **pertenece** al lenguaje, es decir, si **cumple sus reglas**: ¿es Python "
      "válido? ¿tiene forma de CURP? En la siguiente lámina definimos cada palabra.", 14.5, BLANCO, ancla="m")
for g_ in grupos_lfw:
    m.clic(l, g_)

# =====================================================================================
# 12 · Lenguajes formales
l = m.lamina("Lenguajes formales: cuatro palabras", "Alfabeto, cadena, regla y lenguaje, en ese orden: cada una usa la "
             "anterior. Con ejemplos que ya usas todos los días.",
             notas=("Insistir en que «alfabeto» no significa abecedario: es lo que se permite escribir. El guion de "
                    "«55-1234-5678» no está en el alfabeto de los celulares, por eso esa cadena ni siquiera se puede "
                    "formar. Python es un lenguaje formal: el intérprete acepta o rechaza tu archivo."))
defs = [("1 · Alfabeto  Σ", "El **conjunto de símbolos** permitidos. No tiene que ser el abecedario. "
         "Σ (sigma, letra griega) es sólo su nombre.", "Celular: {0, 1, …, 9}\nContraseña: letras y dígitos"),
        ("2 · Cadena", "Símbolos del alfabeto puestos uno tras otro, como un str de Python. Puede ser vacía.",
         '"5512345678"\n"gato7"     ""'),
        ("3 · Regla", "La condición que una cadena debe cumplir para ser válida. También se le dice "
         "**gramática** o **patrón**.", "Celular: exactamente 10 dígitos\nContraseña: al menos un dígito"),
        ("4 · Lenguaje", "El conjunto de **todas** las cadenas que cumplen la regla. Una cadena **pertenece** "
         "al lenguaje si cumple la regla.", "Celulares válidos: {\"5512345678\", \"5598765432\", …}")]
grupos_lf = []
for i, (t, c, e) in enumerate(defs):
    g = m.grupo(l) if i else l
    if i:
        grupos_lf.append(g)
    x = 0.55 + i * 3.09
    tarjeta(g.shapes, x, 1.55, 2.95, 2.45, t, c, tam=11, tam_titulo=15)
    texto(g.shapes, x + 0.15, 3.25, 2.7, 0.65, e, 10.5, AZUL_OSC, True, fuente=MONO if i == 1 else SANS)
for g_ in grupos_lf:
    m.clic(l, g_)
g = m.grupo(l)
caja(g.shapes, 0.55, 4.2, 6.6, 2.3, FONDO, BORDE)
texto(g.shapes, 0.75, 4.3, 6.2, 0.3, "Ejemplo completo: celulares en México (10 dígitos)", 13, AZUL, True)
encabezados(g.shapes, 0.75, 4.68, [("Cadena", 2.1), ("¿Pertenece?", 1.2), ("Por qué", 2.9)], 0.34, tam=11)
cel = [('"5512345678"', "✓ sí", "10 dígitos", VERDE), ('"55-1234-5678"', "✗ no", "el guion no está en el alfabeto", ROJO),
       ('"551234"', "✗ no", "sólo tiene 6 dígitos", ROJO)]
for i, (c_, r_, p_, col_) in enumerate(cel):
    renglon(g.shapes, 0.75, 5.02 + i * 0.44, [(c_, 2.1), (r_, 1.2), (p_, 2.9)], 0.44, tam=11.5,
            colores={1: col_}, negritas={1: True}, fuente=(0,), alinear={2: "l"})
g2 = m.grupo(l)
caja(g2.shapes, 7.35, 4.2, 5.4, 2.3, PIZARRA, None)
texto(g2.shapes, 7.6, 4.32, 5.0, 0.3, "Python también es un lenguaje formal", 13, "93C5FD", True)
texto(g2.shapes, 7.6, 4.7, 5.0, 0.4, "if x > 3 print(x)", 14, "CE9178", fuente=MONO)
texto(g2.shapes, 7.6, 5.1, 5.0, 0.4, "SyntaxError: expected ':'", 12, "F87171", fuente=MONO)
texto(g2.shapes, 7.6, 5.5, 5.0, 0.95, "Un **SyntaxError** quiere decir: «esa cadena no pertenece al lenguaje». "
      "Lo decide una máquina, sin entender qué querías hacer.", 12, "E2E8F0")
m.clic(l, g)
m.clic(l, g2)

# =====================================================================================
# BNF · Cómo se escriben las reglas
l = m.lamina("¿Cómo se escriben las reglas? La notación BNF",
             "BNF = Backus–Naur Form, la «forma de Backus y Naur»: una manera exacta de escribir las reglas de un "
             "lenguaje. Ejemplo: los números enteros como \"-42\".", notas=(
    "Es la «notación exacta» de la lámina anterior. Leer cada regla en voz alta con el vocabulario de abajo: "
    "«un entero se forma con un signo y dígitos, o sólo con dígitos». La regla 3 se usa a sí misma: así dice "
    "«uno o más dígitos» sin escribir una regla para cada largo. La tabla de la derecha revisa \"-42\" de lo "
    "pequeño a lo grande: primero cada símbolo, luego los pedazos más grandes, hasta la cadena completa. "
    "En \"4-2\" falla porque el signo sólo puede ir al principio. La documentación oficial de Python publica la "
    "gramática completa del lenguaje con una notación de este tipo (Full Grammar specification)."))
caja(l.shapes, 0.55, 1.8, 6.0, 1.85, PIZARRA, None)
texto(l.shapes, 0.75, 1.88, 5.6, 0.25, "Las reglas del lenguaje «números enteros»", 11, GRIS, True)
reglas_bnf = ["1  <entero>  ::= <signo> <dígitos> | <dígitos>", "2  <signo>   ::= + | -",
              "3  <dígitos> ::= <dígito> | <dígito> <dígitos>", "4  <dígito>  ::= 0 | 1 | 2 | … | 9"]
texto(l.shapes, 0.75, 2.2, 5.7, 1.4, "\n".join(reglas_bnf), 13, "E2E8F0", fuente=MONO)
vocab_bnf = [("::=", "se lee «se forma con»"), ("|", "se lee «o»"), ("<nombre>", "una pieza que se define en "
             "su propia regla")]
for i, (sim, sig) in enumerate(vocab_bnf):
    x = 0.55 + i * 2.03
    caja(l.shapes, x, 3.8, 1.94, 1.25, FONDO, BORDE)
    texto(l.shapes, x + 0.1, 3.88, 1.74, 0.4, sim, 17, AZUL_OSC, True, "c", fuente=MONO)
    texto(l.shapes, x + 0.1, 4.33, 1.74, 0.7, sig, 11, TEXTO, alinear="c")
texto(l.shapes, 0.55, 5.15, 6.0, 0.4, "La regla 3 usa «<dígitos>» dentro de sí misma: así dice «uno o más dígitos» "
      "sin escribir una regla para cada largo.", 11, TENUE)
texto(l.shapes, 6.8, 1.8, 6.0, 0.3, "¿\"-42\" cumple las reglas? Se revisa de lo pequeño a lo grande:", 12.5, AZUL, True)
encabezados(l.shapes, 6.8, 2.15, [("Pedazo", 1.0), ("Es un…", 1.45), ("¿Por qué?", 3.5)], 0.34, tam=11)
revision = [('"-"', "<signo>", "regla 2: un signo es + o -"), ('"4"', "<dígito>", "regla 4: es uno del 0 al 9"),
            ('"2"', "<dígitos>", "regla 4 (es un <dígito>) y regla 3: un solo <dígito> ya es <dígitos>"),
            ('"42"', "<dígitos>", "regla 3: un <dígito> (4) seguido de <dígitos> (2)"),
            ('"-42"', "<entero>", "regla 1: un <signo> (-) seguido de <dígitos> (42) ✓")]
for i, (pz, es, por) in enumerate(revision):
    g = m.grupo(l)
    renglon(g.shapes, 6.8, 2.49 + i * 0.45, [(pz, 1.0), (es, 1.45), (por, 3.5)], 0.45, tam=11.5, fuente=(0, 1),
            alinear={2: "l"}, colores={1: AZUL_OSC}, negritas={1: True})
    m.clic(l, g)
g = m.grupo(l)
caja(g.shapes, 6.8, 5.25, 5.95, 0.32, ROJO_CL, None)
texto(g.shapes, 6.95, 5.27, 5.7, 0.28, "¿\"4-2\"? Ninguna regla pone un signo a la mitad ⇒ ✗ no pertenece.", 11, ROJO, True)
m.clic(l, g)
g = m.grupo(l)
caja(g.shapes, 0.55, 5.7, 12.2, 0.85, MARINO, None)
texto(g.shapes, 0.85, 5.75, 11.6, 0.75, "Llegamos a la cadena completa usando sólo las reglas ⇒ \"-42\" **sí pertenece**. "
      "Así se publican hoy las reglas de los lenguajes de programación: la documentación oficial de Python trae su "
      "gramática completa escrita con una notación de este tipo.", 13, BLANCO, ancla="m")
m.clic(l, g)

# =====================================================================================
# S2 · Separador autómatas
m.separador("2 de 5", "Autómatas finitos", "La máquina más simple sólo recuerda en qué estado va. "
            "¿Y si necesita recordar más?", ACENTOS[1])

# =====================================================================================
# AUT1 · Qué significa autómata
l = m.lamina("¿Qué significa «autómata»?", "Una palabra muy antigua para una idea muy moderna.", notas=(
    "Los GIF son ilustraciones animadas hechas para la clase; se insertan directamente en Keynote para que se "
    "muevan. Aclarar «por sí mismo»: alguien sí le da la entrada al autómata (apretar el botón del piso 2), pero "
    "nadie decide lo que hace con esa entrada: subir, detenerse en el piso correcto y abrir las puertas ya está "
    "decidido por sus reglas. Mensaje: en computación no importa de qué está hecha la máquina, sino sus estados "
    "y sus reglas."))
caja(l.shapes, 0.55, 1.55, 3.0, 2.95, MARINO, None)
texto(l.shapes, 0.75, 1.7, 2.6, 0.3, "Del griego", 12, GRIS, True)
texto(l.shapes, 0.75, 2.05, 2.6, 0.6, "autómatos", 28, "FDE68A", True)
texto(l.shapes, 0.75, 2.8, 2.6, 1.6, "«que se mueve **por sí mismo**»: nadie tiene que operarlo paso a paso; sigue "
      "sus propias reglas.", 13.5, BLANCO)
ejemplos_aut = [("Elevador", "Tú aprietas un botón (la entrada); él solo decide subir, bajar, detenerse y abrir las "
                 "puertas, según sus reglas.", "elevador.gif"),
                ("Semáforo", "Pasa de verde a amarillo y a rojo, siempre en el mismo orden, sin que nadie lo esté "
                 "operando.", "semaforo.gif")]
for i, (t, c, gif) in enumerate(ejemplos_aut):
    x = 3.75 + i * 4.55
    caja(l.shapes, x, 1.55, 4.45, 2.95, FONDO, BORDE)
    m.gifs.append((len(m.prs.slides), str((RECURSOS / gif).resolve()), x + 0.52, 1.62, 3.4))
    texto(l.shapes, x + 0.15, 3.38, 4.15, 0.3, t, 12.5, AZUL, True)
    texto(l.shapes, x + 0.15, 3.7, 4.15, 0.75, c, 11, TEXTO)
g = m.grupo(l)
caja(g.shapes, 0.55, 4.7, 7.3, 1.85, AZUL_CL, None)
texto(g.shapes, 0.8, 4.78, 6.9, 0.3, "En computación, un autómata…", 13.5, AZUL_OSC, True)
texto(g.shapes, 0.8, 5.13, 6.9, 1.4, "…es un **modelo** de una máquina: lee una entrada **símbolo por símbolo** y, "
      "siguiendo **reglas fijas**, cambia de **estado**. Alguien le da la entrada (aprieta un botón, mete una "
      "moneda), pero **nadie decide qué hace con ella**: eso ya lo dicen sus reglas. No importa de qué esté hecha: "
      "sólo importan sus estados y sus reglas.", 12, AZUL_OSC)
g2 = m.grupo(l)
caja(g2.shapes, 8.05, 4.7, 4.7, 1.85, VERDE_CL, None)
texto(g2.shapes, 8.3, 4.78, 4.3, 0.3, "¿Qué es un estado?", 13.5, VERDE, True)
texto(g2.shapes, 8.3, 5.13, 4.3, 1.4, "La **situación** en la que está la máquina en un momento dado: lo único que "
      "«recuerda». El semáforo tiene 3 estados (verde, amarillo, rojo); una puerta, 2 (abierta, cerrada).", 12.5,
      "14532D")
m.clic(l, g)
m.clic(l, g2)

# =====================================================================================
# AUT2 · Tipos de autómatas
l = m.lamina("¿Qué tipos de autómatas hay?", "Todos tienen estados y reglas. Lo que los distingue es cuánta memoria "
             "tienen además de sus estados.", notas=(
    "Hoy vemos los tres, en orden. El autómata de pila es la máquina que "
    "cuenta sin límite (personas en un museo) o revisa que los bloques de código estén bien anidados. También existen autómatas no deterministas "
    "(pueden tener varias flechas con el mismo símbolo); en este curso usamos sólo deterministas."))
tipos = [("Autómata finito", "Memoria: **sólo sus estados**.", "Como recordar algo con los dedos de una mano: hay "
          "un número fijo de posiciones.", "Ej.: torniquete, ¿la contraseña tiene un dígito?, formato de CURP.",
          VERDE_CL, VERDE, "HOY"),
         ("Autómata de pila", "Memoria: estados + **una pila**.", "Como una pila de platos: puedes poner o quitar "
          "el de arriba, pero no ver los de abajo.", "Ej.: al cerrar el museo, ¿salieron todos los que entraron? ¿están bien "
          "anidados tus if?", AZUL_CL, AZUL_OSC, "HOY, DESPUÉS DE LOS FINITOS"),
         ("Máquina de Turing", "Memoria: estados + **una cinta sin fin**.", "Como un cuaderno infinito: puede leer, "
          "escribir, borrar y regresar a cualquier hoja.", "Ej.: cualquier algoritmo que corra en tu computadora.",
          MORADO_CL, MORADO, "AL FINAL DE HOY")]
grupos_a2 = []
for i, (t, mem, analog, ej, f, col, etq) in enumerate(tipos):
    g = m.grupo(l)
    grupos_a2.append(g)
    x = 0.55 + i * 4.12
    caja(g.shapes, x, 1.55, 3.96, 3.05, f, None)
    texto(g.shapes, x + 0.2, 1.65, 3.6, 0.25, etq, 9.5, col, True)
    texto(g.shapes, x + 0.2, 1.9, 3.6, 0.35, t, 16, col, True)
    texto(g.shapes, x + 0.2, 2.35, 3.6, 0.35, mem, 12.5, MARINO)
    texto(g.shapes, x + 0.2, 2.8, 3.6, 0.9, analog, 11.5, TEXTO)
    texto(g.shapes, x + 0.2, 3.75, 3.6, 0.8, ej, 11.5, TEXTO)
g = m.grupo(l)
grupos_a2.append(g)
caja(g.shapes, 0.55, 4.8, 12.2, 1.75, MARINO, None)
texto(g.shapes, 0.85, 4.9, 11.6, 0.3, "¿Qué hace a un autómata finito o «infinito»?", 14, "93C5FD", True)
texto(g.shapes, 0.85, 5.25, 11.6, 1.25, "**La memoria.** Si todo lo que hay que recordar cabe en un número fijo de "
      "estados, es **finito**. Si necesita una memoria que crece con la entrada (pila o cinta), su memoria es "
      "**infinita** (sin límite). Ojo: los estados siempre son finitos; lo que puede no tener fin es la memoria extra.",
      13.5, BLANCO)
for g_ in grupos_a2:
    m.clic(l, g_)

# =====================================================================================
# 12b · Qué es un autómata, para qué sirve y cómo se lee
l = m.lamina("¿Qué es un autómata finito y para qué sirve?",
             "Una máquina imaginaria (un modelo en papel, no un aparato) con muy poca memoria.", notas=(
    "Insistir en que es un modelo: se dibuja y se razona con él, como un diagrama de flujo. "
    "El doble círculo es lo que más confunde: NO detiene la lectura. Pasar por él a la mitad de la cadena no "
    "cuenta; sólo importa en qué estado quedas cuando ya no hay símbolos. "
    "Los autómatas que sólo controlan (torniquete, semáforo) a veces no tienen doble círculo."))
caja(l.shapes, 0.55, 1.55, 12.2, 1.05, MARINO, None)
texto(l.shapes, 0.85, 1.62, 11.6, 0.9, "Un **autómata finito** lee una cadena (símbolos en fila: letras, monedas, eventos…) "
      "**símbolo por símbolo**, de izquierda a derecha, y con cada símbolo **cambia de estado** según reglas fijas. No puede regresar, ni escribir, ni "
      "guardar nada más que **el estado en que va**.", 14.5, BLANCO, ancla="m")
g1 = m.grupo(l)
tarjeta(g1.shapes, 0.55, 2.8, 6.0, 1.45, "Finalidad 1 · Reconocer (decir SÍ o NO)",
        "¿Esta cadena cumple la regla? Al terminar responde **acepta** (SÍ cumple) o **rechaza** (NO cumple). "
        "Ej.: ¿es un número entero válido? ¿tiene forma de CURP?", relleno=VERDE_CL, borde=None,
        color_titulo=VERDE, tam=12)
g2 = m.grupo(l)
tarjeta(g2.shapes, 6.75, 2.8, 6.0, 1.45, "Finalidad 2 · Controlar (reaccionar a eventos)",
        "Modelar algo que cambia de situación según lo que pasa: un torniquete, un semáforo, un pedido. "
        "Aquí importa en qué estado está, no responder sí o no.", relleno=AZUL_CL, borde=None, color_titulo=AZUL_OSC, tam=12)
texto(l.shapes, 0.55, 4.4, 12, 0.3, "Cómo se lee el dibujo", 13, AZUL, True)
leyenda = [("Círculo = estado", "Una **situación** en la que puede estar la máquina. Lleva un nombre que "
            "dice qué recuerda: «sin dígito», «bloqueado»."),
           ("Flecha con símbolo = transición", "«Si estoy aquí y leo este símbolo, me paso allá». "
            "Si la flecha regresa al mismo círculo, me quedo donde estoy."),
           ("Flecha sin origen = inicio", "Marca el estado donde empieza, antes de leer el primer símbolo. "
            "Siempre hay exactamente uno."),
           ("Doble círculo = aceptación", "Si **al terminar** de leer estás aquí, acepta: **SÍ** cumple la regla. "
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
        estado(g.shapes, x + 2.35, cy, 0.22, "B", True, VERDE_CL, VERDE, 10)
        flecha(g.shapes, x + 0.79, cy, x + 2.11, cy, MARINO, 2)
        texto(g.shapes, cx - 0.5, cy - 0.3, 1.0, 0.25, "dígito", 11, AZUL, True, "c")
    elif i == 2:
        flecha(g.shapes, x + 0.55, cy, x + 1.18, cy, MARINO, 2)
        estado(g.shapes, cx, cy, 0.25, "A", tam=11)
    else:
        estado(g.shapes, cx, cy, 0.25, "B", True, VERDE_CL, VERDE, 11)
    texto(g.shapes, x + 0.15, 5.42, 2.6, 0.25, t, 11, MARINO, True)
    texto(g.shapes, x + 0.15, 5.7, 2.6, 0.8, c, 10, TEXTO)
for g_ in [g1, g2] + grupos_leyenda:
    m.clic(l, g_)

# =====================================================================================
# FAQ · Preguntas sobre la definición
l = m.lamina("Quizás se pregunten", "Sobre la definición de autómata finito.", notas=(
    "Si preguntan qué pasaría si sí pudiera regresar: si sólo lee (no escribe), reconoce exactamente lo mismo "
    "(Rabin y Scott, 1959; Shepherdson, 1959). Si además puede escribir, es la máquina de Turing del final de la clase."))
faq = [("¿Sólo puede leer cadenas?", "Sí, pero «cadena» en sentido amplio: cualquier sucesión de símbolos de su "
        "alfabeto, uno tras otro. Pueden ser letras y dígitos, monedas ($5, $10), eventos (tarjeta, empujar) o las "
        "lecturas de un sensor. Si lo puedes poner en fila, es una cadena.", AZUL_CL, AZUL_OSC),
       ("¿Los estados son cadenas?", "No. La **cadena** es lo que entra; los **estados** son las situaciones de la "
        "máquina (los círculos). Sus nombres («sin dígito», «bloqueado») son etiquetas para nosotros: podrían "
        "llamarse q0 y q1 y el autómata funcionaría igual.", VERDE_CL, VERDE),
       ("¿Por qué no puede regresar?", "Es **por definición**, y tiene una razón: modela entradas que llegan una sola "
        "vez y no se pueden volver a leer (monedas, teclas, gente pasando el torniquete). Además garantiza que "
        "termina: da tantos pasos como símbolos tiene la cadena.", AMBAR_CL, AMBAR)]
for i, (t, c, f, col) in enumerate(faq):
    g = m.grupo(l)
    tarjeta(g.shapes, 0.55 + i * 4.12, 1.6, 3.96, 4.0, t, c, relleno=f, borde=None, color_titulo=col, tam=14,
            tam_titulo=16)
    m.clic(l, g)

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
      "como una variable que sólo puede tomar dos valores.", 15, BLANCO)
m.clic(l, g)

# =====================================================================================
# FI · Finito vs infinito
l = m.lamina("¿Cómo saber si un autómata finito resuelve el problema?",
             "La diferencia no está en el dibujo, sino en cuánta memoria necesita el problema.", notas=(
    "En teoría, un «autómata infinito» tendría una cantidad infinita de estados: no se puede dibujar ni construir. "
    "El museo es el mismo problema que revisar paréntesis balanceados: «entra» = «(», «sale» = «)». Lo que se hace en la práctica es un control finito más una memoria que crece: una pila (autómata de pila) o "
    "una cinta (máquina de Turing). Ojo: la máquina de Turing tiene un número finito de estados; lo infinito es "
    "su cinta. La prueba de las tres preguntas es intuitiva; la formal (lema del bombeo) no se ve en este curso."))
tarjeta(l.shapes, 0.55, 1.55, 6.0, 1.75, "Autómata finito", "Un número **fijo** de estados, decidido antes de ver "
        "la entrada. Su memoria **no crece**, aunque la cadena tenga un millón de símbolos. Ej.: torniquete, "
        "contraseña con dígito, formato de CURP.", relleno=VERDE_CL, borde=None, color_titulo=VERDE, tam=12.5,
        tam_titulo=15)
g1 = m.grupo(l)
tarjeta(g1.shapes, 6.75, 1.55, 6.0, 1.75, "«Infinito»: memoria sin límite", "Necesitaría **un estado nuevo por "
        "cada cosa más que recordar**: nunca terminarías de dibujarlo. Se resuelve con estados finitos + una "
        "memoria que crece: una **pila** o una **cinta** (máquina de Turing).", relleno=MORADO_CL, borde=None,
        color_titulo=MORADO, tam=12.5, tam_titulo=15)
texto(l.shapes, 0.55, 3.5, 12, 0.3, "Cómo identificarlo: tres preguntas", 13, AZUL, True)
preg_fi = [("1 · ¿Qué tengo que recordar?", "Escríbelo en una frase: «si ya vi un dígito», «cuántas personas "
            "siguen adentro del museo»."),
           ("2 · ¿Tiene un límite fijo?", "«¿ya vi un dígito?» = sí o no → **finito**. «cuántas adentro» = "
            "0, 1, 2, 3… sin tope → **no alcanza**."),
           ("3 · ¿Puedo dibujarlo completo?", "Si al dibujar tienes que escribir «… y así sucesivamente», "
            "no es finito.")]
grupos_fi = []
for i, (t, c) in enumerate(preg_fi):
    g = m.grupo(l)
    tarjeta(g.shapes, 0.55 + i * 4.12, 3.85, 3.96, 1.35, t, c, tam=12, tam_titulo=13)
    grupos_fi.append(g)
g2 = m.grupo(l)
caja(g2.shapes, 0.55, 5.4, 12.2, 1.15, FONDO, BORDE)
texto(g2.shapes, 0.75, 5.5, 3.3, 0.9, "¿Quedó vacío el museo al cerrar?\nUn estado por cada persona adentro:", 11.5, MARINO,
      True)
for k in range(4):
    cx = 4.5 + k * 1.45
    estado(g2.shapes, cx, 5.97, 0.3, str(k), k == 0, VERDE_CL if k == 0 else BLANCO, VERDE if k == 0 else AZUL_OSC, 12)
    flecha(g2.shapes, cx + 0.32, 5.88, cx + 1.13, 5.88, MARINO, 1.5)
    texto(g2.shapes, cx + 0.3, 5.6, 0.85, 0.25, "entra", 10.5, AZUL, True, "c")
texto(g2.shapes, 10.2, 5.75, 0.6, 0.4, "···", 22, GRIS, True)
texto(g2.shapes, 10.75, 5.5, 1.95, 0.95, "nunca termina: no es finito.\nCon cupo de 50, sí: 51 estados.", 11.5, ROJO, True)
for g_ in [g1] + grupos_fi + [g2]:
    m.clic(l, g_)

# =====================================================================================
# 14 · Partes del autómata (contraseña)
l = m.lamina("Las cinco piezas de un autómata finito",
             "Ejemplo real: muchos sitios exigen que tu contraseña tenga al menos un dígito. ¿Cómo lo revisan?",
             notas=("Para simplificar, el alfabeto son letras y dígitos (sin @, #, etc.). La cadena vacía no tiene "
                    "dígito: se rechaza (no cumple la regla). Una vez que viste un dígito, nada te saca de «con dígito»: por eso el bucle "
                    "«letra o dígito». Doble círculo = estado de aceptación: si al terminar estás ahí, se acepta (sí cumple la regla)."))
estado(l.shapes, 2.0, 3.75, 0.75, "sin dígito", False, BLANCO, AZUL_OSC, 14)
estado(l.shapes, 5.6, 3.75, 0.75, "con dígito", True, VERDE_CL, VERDE, 14)
flecha(l.shapes, 0.45, 3.75, 1.25, 3.75, MARINO, 2)
texto(l.shapes, 0.3, 3.35, 1.0, 0.3, "inicio", 11, TENUE, alinear="c")
flecha(l.shapes, 2.75, 3.75, 4.85, 3.75, MARINO, 2)
texto(l.shapes, 3.0, 3.35, 1.6, 0.35, "dígito", 14, AZUL, True, "c")
bucle(l.shapes, 2.0, 3.75, 0.75, "letra", 90, rb=0.42, tam=14, fuente=SANS)
bucle(l.shapes, 5.6, 3.75, 0.75, "letra o dígito", 90, rb=0.42, tam=14, fuente=SANS)
piezas = [("1 · Estados", "sin dígito, con dígito"), ("2 · Alfabeto", "letras y dígitos: lo que puedes teclear"),
          ("3 · Estado inicial", "sin dígito (la flecha que entra)"),
          ("4 · Aceptación", "con dígito (doble círculo): si terminas aquí, sí cumple la regla"),
          ("5 · Transiciones", "con un dígito pasas a «con dígito»; con una letra te quedas")]
for i, (t, c) in enumerate(piezas):
    g = m.grupo(l)
    caja(g.shapes, 7.2, 1.55 + i * 0.75, 5.55, 0.65, FONDO, BORDE)
    caja(g.shapes, 7.2, 1.55 + i * 0.75, 0.08, 0.65, ACENTOS[i], None, 0)
    texto(g.shapes, 7.45, 1.72 + i * 0.75, 2.0, 0.3, t, 13, MARINO, True)
    texto(g.shapes, 9.4, 1.66 + i * 0.75, 3.3, 0.45, c, 11.5, TEXTO, ancla="m")
    m.clic(l, g)
g = m.grupo(l)
caja(g.shapes, 0.55, 5.45, 12.2, 1.05, AZUL_CL, None)
texto(g.shapes, 0.8, 5.6, 11.7, 0.8, "El **lenguaje** del autómata = todas las contraseñas que acepta (sí cumplen): "
      '"gato7", "2026", "a1b"…   Rechaza (no cumplen) "hola", "abc" y "".', 14, AZUL_OSC)
m.clic(l, g)

# =====================================================================================
# 15 · Traza "mi5x"
l = m.lamina("Prueba de escritorio de un autómata: \"mi5x\"",
             "Igual que en la Clase 17: un renglón por paso. Aquí la única «variable» es el estado.", notas=(
    "Hacer notar que el estado sólo cambia una vez (en el 5) y que después la x ya no lo mueve. "
    "En la siguiente lámina el mismo autómata se escribe en Python."))
estado(l.shapes, 1.6, 3.05, 0.6, "sin dígito", False, BLANCO, AZUL_OSC, 12)
estado(l.shapes, 4.6, 3.05, 0.6, "con dígito", True, VERDE_CL, VERDE, 12)
flecha(l.shapes, 0.4, 3.05, 1.0, 3.05, MARINO, 2)
flecha(l.shapes, 2.2, 3.05, 4.0, 3.05, MARINO, 2)
texto(l.shapes, 2.4, 2.7, 1.4, 0.3, "dígito", 13, AZUL, True, "c")
bucle(l.shapes, 1.6, 3.05, 0.6, "letra", 90, rb=0.36, tam=12, fuente=SANS)
bucle(l.shapes, 4.6, 3.05, 0.6, "letra o dígito", 90, rb=0.36, tam=12, fuente=SANS)
texto(l.shapes, 0.55, 3.95, 5.2, 0.3, "Contraseña de entrada", 12, TENUE, True)
cinta(l.shapes, 0.55, 4.3, list("mi5x"), None, 0.6, 20)
cols = [("Paso", 0.8), ("Lee", 0.9), ("Estado antes", 2.2), ("Estado después", 2.4)]
encabezados(l.shapes, 6.3, 1.6, cols, 0.42, tam=12)
traza = [("0", "—", "—", "sin dígito (inicio)"), ("1", "m", "sin dígito", "sin dígito"),
         ("2", "i", "sin dígito", "sin dígito"), ("3", "5", "sin dígito", "con dígito"),
         ("4", "x", "con dígito", "con dígito")]
for i, f in enumerate(traza):
    g = m.grupo(l)
    renglon(g.shapes, 6.3, 2.02 + i * 0.5, list(zip(f, (0.8, 0.9, 2.2, 2.4))), 0.5, tam=13,
            colores={3: AZUL}, negritas={3: True})
    m.clic(l, g)
g = m.grupo(l)
caja(g.shapes, 6.3, 4.75, 6.3, 0.85, VERDE_CL, None)
texto(g.shapes, 6.5, 4.9, 5.9, 0.6, "Terminó en **con dígito** (doble círculo) ⇒ \"mi5x\" **se acepta: sí cumple la regla**.", 14, "14532D")
m.clic(l, g)

# =====================================================================================
# 16 · El autómata en Python
l = m.lamina("El autómata en Python: un for, un if y una variable de estado",
             "Ya sabes escribirlo: recorrer la contraseña carácter por carácter y actualizar el estado.", notas=(
    "caracter in \"0123456789\" pregunta si el carácter es uno de los diez dígitos. "
    "La variable estado guarda en qué estado va el autómata: el programa no guarda cuántos dígitos hay ni cuáles, "
    "sólo si ya vio uno. Nombre según la regla del curso: regresa True/False, así que empieza con es_. "
    "Sin ñ en los identificadores."))
codigo(l.shapes, 0.55, 1.55, 7.0, 3.6, '''def es_contrasena_con_digito(contrasena):
    estado = "sin digito"
    for caracter in contrasena:
        if caracter in "0123456789":
            estado = "con digito"
    resultado = estado == "con digito"
    return resultado''', 14)
tarjeta(l.shapes, 7.8, 1.55, 4.95, 1.1, "Llamadas", "", tam=12)
texto(l.shapes, 8.0, 1.95, 4.6, 0.6, 'es_contrasena_con_digito("mi5x") → True\nes_contrasena_con_digito("hola") → False',
      10.5, AZUL_OSC, fuente=MONO)
g = m.grupo(l)
tarjeta(g.shapes, 7.8, 2.85, 4.95, 2.3, "¿Dónde está cada pieza?", "Estado inicial → línea 2\n"
        "Leer carácter por carácter → línea 3\nTransición con un dígito → líneas 4 y 5\n"
        "Con una letra no hay if: el estado se queda igual (el bucle)\nAceptación → líneas 6 y 7", tam=12.5)
m.clic(l, g)
g = m.grupo(l)
caja(g.shapes, 0.55, 5.4, 12.2, 1.1, MARINO, None)
texto(g.shapes, 0.85, 5.55, 11.6, 0.85, "No importa si la contraseña tiene 4 caracteres o 4 millones: la función "
      "sólo usa **una variable** de memoria. Eso es lo que hace «finito» al autómata: memoria O(1).",
      15, BLANCO)
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
flecha(l.shapes, 1.6, 3.62, 3.6, 4.24, ROJO, 1.5, punteada=True)
flecha(l.shapes, 6.0, 3.55, 4.42, 4.5, ROJO, 1.5, punteada=True)
texto(l.shapes, 4.55, 4.1, 2.6, 0.3, "cualquier otro símbolo", 11, ROJO, alinear="c")
bucle(l.shapes, 3.9, 4.7, 0.55, "", 180, rb=0.3, color=ROJO)
texto(l.shapes, 1.2, 4.5, 1.6, 0.4, "cualquier\nsímbolo", 11, ROJO, True, "r")
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
# REPY · La expresión regular en Python
l = m.lamina("La misma expresión regular, en Python normal",
             "^[+-]?[0-9]+$ es el autómata del número entero. Escrito con for e if, igual que el de la contraseña.",
             notas=("Cada estado del dibujo es un valor de la variable estado. El orden de los if importa: primero el "
                    "signo (sólo se acepta en el estado inicio), luego cualquier dígito (desde cualquier estado que no "
                    "sea error) y todo lo demás manda a error, de donde ya no se sale. Python también tiene un módulo "
                    "para usar expresiones regulares directamente (re), pero aquí lo escribimos a mano para ver el "
                    "autómata."))
codigo(l.shapes, 0.55, 1.55, 7.4, 4.1, '''def es_entero_valido(cadena):
    estado = "inicio"
    for caracter in cadena:
        es_digito = caracter in "0123456789"
        if estado == "inicio" and caracter in "+-":
            estado = "signo"
        elif estado != "error" and es_digito:
            estado = "digitos"
        else:
            estado = "error"
    resultado = estado == "digitos"
    return resultado''', 13)
encabezados(l.shapes, 8.2, 1.55, [("Pieza de la regex", 1.7), ("En el código", 2.85)], 0.36, tam=11)
piezas_py = [("^", "línea 2: empieza en «inicio»"), ("[+-]?", "líneas 5 y 6: el signo, sólo al inicio"),
             ("[0-9]", "líneas 4, 7 y 8: un dígito"), ("+", "línea 7: otro dígito te deja en «digitos»"),
             ("$", "líneas 11 y 12: al terminar, ¿quedó en «digitos»?"), ("(error)", "líneas 9 y 10: cualquier otra cosa")]
for i, (pz, cod) in enumerate(piezas_py):
    g = m.grupo(l)
    renglon(g.shapes, 8.2, 1.91 + i * 0.5, [(pz, 1.7), (cod, 2.85)], 0.5, tam=11, fuente=(0,), alinear={1: "l"},
            colores={0: AZUL_OSC}, negritas={0: True})
    m.clic(l, g)
tarjeta(l.shapes, 8.2, 4.98, 4.55, 0.75, "Llamadas", "", tam=10)
texto(l.shapes, 8.35, 5.38, 4.3, 0.3, 'es_entero_valido("-42") → True · ("4-2") → False', 10, AZUL_OSC, fuente=MONO)
g = m.grupo(l)
caja(g.shapes, 0.55, 5.85, 12.2, 0.7, MARINO, None)
texto(g.shapes, 0.85, 5.9, 11.6, 0.6, "Una expresión regular, su autómata y este código son **la misma regla** escrita "
      "de tres maneras.", 14, BLANCO, ancla="m")
m.clic(l, g)

# =====================================================================================
# S3 · Separador del problema al código
m.separador("3 de 5", "Del problema al código", "Problema, autómata, diagrama de flujo y Python no compiten: "
            "son el mismo algoritmo visto de lejos y de cerca.", ACENTOS[2])

# =====================================================================================
# 16b · Mismo problema: diagrama de flujo vs autómata
l = m.lamina("Mismo problema, dos dibujos: diagrama de flujo y autómata",
             "¿La contraseña tiene al menos un dígito? A la izquierda, como en la Clase 15; a la derecha, como hoy.",
             notas=("El diagrama de flujo es el de la función es_contrasena_con_digito, con los mismos símbolos de la "
                    "Clase 15 y de la plataforma: el hexágono es el ciclo (sirve para for y para while), «siguiente» "
                    "entra al cuerpo y «terminó» sale. Recorrer los dos con \"mi5x\". En el diagrama el dedo pasa por "
                    "acciones (asignar, comparar, regresar); en el autómata sólo salta de un círculo a otro con cada "
                    "símbolo: el ciclo y el «leer el siguiente» están implícitos."))
caja(l.shapes, 0.55, 1.55, 6.0, 5.0, FONDO, BORDE)
texto(l.shapes, 0.75, 1.6, 5.6, 0.3, "Diagrama de flujo (Clase 15): las figuras son acciones", 12, VERDE, True)
cx = 3.45
fl_figura(l.shapes, "terminal", cx, 1.95, 3.6, 0.34, "es_contrasena_con_digito(contrasena)", 9.5)
fl_figura(l.shapes, "proceso", cx, 2.45, 2.6, 0.32, 'estado = "sin digito"', 10)
_, _, c_izq, c_der = fl_figura(l.shapes, "ciclo", cx, 2.95, 3.3, 0.4, "for caracter in contrasena", 10)
_, _, d_izq, d_der = fl_figura(l.shapes, "decision", cx, 3.6, 3.0, 0.58, 'caracter in "0123456789"', 9)
fl_figura(l.shapes, "proceso", cx, 4.4, 2.6, 0.32, 'estado = "con digito"', 10)
fl_figura(l.shapes, "proceso", cx, 5.18, 3.4, 0.32, 'resultado = estado == "con digito"', 9.5)
fl_figura(l.shapes, "salida", cx, 5.68, 2.2, 0.32, "return resultado", 10)
fl_figura(l.shapes, "terminal", cx, 6.15, 1.0, 0.28, "Fin", 10)
for y1, y2 in ((2.29, 2.45), (2.77, 2.95), (3.35, 3.6), (4.18, 4.4), (5.5, 5.68), (6.0, 6.15)):
    fl_linea(l.shapes, [(cx, y1), (cx, y2)])
fl_etiqueta(l.shapes, cx + 0.08, 3.36, "siguiente")
fl_etiqueta(l.shapes, cx + 0.08, 4.19, "Sí")
fl_etiqueta(l.shapes, d_der[0] + 0.05, d_der[1] - 0.25, "No")
fl_linea(l.shapes, [d_der, (5.35, d_der[1]), (5.35, 4.88), (cx, 4.88)])
fl_linea(l.shapes, [(cx, 4.72), (cx, 4.88)], punta=False)
fl_linea(l.shapes, [(cx, 4.88), (0.85, 4.88), (0.85, c_izq[1]), c_izq])
fl_etiqueta(l.shapes, c_der[0] + 0.05, c_der[1] - 0.25, "terminó")
fl_linea(l.shapes, [c_der, (6.25, c_der[1]), (6.25, 5.05), (cx, 5.05), (cx, 5.18)])
g = m.grupo(l)
caja(g.shapes, 6.75, 1.55, 6.0, 5.0, FONDO, BORDE)
texto(g.shapes, 6.95, 1.62, 5.6, 0.3, "Autómata (hoy)", 13, AZUL, True)
estado(g.shapes, 8.4, 3.85, 0.65, "sin dígito", False, BLANCO, AZUL_OSC, 13)
estado(g.shapes, 11.3, 3.85, 0.65, "con dígito", True, VERDE_CL, VERDE, 13)
flecha(g.shapes, 6.95, 3.85, 7.75, 3.85, MARINO, 2)
flecha(g.shapes, 9.05, 3.85, 10.65, 3.85, MARINO, 2)
texto(g.shapes, 9.15, 3.48, 1.4, 0.3, "dígito", 13, AZUL, True, "c")
bucle(g.shapes, 8.4, 3.85, 0.65, "letra", 90, rb=0.38, tam=13, fuente=SANS)
bucle(g.shapes, 11.3, 3.85, 0.65, "letra o dígito", 90, rb=0.38, tam=13, fuente=SANS)
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
       ("Resultado", "cualquier cosa: números, texto, listas…", "SÍ o NO (¿cumple la regla?), o el estado final"),
       ("Se usa para…", "diseñar cualquier programa", "reconocer patrones y controlar sistemas con estados")]
for i, (a_, b_, c_) in enumerate(dif):
    g = m.grupo(l)
    renglon(g.shapes, 0.55, 3.2 + i * 0.55, [(a_, 2.6), (b_, 4.8), (c_, 4.8)], 0.55, tam=12,
            negritas={0: True}, colores={0: AZUL_OSC}, alinear={1: "l", 2: "l"})
    m.clic(l, g)

# =====================================================================================
# CV · Cómo conviven
l = m.lamina("Cómo conviven: problema, autómata, diagrama de flujo y código",
             "Ejemplo: una máquina expendedora vende un dulce de $15 y recibe monedas de $5 y $10.", notas=(
    "Cada etapa responde una pregunta distinta y se revisa contra la anterior. El autómata decide QUÉ recordar "
    "(el total, topado en 15: cuatro estados). El diagrama de flujo, con los símbolos de la Clase 15, dice CÓMO "
    "recorrer las monedas. El código es el diagrama traducido, renglón por renglón. "
    "Simplificación: si mete de más, vende sin dar cambio."))
etapas = [("1 · Problema", "qué quiere la gente", 2.1, AZUL), ("2 · Autómata", "qué hay que recordar", 3.0, VERDE),
          ("3 · Diagrama de flujo", "cómo recorrer las monedas", 3.2, AMBAR), ("4 · Código", "lo que se ejecuta", 3.3, MORADO)]
xs = [0.55]
for _, _, w, _ in etapas[:-1]:
    xs.append(xs[-1] + w + 0.2)
grupos_cv = []
for (t, sub, w, col), x in zip(etapas, xs):
    g = m.grupo(l)
    grupos_cv.append(g)
    caja(g.shapes, x, 1.55, w, 4.53, FONDO, BORDE)
    caja_texto(g.shapes, x, 1.55, w, 0.42, t, 12.5, BLANCO, col, None, True, redondeo=0)
    texto(g.shapes, x + 0.1, 2.02, w - 0.2, 0.25, sub, 10.5, TENUE, alinear="c")
g = grupos_cv[0]
texto(g.shapes, 0.66, 2.4, 1.9, 3.5, "En español:\n\n«¿Las monedas que entraron ya suman $15?»\n\n"
      "Hay que precisarlo: ¿y si mete $20? Decidimos: también vende (sin cambio).", 11.5, TEXTO)
g = grupos_cv[1]
x = xs[1]
izq, der, arr, aba = x + 0.75, x + 2.3, 2.95, 4.3
estado(g.shapes, izq, arr, 0.3, "$0", tam=11)
estado(g.shapes, der, arr, 0.3, "$5", tam=11)
estado(g.shapes, izq, aba, 0.3, "$10", tam=11)
estado(g.shapes, der, aba, 0.32, "$15", True, VERDE_CL, VERDE, 11)
flecha(g.shapes, x + 0.08, arr, izq - 0.3, arr, MARINO, 1.75)
flecha(g.shapes, izq + 0.3, arr, der - 0.3, arr, MARINO, 1.75)
texto(g.shapes, izq + 0.4, arr - 0.3, 0.8, 0.25, "+5", 11, AZUL, True, "c")
flecha(g.shapes, izq, arr + 0.3, izq, aba - 0.3, MARINO, 1.75)
texto(g.shapes, x + 0.05, (arr + aba) / 2 - 0.12, 0.6, 0.25, "+10", 11, AZUL, True, "r")
flecha(g.shapes, der - 0.22, arr + 0.22, izq + 0.22, aba - 0.22, MARINO, 1.75)
texto(g.shapes, (izq + der) / 2 - 0.05, (arr + aba) / 2 - 0.3, 0.6, 0.25, "+5", 11, AZUL, True, "c")
flecha(g.shapes, der, arr + 0.3, der, aba - 0.32, MARINO, 1.75)
texto(g.shapes, der + 0.08, (arr + aba) / 2 - 0.12, 0.6, 0.25, "+10", 11, AZUL, True)
flecha(g.shapes, izq + 0.3, aba, der - 0.32, aba, MARINO, 1.75)
texto(g.shapes, izq + 0.2, aba + 0.03, 1.2, 0.25, "+5 o +10", 10.5, AZUL, True, "c")
bucle(g.shapes, der, aba, 0.32, "", 270, rb=0.22)
texto(g.shapes, der - 0.15, aba + 0.75, 0.85, 0.25, "+5 o +10", 10, AZUL, True)
texto(g.shapes, x + 0.1, 5.25, 2.8, 0.75, "Recordar el total, topado en $15: **4 estados**. $15 es de aceptación: "
      "sí alcanza para el dulce.", 10.5, TEXTO)
g = grupos_cv[2]
x = xs[2]
cx = x + 1.6
fl_figura(g.shapes, "terminal", cx, 2.35, 3.0, 0.28, "es_pago_completo(lista_monedas)", 8.5)
fl_figura(g.shapes, "proceso", cx, 2.75, 1.6, 0.26, "estado = 0", 9)
_, _, c_izq, c_der = fl_figura(g.shapes, "ciclo", cx, 3.15, 2.7, 0.32, "for moneda in lista_monedas", 8.5)
fl_figura(g.shapes, "proceso", cx, 3.63, 2.4, 0.26, "estado = estado + moneda", 8.5)
_, _, d_izq, d_der = fl_figura(g.shapes, "decision", cx, 4.02, 1.9, 0.42, "estado > 15", 8.5)
fl_figura(g.shapes, "proceso", cx, 4.6, 1.6, 0.25, "estado = 15", 9)
fl_figura(g.shapes, "proceso", cx, 5.15, 2.6, 0.25, "resultado = estado == 15", 8.5)
fl_figura(g.shapes, "salida", cx, 5.5, 2.0, 0.24, "return resultado", 8.5)
fl_figura(g.shapes, "terminal", cx, 5.82, 0.8, 0.22, "Fin", 8.5)
for y1, y2 in ((2.63, 2.75), (3.01, 3.15), (3.47, 3.63), (3.89, 4.02), (4.44, 4.6), (5.4, 5.5), (5.74, 5.82)):
    fl_linea(g.shapes, [(cx, y1), (cx, y2)])
fl_etiqueta(g.shapes, cx + 0.05, 3.46, "siguiente", 7.5)
fl_etiqueta(g.shapes, cx + 0.05, 4.43, "Sí", 7.5)
fl_etiqueta(g.shapes, d_der[0] + 0.02, d_der[1] - 0.2, "No", 7.5)
fl_linea(g.shapes, [d_der, (cx + 1.2, d_der[1]), (cx + 1.2, 4.97), (cx, 4.97)])
fl_linea(g.shapes, [(cx, 4.85), (cx, 4.97)], punta=False)
fl_linea(g.shapes, [(cx, 4.97), (x + 0.1, 4.97), (x + 0.1, c_izq[1]), c_izq])
fl_etiqueta(g.shapes, c_der[0] + 0.01, c_der[1] - 0.2, "terminó", 7.5)
fl_linea(g.shapes, [c_der, (x + 3.12, c_der[1]), (x + 3.12, 5.07), (cx, 5.07), (cx, 5.15)])
g = grupos_cv[3]
x = xs[3]
codigo(g.shapes, x + 0.08, 2.38, 3.14, 3.0, '''def es_pago_completo(lista_monedas):
    estado = 0
    for moneda in lista_monedas:
        estado = estado + moneda
        if estado > 15:
            estado = 15
    resultado = estado == 15
    return resultado''', 8.5, etiqueta=None)
g5 = m.grupo(l)
caja(g5.shapes, 0.55, 6.15, 12.2, 0.5, MARINO, None)
texto(g5.shapes, 0.85, 6.17, 11.6, 0.46, "En ese orden: el **autómata** dice **qué** recordar; el **diagrama**, **cómo** "
      "recorrer las monedas; el **código** es el diagrama traducido.", 12.5, BLANCO, ancla="m")
for g_ in grupos_cv + [g5]:
    m.clic(l, g_)

# =====================================================================================
# RC · Receta
l = m.lamina("Receta: de una situación real a un autómata",
             "Siete preguntas. Ejemplo: una lámpara con un solo botón (apagada → tenue → fuerte → apagada).", notas=(
    "La pregunta 5 es donde más se equivocan: hay que llenar la tabla completa, una casilla por cada estado y "
    "cada símbolo. Si una combinación «no debería pasar», igual hay que decidir qué hace (ignorarla o ir a error). "
    "La 7 conecta con la lámina de finito vs infinito."))
cols_rc = [("Paso", 1.4), ("Pregunta", 3.9), ("Para la lámpara", 3.0)]
encabezados(l.shapes, 0.55, 1.6, cols_rc, 0.38, tam=11.5)
receta = [("1 · Estados", "¿Qué tengo que recordar? Cada posibilidad es un estado.", "apagada, tenue, fuerte"),
          ("2 · Alfabeto", "¿Qué puede pasar? (símbolos o eventos)", "{botón}"),
          ("3 · Inicio", "¿En qué situación empieza?", "apagada"),
          ("4 · Aceptación", "¿Cuándo respondo SÍ? Si sólo controla, ninguno.", "ninguno: sólo controla"),
          ("5 · Transiciones", "Para **cada** estado y **cada** símbolo, ¿a dónde voy? Llena la tabla completa.",
           "apagada → tenue → fuerte → apagada"),
          ("6 · Prueba", "Prueba de escritorio con 2 o 3 casos, incluidos los raros.", "3 clics: regresa a apagada ✓"),
          ("7 · ¿Finito?", "¿Lo que recuerdo tiene un límite fijo?", "sí: 3 estados")]
for i in range(len(receta)):
    renglon(l.shapes, 0.55, 1.98 + i * 0.58, [("", 1.4), ("", 3.9), ("", 3.0)], 0.58)
for i, (pz, q, ej) in enumerate(receta):
    y = 1.98 + i * 0.58
    g = m.grupo(l)
    caja_texto(g.shapes, 0.55, y, 1.4, 0.58, pz, 11, AZUL_OSC, BLANCO, BORDE, True, alinear="l", redondeo=0)
    caja_texto(g.shapes, 1.95, y, 3.9, 0.58, q, 10.5, TEXTO, BLANCO, BORDE, alinear="l", redondeo=0)
    m.clic(l, g)
    g = m.grupo(l)
    caja_texto(g.shapes, 5.85, y, 3.0, 0.58, ej, 11, VERDE, VERDE_CL, BORDE, True, redondeo=0)
    m.clic(l, g)
g = m.grupo(l)
caja(g.shapes, 9.1, 1.6, 3.65, 4.4, FONDO, BORDE)
texto(g.shapes, 9.25, 1.7, 3.4, 0.3, "El autómata de la lámpara", 12, AZUL, True)
estado(g.shapes, 10.0, 3.0, 0.5, "apagada", relleno=BLANCO, tam=10.5)
estado(g.shapes, 11.9, 3.0, 0.5, "tenue", relleno=AMBAR_CL, borde=AMBAR, tam=10.5)
estado(g.shapes, 10.95, 4.85, 0.5, "fuerte", relleno="FDE68A", borde=AMBAR, tam=10.5)
flecha(g.shapes, 9.2, 3.0, 9.5, 3.0, MARINO, 2)
flecha(g.shapes, 10.5, 3.0, 11.4, 3.0, MARINO, 2)
texto(g.shapes, 10.55, 2.68, 0.8, 0.25, "botón", 10, AZUL, True, "c")
flecha(g.shapes, 11.68, 3.45, 11.2, 4.4, MARINO, 2)
texto(g.shapes, 11.55, 3.85, 0.8, 0.25, "botón", 10, AZUL, True, "c")
flecha(g.shapes, 10.7, 4.4, 10.22, 3.45, MARINO, 2)
texto(g.shapes, 9.55, 3.85, 0.8, 0.25, "botón", 10, AZUL, True, "c")
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
# SP · Separador autómata de pila
m.separador("4 de 5", "Autómata de pila", "Cuando contar no tiene tope: un autómata finito con una memoria extra.",
            ACENTOS[3])

# =====================================================================================
# 18 · Límite del autómata finito + jerarquía
l = m.lamina("Lo que un autómata finito NO puede hacer",
             "¿Quedó vacío el museo al cerrar? Hay que contar cuántos siguen adentro, y eso no tiene límite.",
             notas=(
    "Con k estados sólo puedes contar hasta k − 1 personas. Siempre puede llegar una más. "
    "Es el mismo problema que revisar paréntesis balanceados; por eso Python usa una pila (autómata de pila) "
    "para revisar paréntesis y bloques. "
    "Chomsky, 1956: jerarquía de lenguajes."))
tarjeta(l.shapes, 0.55, 1.6, 4.6, 2.2, "Con 3 estados cuento hasta 2 personas",
        "estados «0 adentro», «1 adentro», «2 adentro».\nSi entra una tercera, ya no me alcanzan los estados. "
        "Y siempre puede llegar una persona más.", tam=12.5)
g = m.grupo(l)
tarjeta(g.shapes, 0.55, 4.0, 4.6, 2.5, "La salida: darle memoria", "Un **autómata de pila** apila una ficha "
        "por cada persona que entra y quita una por cada una que sale. Una **máquina de Turing** tiene una cinta infinita: "
        "puede escribir, borrar y regresar.", relleno=AZUL_CL, borde=None, color_titulo=AZUL_OSC, tam=12.5)
m.clic(l, g)
niveles = [("Máquina de Turing", "cinta infinita · lee, escribe y regresa", "cualquier algoritmo", "EDE9FE", MORADO),
           ("Autómata de pila", "estados + una pila", "contar personas, la gramática de Python", "DBEAFE", AZUL_OSC),
           ("Autómata finito", "sólo estados", "CURP, contraseñas, torniquete", "DCFCE7", VERDE)]
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
# P1 · Qué es una pila
l = m.lamina("Autómata de pila: un autómata finito + una pila",
             "La pila es memoria extra sin límite, pero con una regla: sólo se puede tocar el elemento de arriba.",
             notas=("Antes del autómata, la estructura. Pedir ejemplos de pilas en su vida: platos, cartas, "
                    "historial del navegador, Ctrl+Z."))
tarjeta(l.shapes, 0.55, 1.6, 6.0, 4.95, "¿Qué es una pila?", "Como una pila de platos, sólo puedes hacer tres cosas:\n\n"
        "• **apilar**: poner uno arriba\n• **desapilar**: quitar el de arriba\n• **ver** cuál está arriba\n\n"
        "No puedes sacar uno de en medio. El último que entra es el primero que sale.", tam=14, tam_titulo=17)
g = m.grupo(l)
caja(g.shapes, 6.75, 1.6, 6.0, 4.95, FONDO, BORDE)
texto(g.shapes, 6.95, 1.72, 5.6, 0.3, "Ya las usas todos los días", 15, AZUL, True)
for k, col in enumerate(("DBEAFE", "DCFCE7", "FEF3C7", "EDE9FE")):
    caja_texto(g.shapes, 7.3, 4.9 - k * 0.5, 2.2, 0.44, f"plato {k + 1}", 12, MARINO, col, GRIS, redondeo=0.08)
flecha(g.shapes, 9.9, 2.75, 9.9, 3.25, VERDE, 2.5)
texto(g.shapes, 9.55, 2.45, 1.0, 0.25, "apilar", 12, VERDE, True, "c")
flecha(g.shapes, 10.6, 3.25, 10.6, 2.75, ROJO, 2.5)
texto(g.shapes, 10.2, 3.3, 1.2, 0.25, "desapilar", 12, ROJO, True, "c")
texto(g.shapes, 9.8, 3.9, 2.8, 2.5, "**Ctrl+Z** deshace la última acción.\n\nEl botón **«atrás»** del navegador "
      "regresa a la última página.", 13, TEXTO)
m.clic(l, g)

# =====================================================================================
# P1b · El autómata de pila del museo
l = m.lamina("El autómata de pila del museo", "Alfabeto: {entra, sale, cierra}. Las flechas dicen «lo que leo / lo "
             "que hago con la pila».", notas=(
    "Responder las dos preguntas típicas. ¿Hay estado cerrado? Sí: al leer «cierra» se pasa a «museo vacío» (doble "
    "círculo, acepta) si la pila no tiene fichas, o a «quedó gente» si todavía tiene. ¿Se ve en el dibujo cuántas "
    "personas hay? No, y a propósito: si hubiera un círculo por cada número de personas, regresaríamos a la cadena "
    "infinita. El dibujo tiene las reglas (fijas); la pila tiene la cuenta (cambia). Para saber cuántos hay en un "
    "momento se mira la «foto»: estado + contenido de la pila. Por eso la prueba de escritorio dibuja la pila."))
caja(l.shapes, 0.55, 1.55, 7.75, 5.0, FONDO, BORDE)
estado(l.shapes, 2.6, 3.9, 0.6, "abierto", relleno=BLANCO, tam=13)
flecha(l.shapes, 0.75, 3.9, 2.0, 3.9, MARINO, 2)
bucle(l.shapes, 2.6, 3.9, 0.6, "entra / apila ●", 90, rb=0.36, tam=12, fuente=SANS, color_etiqueta=VERDE)
bucle(l.shapes, 2.6, 3.9, 0.6, "", 270, rb=0.36)
texto(l.shapes, 1.4, 5.35, 2.4, 0.3, "sale / desapila ●", 12, AZUL, True, "c")
estado(l.shapes, 6.6, 2.35, 0.55, "error", relleno=ROJO_CL, borde=ROJO, tam=12)
flecha(l.shapes, 3.1, 3.55, 6.08, 2.5, ROJO, 2)
texto(l.shapes, 3.6, 2.45, 2.4, 0.3, "sale, pila vacía", 11.5, ROJO, True, "c")
bucle(l.shapes, 6.6, 2.35, 0.55, "", 0, rb=0.28, color=ROJO)
texto(l.shapes, 6.95, 2.9, 1.3, 0.3, "cualquiera", 10.5, ROJO, True)
estado(l.shapes, 6.6, 3.95, 0.6, "museo\nvacío", True, VERDE_CL, VERDE, 12)
flecha(l.shapes, 3.2, 3.92, 6.0, 3.95, VERDE, 2)
texto(l.shapes, 3.5, 3.6, 2.3, 0.3, "cierra, pila vacía", 11.5, VERDE, True, "c")
estado(l.shapes, 6.6, 5.55, 0.55, "quedó\ngente", relleno=AMBAR_CL, borde=AMBAR, tam=11.5)
flecha(l.shapes, 3.1, 4.25, 6.1, 5.35, AMBAR, 2)
texto(l.shapes, 4.15, 4.95, 2.6, 0.3, "cierra, pila con fichas", 11.5, AMBAR, True, "c")
g = m.grupo(l)
caja(g.shapes, 8.5, 1.55, 4.25, 2.65, AZUL_CL, None)
texto(g.shapes, 8.7, 1.62, 3.9, 0.3, "¿Dónde está la cuenta?", 13.5, AZUL_OSC, True)
caja_texto(g.shapes, 8.75, 2.15, 1.35, 0.42, "abierto", 12, MARINO, BLANCO, AZUL_OSC, True, redondeo=0.2)
texto(g.shapes, 10.2, 2.2, 0.3, 0.3, "+", 14, AZUL_OSC, True, "c")
caja(g.shapes, 10.6, 2.0, 0.06, 1.0, GRIS, None, 0)
for k in range(3):
    s = g.shapes.add_shape(MSO_SHAPE.OVAL, Inches(10.75 + k * 0.4), Inches(2.25), Inches(0.32), Inches(0.32))
    s.fill.solid(); s.fill.fore_color.rgb = rgb(AMBAR if k == 2 else "FDE68A"); s.line.fill.background()
    s.shadow.inherit = False
texto(g.shapes, 8.7, 3.1, 3.9, 1.05, "Una «foto» del autómata = su **estado** + lo que tiene la **pila**. Aquí: "
      "abierto con 3 fichas = **3 personas adentro**.", 11.5, AZUL_OSC)
m.clic(l, g)
g = m.grupo(l)
caja(g.shapes, 8.5, 4.35, 4.25, 2.2, MARINO, None)
texto(g.shapes, 8.7, 4.45, 3.9, 2.0, "¿Un círculo por cada número de personas? **No**: eso sería infinito. Los "
      "círculos dicen **en qué etapa** va; la **pila** guarda **cuántos** hay. Por eso la cuenta se ve en la prueba "
      "de escritorio, no en el dibujo.", 12, BLANCO)
m.clic(l, g)

# =====================================================================================
# P2 · Traza del autómata de pila
l = m.lamina("Prueba de escritorio con pila: ¿quedó vacío el museo?",
             "Entrada: entra, entra, sale, entra, sale, sale, cierra. Cada renglón es una «foto»: estado + pila.", notas=(
    "Tu turno, caso 1: «entra, sale, sale»: en el paso 3 «sale» llega con la pila vacía: pasa a error y ahí se "
    "queda (salió alguien que no entró). Caso 2: «entra, cierra»: la pila tiene una ficha al cerrar: «quedó gente»."))
cols_p = [("Paso", 0.7), ("Lee", 1.1), ("Qué hace", 2.3), ("Pila (arriba = derecha)", 3.5), ("Personas", 1.4),
          ("Estado", 3.2)]
encabezados(l.shapes, 0.55, 1.6, cols_p, 0.4, tam=11.5)
pasos_p = [("0", "—", "empieza vacía", 0, "abierto"), ("1", "entra", "apila ●", 1, "abierto"),
           ("2", "entra", "apila ●", 2, "abierto"), ("3", "sale", "desapila ●", 1, "abierto"),
           ("4", "entra", "apila ●", 2, "abierto"), ("5", "sale", "desapila ●", 1, "abierto"),
           ("6", "sale", "desapila ●", 0, "abierto"), ("7", "cierra", "pila vacía", 0, "museo vacío ✓")]
for i, (p_, lee, hace, n, est) in enumerate(pasos_p):
    g = m.grupo(l)
    y = 2.0 + i * 0.45
    renglon(g.shapes, 0.55, y, [(p_, 0.7), (lee, 1.1), (hace, 2.3), ("", 3.5), (str(n), 1.4), (est, 3.2)], 0.45,
            tam=12, negritas={4: True, 5: True}, colores={4: AZUL, 5: VERDE if i == 7 else AZUL_OSC})
    x0 = 0.55 + 0.7 + 1.1 + 2.3 + 0.2
    caja(g.shapes, x0, y + 0.08, 0.06, 0.29, GRIS, None, 0)
    for k in range(n):
        s = g.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x0 + 0.15 + k * 0.36), Inches(y + 0.08), Inches(0.29), Inches(0.29))
        s.fill.solid(); s.fill.fore_color.rgb = rgb(AMBAR if k == n - 1 else "FDE68A")
        s.line.fill.background(); s.shadow.inherit = False
    if n == 0:
        texto(g.shapes, x0 + 0.15, y + 0.1, 1.5, 0.25, "(vacía)", 11, GRIS)
    m.clic(l, g)
g = m.grupo(l)
caja(g.shapes, 0.55, 5.75, 6.0, 0.8, VERDE_CL, None)
texto(g.shapes, 0.75, 5.8, 5.6, 0.7, "Al cerrar la pila está **vacía** ⇒ «museo vacío»: acepta, **SÍ** quedó vacío.",
      13, "14532D", ancla="m")
m.clic(l, g)
g = m.grupo(l)
caja(g.shapes, 6.75, 5.75, 6.0, 0.8, AMBAR_CL, None)
texto(g.shapes, 6.95, 5.8, 5.6, 0.7, "Tu turno: «entra, sale, sale» y «entra, cierra». ¿En qué estado termina cada una?",
      12.5, "78350F", True, ancla="m")
m.clic(l, g)

# =====================================================================================
# S4 · Separador Turing
m.separador("5 de 5", "La máquina de Turing", "Un autómata con una cinta infinita: puede leer, escribir y "
            "regresar. Con eso calcula todo lo que tu laptop calcula.", ACENTOS[3])

# =====================================================================================
# 20 · Turing 1936
l = m.lamina("1936 · Alan Turing: ¿qué hace una persona cuando calcula?",
             "En 1936 quiso definir con precisión qué es «calcular». Su idea: imitar a una persona haciendo cuentas.", notas=(
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
# 35 · Práctica (índice)
l = m.lamina("Práctica", "En tu cuaderno o en equipos. Primero resuelve; después revisamos con un clic.")
ej = [("1", "¿Cumple o no cumple?", "Con el autómata de la contraseña con dígito."),
      ("2", "Diseña un autómata", "¿La puerta quedó cerrada al final del día?"),
      ("3", "Del mundo real al autómata", "Pedido de comida, cajero y semáforo."),
      ("4", "¿Finito o de pila?", "Seis preguntas y la pila de la biblioteca."),
      ("5", "Máquinas de Turing", "Sumar 1 a 0111 e invertir los bits de 1011.")]
for i, (n, t, c) in enumerate(ej):
    y = 1.6 + i * 0.97
    caja(l.shapes, 0.55, y, 12.2, 0.82, FONDO, BORDE)
    texto(l.shapes, 0.8, y + 0.17, 0.6, 0.5, n, 24, ACENTOS[i] if ACENTOS[i] != "FBBF24" else AMBAR, True)
    texto(l.shapes, 1.5, y + 0.25, 4.5, 0.4, t, 16, MARINO, True)
    texto(l.shapes, 6.0, y + 0.27, 6.6, 0.4, c, 14, TEXTO)

# =====================================================================================
# 36 · Ejercicios 1 y 2
l = m.lamina("Ejercicios 1 y 2 · Autómatas", "1: sigue el autómata de la contraseña. "
             "2: diseña uno nuevo para la puerta de tu casa.", notas=(
    "Ej. 2: dos estados. Sólo importa el último evento: si fue «cerrar», quedó cerrada. Empieza en «cerrada» y es de "
    "aceptación, porque si no pasó nada la puerta sigue cerrada. Cerrar una puerta ya cerrada no cambia nada: bucle."))
encabezados(l.shapes, 0.55, 1.6, [("Contraseña", 1.6), ("¿Dígito?", 1.0), ("Termina en", 1.6), ("Resultado", 1.5)], 0.4)
e1 = [('"hola"', "no", "sin dígito", "✗ no cumple", ROJO), ('"gato7"', "sí", "con dígito", "✓ sí cumple", VERDE),
      ('""', "no", "sin dígito", "✗ no cumple", ROJO), ('"2026"', "sí", "con dígito", "✓ sí cumple", VERDE),
      ('"7up"', "sí", "con dígito", "✓ sí cumple", VERDE)]
for i, (c, u, t, r, col) in enumerate(e1):
    renglon(l.shapes, 0.55, 2.0 + i * 0.46, [(c, 1.6), ("", 1.0), ("", 1.6), ("", 1.5)], 0.46, tam=13, fuente=(0,))
    g = m.grupo(l)
    texto(g.shapes, 2.15, 2.12 + i * 0.46, 1.0, 0.3, u, 13, TEXTO, alinear="c")
    texto(g.shapes, 3.15, 2.12 + i * 0.46, 1.6, 0.3, t, 12.5, TEXTO, alinear="c")
    texto(g.shapes, 4.75, 2.12 + i * 0.46, 1.5, 0.3, r, 13, col, True, "c")
    m.clic(l, g)
tarjeta(l.shapes, 6.75, 1.6, 6.0, 1.55, "Ejercicio 2 · La puerta", "Empieza **cerrada**. Durante el día pasan "
        "eventos «abrir» y «cerrar». Al final del día, ¿quedó cerrada?\nabrir, cerrar → sí · abrir → no · "
        "(nada) → sí", tam=12)
g = m.grupo(l)
caja(g.shapes, 6.75, 3.3, 6.0, 3.2, FONDO, BORDE)
estado(g.shapes, 8.2, 4.7, 0.6, "cerrada", True, VERDE_CL, VERDE, 12)
estado(g.shapes, 11.3, 4.7, 0.6, "abierta", False, BLANCO, AZUL_OSC, 12)
flecha(g.shapes, 6.95, 4.7, 7.6, 4.7, MARINO, 2)
flecha(g.shapes, 8.8, 4.45, 10.7, 4.45, MARINO, 2)
texto(g.shapes, 9.25, 4.1, 1.0, 0.3, "abrir", 12, AZUL, True, "c")
flecha(g.shapes, 10.7, 4.95, 8.8, 4.95, MARINO, 2)
texto(g.shapes, 9.25, 5.0, 1.0, 0.3, "cerrar", 12, AZUL, True, "c")
bucle(g.shapes, 8.2, 4.7, 0.6, "cerrar", 90, rb=0.3, tam=12, fuente=SANS)
bucle(g.shapes, 11.3, 4.7, 0.6, "abrir", 90, rb=0.3, tam=12, fuente=SANS)
texto(g.shapes, 6.95, 5.6, 5.6, 0.8, "Sólo importa **el último evento**. Cerrar una puerta ya cerrada no cambia nada: "
      "por eso el bucle.", 11.5, TEXTO)
m.clic(l, g)

# =====================================================================================
# EJR · Ejercicios del mundo real (enunciados)
l = m.lamina("Ejercicios · Del mundo real al autómata", "En equipos. Para cada situación usa la receta: estados, "
             "alfabeto, inicio, aceptación, tabla de transiciones, una prueba de escritorio y ¿es finito?", notas=(
    "Dar 5 minutos por situación. Pedir que primero escriban en una frase qué hay que recordar. "
    "Las soluciones están en las láminas siguientes; hay más de una respuesta correcta (por ejemplo, nombres "
    "distintos para los estados o decidir que un evento sin flecha va a un estado de error)."))
ejr = [("A · Pedido de comida", "Un pedido se crea, se paga, el restaurante lo acepta, el repartidor lo recoge y se "
        "entrega. Se puede cancelar **antes** de que salga a entregarse, no después.\n\n"
        "Pregunta: ¿el pedido llegó?", AZUL_CL, AZUL_OSC),
       ("B · Cajero automático", "Tienes 3 intentos para escribir tu NIP. Si aciertas, entras. Si fallas 3 veces, "
        "la tarjeta se bloquea y ya no importa lo que escribas.\n\nPregunta: ¿logró entrar?", VERDE_CL, VERDE),
       ("C · Semáforo con botón", "Para autos está en verde. Si un peatón aprieta el botón, pasa a amarillo; al "
        "terminar el tiempo, a rojo para autos y verde para peatones; al terminar otra vez, regresa a verde.\n\n"
        "Sin pregunta: sólo controla.", AMBAR_CL, AMBAR)]
for i, (t, c, f, col) in enumerate(ejr):
    tarjeta(l.shapes, 0.55 + i * 4.12, 1.75, 3.96, 3.6, t, c, relleno=f, borde=None, color_titulo=col, tam=12.5,
            tam_titulo=15)
caja(l.shapes, 0.55, 5.6, 12.2, 0.9, MARINO, None)
texto(l.shapes, 0.85, 5.67, 11.6, 0.8, "Reto extra: inventa tu propia situación (la puerta de tu edificio, un "
      "videojuego, el registro de materias) y plantéala igual. La mejor la resolvemos en el pizarrón.", 13.5,
      BLANCO, ancla="m")

# =====================================================================================
# SA · Solución A pedido
l = m.lamina("Solución A · Pedido de comida", "Una respuesta posible: los nombres de los estados pueden variar.",
             notas=("Preguntar: ¿qué pasa si llega el evento «entrega» estando en «creado»? No hay flecha: hay que "
                    "decidir si se ignora o si va a un estado de error. Eso también es una regla del negocio."))
nombres_a = [("creado", 1.3), ("pagado", 3.55), ("preparando", 5.8), ("en camino", 8.05), ("entregado", 10.3)]
eventos_a = ["pagar", "acepta", "recoge", "entrega"]
for i, (n, x) in enumerate(nombres_a):
    estado(l.shapes, x, 2.75, 0.6, n, i == 4, VERDE_CL if i == 4 else BLANCO, VERDE if i == 4 else AZUL_OSC, 11)
flecha(l.shapes, 0.3, 2.75, 0.7, 2.75, MARINO, 2)
for i, ev in enumerate(eventos_a):
    x1 = nombres_a[i][1] + 0.6
    x2 = nombres_a[i + 1][1] - 0.6
    flecha(l.shapes, x1, 2.75, x2, 2.75, MARINO, 2)
    texto(l.shapes, x1, 2.4, x2 - x1, 0.3, ev, 11, AZUL, True, "c")
g = m.grupo(l)
estado(g.shapes, 3.55, 4.9, 0.6, "cancelado", relleno=ROJO_CL, borde=ROJO, tam=11)
for i in range(3):
    xx = nombres_a[i][1]
    flecha(g.shapes, xx + (0.15 if i == 0 else 0 if i == 1 else -0.2), 3.35, 3.55 + (i - 1) * 0.35, 4.32, ROJO,
           1.5, punteada=True)
texto(g.shapes, 1.55, 4.0, 1.4, 0.3, "cancelar", 11, ROJO, True, "c")
m.clic(l, g)
g = m.grupo(l)
tarjeta(g.shapes, 5.6, 4.0, 7.15, 2.5, "Lo que dice el dibujo", "• Desde «en camino» **no hay flecha** de cancelar: "
        "la regla del negocio quedó en el modelo.\n• Doble círculo en «entregado»: responde «¿el pedido llegó?».\n"
        "• ¿«entrega» estando en «creado»? No hay flecha: hay que **decidir** si se ignora o va a un estado de error.\n"
        "• Finito: 6 estados, sin importar cuántos pedidos haya.", tam=12)
m.clic(l, g)

# =====================================================================================
# SB · Solución B cajero
l = m.lamina("Solución B · Cajero: NIP con 3 intentos", "Cada intento es un estado: el autómata «cuenta» hasta 3 "
             "con estados, porque el límite es fijo.", notas=(
    "Conexión con finito vs infinito: contar hasta un número fijo (3) se puede con estados. Contar sin límite, no. "
    "La tarjeta bloqueada se queda bloqueada con cualquier entrada: bucle a sí misma."))
estado(l.shapes, 1.45, 2.7, 0.55, "intento 1")
estado(l.shapes, 3.75, 2.7, 0.55, "intento 2")
estado(l.shapes, 6.05, 2.7, 0.55, "intento 3")
estado(l.shapes, 6.05, 5.0, 0.6, "bloqueada", relleno=ROJO_CL, borde=ROJO, tam=11)
estado(l.shapes, 1.45, 5.0, 0.6, "dentro", True, VERDE_CL, VERDE, 12)
flecha(l.shapes, 0.35, 2.7, 0.9, 2.7, MARINO, 2)
flecha(l.shapes, 2.0, 2.7, 3.2, 2.7, ROJO, 2)
texto(l.shapes, 2.0, 2.35, 1.2, 0.3, "NIP mal", 11, ROJO, True, "c")
flecha(l.shapes, 4.3, 2.7, 5.5, 2.7, ROJO, 2)
texto(l.shapes, 4.3, 2.35, 1.2, 0.3, "NIP mal", 11, ROJO, True, "c")
flecha(l.shapes, 6.05, 3.25, 6.05, 4.4, ROJO, 2)
texto(l.shapes, 6.15, 3.65, 1.0, 0.3, "NIP mal", 11, ROJO, True)
flecha(l.shapes, 1.45, 3.25, 1.45, 4.4, VERDE, 2)
flecha(l.shapes, 3.4, 3.12, 1.9, 4.55, VERDE, 2)
flecha(l.shapes, 5.6, 3.05, 2.0, 4.75, VERDE, 2)
texto(l.shapes, 1.55, 3.65, 1.1, 0.3, "NIP bien", 11, VERDE, True)
bucle(l.shapes, 6.05, 5.0, 0.6, "", 0, rb=0.32, color=ROJO)
texto(l.shapes, 7.05, 4.55, 1.1, 0.3, "cualquiera", 10.5, ROJO, True)
g = m.grupo(l)
encabezados(g.shapes, 8.2, 1.6, [("estado", 1.6), ("NIP bien", 1.4), ("NIP mal", 1.55)], 0.38, tam=11)
filas_b = [("intento 1", "dentro", "intento 2"), ("intento 2", "dentro", "intento 3"), ("intento 3", "dentro", "bloqueada"),
           ("dentro", "dentro", "dentro"), ("bloqueada", "bloqueada", "bloqueada")]
for i, f in enumerate(filas_b):
    renglon(g.shapes, 8.2, 1.98 + i * 0.4, list(zip(f, (1.6, 1.4, 1.55))), 0.4, tam=11, negritas={0: True})
m.clic(l, g)
g = m.grupo(l)
tarjeta(g.shapes, 8.2, 4.2, 4.55, 2.3, "Prueba y finitud", "mal, mal, bien → intento 1 → 2 → 3 → **dentro** ✓\n"
        "mal, mal, mal, bien → … → **bloqueada** ✗\n\nFinito: contar hasta **3** cabe en estados porque el "
        "límite es fijo.", tam=11.5)
m.clic(l, g)

# =====================================================================================
# SC · Solución C semáforo + finito o no
l = m.lamina("Solución C · Semáforo con botón", "Dos eventos: el botón y «se acabó el tiempo». Cada estado debe "
             "decir qué hace con los dos.", notas=(
    "Lo interesante son los bucles: apretar el botón cuando ya está en amarillo o en verde peatonal no cambia nada. "
    "Y en verde para autos, si se acaba el tiempo sin botón, se queda en verde. Es un autómata de control: no hay "
    "doble círculo."))
estado(l.shapes, 2.0, 3.3, 0.75, "autos:\nverde", relleno=VERDE_CL, borde=VERDE, tam=12)
estado(l.shapes, 6.0, 3.3, 0.75, "autos:\namarillo", relleno=AMBAR_CL, borde=AMBAR, tam=12)
estado(l.shapes, 4.0, 5.55, 0.7, "peatones:\nverde", relleno=AZUL_CL, borde=AZUL_OSC, tam=11)
flecha(l.shapes, 0.55, 3.3, 1.25, 3.3, MARINO, 2)
flecha(l.shapes, 2.75, 3.3, 5.25, 3.3, MARINO, 2)
texto(l.shapes, 3.3, 2.95, 1.4, 0.3, "botón", 11.5, AZUL, True, "c")
flecha(l.shapes, 5.55, 3.92, 4.5, 5.05, MARINO, 2)
texto(l.shapes, 5.15, 4.45, 1.3, 0.3, "tiempo", 11.5, AZUL, True)
flecha(l.shapes, 3.45, 5.05, 2.45, 3.92, MARINO, 2)
texto(l.shapes, 1.35, 4.45, 1.3, 0.3, "tiempo", 11.5, AZUL, True, "r")
g = m.grupo(l)
bucle(g.shapes, 2.0, 3.3, 0.75, "tiempo", 90, rb=0.38, tam=11, fuente=SANS)
bucle(g.shapes, 6.0, 3.3, 0.75, "botón", 90, rb=0.38, tam=11, fuente=SANS)
bucle(g.shapes, 4.0, 5.55, 0.7, "botón", 0, rb=0.32, tam=11, fuente=SANS)
m.clic(l, g)
g = m.grupo(l)
encabezados(g.shapes, 7.55, 1.6, [("estado", 2.0), ("botón", 1.6), ("tiempo", 1.6)], 0.38, tam=11)
filas_c = [("autos: verde", "autos: amarillo", "autos: verde"), ("autos: amarillo", "autos: amarillo", "peatones: verde"),
           ("peatones: verde", "peatones: verde", "autos: verde")]
for i, f in enumerate(filas_c):
    renglon(g.shapes, 7.55, 1.98 + i * 0.5, list(zip(f, (2.0, 1.6, 1.6))), 0.5, tam=10.5, negritas={0: True})
m.clic(l, g)
g = m.grupo(l)
tarjeta(g.shapes, 7.55, 3.8, 5.2, 2.7, "Lo que enseña", "• Los **bucles** importan: botón en amarillo, o tiempo "
        "sin botón, no cambian el estado. Si los olvidas, la tabla queda incompleta.\n• Sin doble círculo: es de "
        "**control**.\n• Finito: 3 estados.", tam=12)
m.clic(l, g)

# =====================================================================================
# FO · ¿Finito o no?
l = m.lamina("Ejercicio · ¿Alcanza un autómata finito?", "Para cada pregunta: ¿qué hay que recordar? ¿Tiene un "
             "límite fijo?", notas=(
    "La cuenta entre 3: al leer un dígito d, el residuo nuevo es (10·r + d) % 3. Sólo hay tres residuos "
    "posibles: 3 estados. Es el más sorprendente porque el número puede ser enorme. "
    "Contraseña de 8 o más: se cuenta hasta 8 y después ya no importa: 9 estados."))
encabezados(l.shapes, 0.55, 1.6, [("Pregunta", 5.4), ("¿Finito?", 1.4), ("Qué hay que recordar", 5.4)], 0.4, tam=12)
fo = [("¿La contraseña tiene al menos 8 caracteres?", "✓ sí", "cuántos llevo, hasta 8: «0, 1, …, 7, 8 o más» (9 estados)", VERDE),
      ("¿Se devolvieron todos los libros que se prestaron hoy?", "✗ no", "cuántos libros siguen prestados: no tiene tope", ROJO),
      ("¿El total de la cuenta se divide exacto entre 3 amigos?", "✓ sí", "leyendo dígito por dígito, sólo el residuo entre 3: 0, 1 o 2", VERDE),
      ("¿La palabra es palíndromo? (oso, reconocer)", "✗ no", "toda la primera mitad, y puede ser tan larga como quieras", ROJO),
      ("¿El correo termina en «.mx»?", "✓ sí", "los últimos 3 caracteres que leí (pocos casos)", VERDE),
      ("¿Metió tantas monedas de $5 como de $10?", "✗ no", "la diferencia entre las dos cuentas: sin tope", ROJO)]
for i, (q, r, por, col) in enumerate(fo):
    y = 2.0 + i * 0.6
    renglon(l.shapes, 0.55, y, [(q, 5.4), ("", 1.4), ("", 5.4)], 0.6, tam=12.5, alinear={0: "l"})
    g = m.grupo(l)
    caja_texto(g.shapes, 5.95, y, 1.4, 0.6, r, 13, col, VERDE_CL if col == VERDE else ROJO_CL, BORDE, True, redondeo=0)
    caja_texto(g.shapes, 7.35, y, 5.4, 0.6, por, 11.5, TEXTO, BLANCO, BORDE, alinear="l", redondeo=0)
    m.clic(l, g)
caja(l.shapes, 0.55, 5.8, 12.2, 0.7, AZUL_CL, None)
texto(l.shapes, 0.8, 5.88, 11.7, 0.55, "Truco: contar **hasta un número fijo** sí se puede con estados; contar **sin "
      "límite**, no. Para eso hace falta una pila o la cinta de una máquina de Turing.", 13, AZUL_OSC, ancla="m")

# =====================================================================================
# PEJ · Ejercicio de pila: biblioteca
l = m.lamina("Ejercicio · Autómata de pila: la biblioteca", "Cada préstamo apila un libro; cada devolución desapila "
             "uno. Al cerrar, ¿se devolvieron todos los libros?", notas=(
    "Es el mismo autómata del museo con otros nombres: «presta» = «entra», «devuelve» = «sale». Caso B: la segunda "
    "devolución llega con la pila vacía: se devolvió un libro que no estaba prestado. Error, y ahí se queda aunque "
    "después haya otro préstamo."))
casos_p = [("Caso A", ["presta", "presta", "devuelve", "presta", "devuelve", "devuelve"], [1, 2, 1, 2, 1, 0],
            "Pila vacía ⇒ **SÍ**: se devolvieron todos.", VERDE_CL, "14532D"),
           ("Caso B", ["presta", "devuelve", "devuelve", "presta"], [1, 0, -1, -1],
            "Error en el paso 3: se devolvió un libro que no estaba prestado.", ROJO_CL, ROJO)]
for j, (t, entrada, pilas, conclusion, f, col) in enumerate(casos_p):
    x = 0.55 + j * 6.2
    caja(l.shapes, x, 1.6, 6.0, 4.95, FONDO, BORDE)
    texto(l.shapes, x + 0.2, 1.68, 5.6, 0.3, f"{t}: " + ", ".join(entrada), 12, AZUL, True)
    encabezados(l.shapes, x + 0.2, 2.05, [("Paso", 0.8), ("Lee", 1.6), ("Libros prestados (pila)", 3.2)], 0.36, tam=11)
    for i, (lee, n) in enumerate(zip(entrada, pilas)):
        y = 2.41 + i * 0.44
        renglon(l.shapes, x + 0.2, y, [(str(i + 1), 0.8), (lee, 1.6), ("", 3.2)], 0.44, tam=12)
        g = m.grupo(l)
        if n < 0:
            texto(g.shapes, x + 2.7, y + 0.1, 3.0, 0.3, "error ✗", 12.5, ROJO, True)
        else:
            for k in range(n):
                s = g.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x + 2.75 + k * 0.36), Inches(y + 0.08), Inches(0.28),
                                       Inches(0.28))
                s.fill.solid(); s.fill.fore_color.rgb = rgb(AMBAR if k == n - 1 else "FDE68A")
                s.line.fill.background(); s.shadow.inherit = False
            if n == 0:
                texto(g.shapes, x + 2.75, y + 0.1, 1.5, 0.25, "(vacía)", 11, GRIS)
        m.clic(l, g)
    g = m.grupo(l)
    caja(g.shapes, x + 0.2, 5.3, 5.6, 1.05, f, None)
    texto(g.shapes, x + 0.35, 5.35, 5.3, 0.95, conclusion, 13, col, ancla="m")
    m.clic(l, g)

# =====================================================================================
# 37 · Ejercicios 3 y 4
l = m.lamina("Ejercicio 5 · Máquinas de Turing", "a: usa la tabla de reglas de sumar 1. "
             "b: una máquina nueva que invierte los bits.")
caja(l.shapes, 0.55, 1.55, 6.0, 4.95, FONDO, BORDE)
texto(l.shapes, 0.75, 1.68, 5.6, 0.3, "5a · 0111 + 1", 14, AZUL, True)
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
texto(l.shapes, 6.95, 1.68, 5.6, 0.3, "5b · Invertir los bits de 1011", 14, AZUL, True)
encabezados(l.shapes, 6.9, 2.05, [("Estado", 1.2), ("Lee", 0.75), ("Escribe", 1.0), ("Mueve", 0.85), ("Nuevo", 1.2)], 0.32, tam=10)
for i, f in enumerate([("invertir", "0", "1", "→", "invertir"), ("invertir", "1", "0", "→", "invertir"),
                       ("invertir", "□", "□", "—", "alto")]):
    renglon(l.shapes, 6.9, 2.37 + i * 0.32, list(zip(f, (1.2, 0.75, 1.0, 0.85, 1.2))), 0.32, tam=10.5, fuente=MONO)
encabezados(l.shapes, 6.9, 3.5, [("Paso", 0.6), ("Estado", 1.05), ("Cinta", 2.6), ("Hace", 1.45)], 0.3, tam=10)
e5b = [("0", "invertir", [B, "1", "0", "1", "1", B], 1, "inicio"),
       ("1", "invertir", [B, "0", "0", "1", "1", B], 2, "1 → 0"),
       ("2", "invertir", [B, "0", "1", "1", "1", B], 3, "0 → 1"),
       ("3", "invertir", [B, "0", "1", "0", "1", B], 4, "1 → 0"),
       ("4", "invertir", [B, "0", "1", "0", "0", B], 5, "1 → 0"),
       ("5", "alto", [B, "0", "1", "0", "0", B], 5, "□ · alto")]
for i, (p_, e, c, cab, q) in enumerate(e5b):
    g = m.grupo(l)
    y = 3.8 + i * 0.38
    renglon(g.shapes, 6.9, y, [(p_, 0.6), (e, 1.05), ("", 2.6), (q, 1.45)], 0.38, tam=10,
            colores={1: AZUL if e != "alto" else VERDE}, negritas={1: True}, fuente=(1,))
    cinta(g.shapes, 6.9 + 0.6 + 1.05 + 0.15, y + 0.04, c, cab, 0.3, 10)
    m.clic(l, g)
g = m.grupo(l)
texto(g.shapes, 6.95, 6.1, 5.6, 0.3, "Resultado: **0100**. Sólo camina a la derecha: nunca necesita regresar.", 11, "14532D")
m.clic(l, g)

# =====================================================================================
# 39 · Para llevar
l = m.oscura()
texto(l.shapes, 0.8, 0.55, 11, 0.6, "Para llevar", 30, BLANCO, True)
llevar = [("Lenguaje formal", "Alfabeto (símbolos permitidos) + reglas exactas. Python es uno: SyntaxError = «no pertenece»."),
          ("Autómata finito", "Estados y transiciones; su única memoria es el estado. Toda expresión regular es uno."),
          ("¿Finito o infinito?", "¿Lo que hay que recordar tiene un límite fijo? Si no, hace falta pila o cinta."),
          ("Del problema al código", "Problema → autómata (qué recordar) → diagrama (cómo recorrer) → Python."),
          ("Máquina de Turing", "Cinta + cabezal + estado + reglas. Calcula todo lo que tu laptop calcula."),
          ("Próxima sesión", "La historia: David Hilbert, Kurt Gödel, Alan Turing… y lo que NINGUNA máquina puede calcular.")]
for i, (t, c) in enumerate(llevar):
    x = 0.8 + (i % 3) * 3.95
    y = 1.6 + (i // 3) * 2.05
    caja(l.shapes, x, y, 3.75, 1.8, PIZARRA, None, 0.08)
    texto(l.shapes, x + 0.22, y + 0.2, 3.3, 0.3, t, 14, ACENTOS[i], True)
    texto(l.shapes, x + 0.22, y + 0.6, 3.3, 1.1, c, 12.5, "E2E8F0")
texto(l.shapes, 0.8, 5.95, 11.7, 0.8, "Antes de programar, pregúntate: ¿qué tiene que recordar mi programa? "
      "Esa respuesta es tu autómata.", 16, "CBD5E1", alinear="c")

# =====================================================================================
salida = Path(sys.argv[1])
salida.parent.mkdir(parents=True, exist_ok=True)
m.guardar(str(salida))
Path(sys.argv[2] if len(sys.argv) > 2 else salida.with_suffix(".notas.json")).write_text(json.dumps(m.notas, ensure_ascii=False, indent=1))
notas_json = Path(sys.argv[2] if len(sys.argv) > 2 else salida.with_suffix(".notas.json"))
notas_json.with_suffix(".gifs.json").write_text(json.dumps(m.gifs, ensure_ascii=False))
print(len(m.prs.slides), "láminas ·", m.clics_totales(), "clics →", salida)
