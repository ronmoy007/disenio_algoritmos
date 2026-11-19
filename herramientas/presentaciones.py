"""Utilidades para generar las presentaciones del curso (python-pptx → Keynote).

Estilo del curso: 13.33 × 7.5 in, portada azul marino 0F172A, contenido en blanco con
paleta slate, código en recuadro oscuro con colores tipo VS Code (Menlo) y texto en
Helvetica Neue. Lo que se revela «al hacer clic» se agrupa y se le agrega un <p:timing>
con efecto «aparecer» (o «desaparecer»), que Keynote importa como builds.

Las notas del presentador NO se escriben con notes_slide (Keynote marca el archivo como
inválido): se regresan en `Mazo.notas` y se ponen después desde AppleScript.
"""
import re
from lxml import etree
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn

# ---------------------------------------------------------------- paleta
MARINO = "0F172A"; PIZARRA = "1E293B"; TENUE = "64748B"; GRIS = "94A3B8"
BORDE = "E2E8F0"; FONDO = "F8FAFC"; AZUL = "2563EB"; AZUL_OSC = "1E3A8A"
TEXTO = "334155"; BLANCO = "FFFFFF"
VERDE = "15803D"; VERDE_CL = "DCFCE7"; ROJO = "B91C1C"; ROJO_CL = "FEE2E2"
AMBAR = "B45309"; AMBAR_CL = "FEF3C7"; AZUL_CL = "DBEAFE"; MORADO = "6D28D9"; MORADO_CL = "EDE9FE"
ACENTOS = ["F87171", "60A5FA", "A78BFA", "4ADE80", "FBBF24", "22D3EE"]

SANS = "Helvetica Neue"
MONO = "Menlo"

# colores tipo VS Code
_VS = {"kw": "C586C0", "def": "569CD6", "fn": "DCDCAA", "str": "CE9178", "num": "B5CEA8",
       "com": "6A9955", "txt": "D4D4D4", "lin": "64748B"}
_CONTROL = {"if", "elif", "else", "for", "while", "return", "in", "import", "from", "break", "continue"}
_DEF = {"def", "True", "False", "None", "and", "or", "not"}
_BUILTIN = {"print", "len", "range", "int", "str", "float", "type", "input", "round", "abs", "min", "max"}


def rgb(h):
    return RGBColor.from_string(h)


# ---------------------------------------------------------------- texto
def _fuente(run, tam, color, negritas=False, fuente=SANS, cursiva=False):
    f = run.font
    f.size = Pt(tam)
    f.bold = negritas
    f.italic = cursiva
    f.name = fuente
    f.color.rgb = rgb(color)
    rPr = run._r.get_or_add_rPr()
    for etiqueta in ("a:ea", "a:cs"):
        e = rPr.find(qn(etiqueta))
        if e is None:
            e = etree.SubElement(rPr, qn(etiqueta))
        e.set("typeface", fuente)


def _partes(linea):
    """Divide «**negritas**» y «`código`» en pedazos (texto, negritas, código)."""
    salida = []
    for trozo in re.split(r"(\*\*[^*]+\*\*|`[^`]+`)", linea):
        if not trozo:
            continue
        if trozo.startswith("**"):
            salida.append((trozo[2:-2], True, False))
        elif trozo.startswith("`"):
            salida.append((trozo[1:-1], False, True))
        else:
            salida.append((trozo, False, False))
    return salida


def texto(formas, x, y, w, h, contenido, tam=14, color=TEXTO, negritas=False, alinear="l",
          ancla="t", fuente=SANS, interlineado=None, color_codigo=AZUL_OSC, espacio_despues=0):
    """Caja de texto. `contenido` admite \\n (párrafos), **negritas** y `código`."""
    caja = formas.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = caja.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}[ancla]
    for i, linea in enumerate(contenido.split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[alinear]
        if interlineado:
            p.line_spacing = interlineado
        if espacio_despues:
            p.space_after = Pt(espacio_despues)
        partes = _partes(linea) or [("", False, False)]
        for t, b, c in partes:
            r = p.add_run()
            r.text = t
            if c:
                _fuente(r, tam * 0.92, color_codigo, negritas, MONO)
            else:
                _fuente(r, tam, color, negritas or b, fuente)
    return caja


def caja(formas, x, y, w, h, relleno=FONDO, borde=BORDE, redondeo=0.06, forma=None, grosor=1.0):
    tipo = forma or (MSO_SHAPE.ROUNDED_RECTANGLE if redondeo else MSO_SHAPE.RECTANGLE)
    s = formas.add_shape(tipo, Inches(x), Inches(y), Inches(w), Inches(h))
    if tipo == MSO_SHAPE.ROUNDED_RECTANGLE:
        s.adjustments[0] = min(0.5, redondeo / max(0.01, min(w, h)) * 1.0)
    if relleno:
        s.fill.solid()
        s.fill.fore_color.rgb = rgb(relleno)
    else:
        s.fill.background()
    if borde:
        s.line.color.rgb = rgb(borde)
        s.line.width = Pt(grosor)
    else:
        s.line.fill.background()
    s.shadow.inherit = False
    return s


def caja_texto(formas, x, y, w, h, contenido, tam=14, color=TEXTO, relleno=FONDO, borde=BORDE,
               negritas=False, alinear="c", ancla="m", fuente=SANS, redondeo=0.06, grosor=1.0):
    """Forma con texto adentro (centrado por omisión)."""
    s = caja(formas, x, y, w, h, relleno, borde, redondeo, grosor=grosor)
    tf = s.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.06)
    tf.margin_top = tf.margin_bottom = Inches(0.02)
    tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}[ancla]
    for i, linea in enumerate(contenido.split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[alinear]
        for t, b, c in (_partes(linea) or [("", False, False)]):
            r = p.add_run()
            r.text = t
            _fuente(r, tam, color, negritas or b, MONO if c else fuente)
    return s


def tarjeta(formas, x, y, w, h, titulo, cuerpo="", relleno=FONDO, borde=BORDE, color_titulo=AZUL,
            tam_titulo=13, tam=12, color=TEXTO, etiqueta=None, color_etiqueta=GRIS):
    """Tarjeta como las de la Clase 19: título de color y texto debajo."""
    caja(formas, x, y, w, h, relleno, borde)
    yy = y + 0.13
    if etiqueta:
        texto(formas, x + 0.18, yy, w - 0.36, 0.2, etiqueta, 9, color_etiqueta, True)
        yy += 0.24
    texto(formas, x + 0.18, yy, w - 0.36, 0.3, titulo, tam_titulo, color_titulo, True)
    if cuerpo:
        texto(formas, x + 0.18, yy + tam_titulo / 72 * 1.55, w - 0.36,
              h - (yy - y) - 0.3, cuerpo, tam, color, interlineado=1.08)


# ---------------------------------------------------------------- código
def _tokens(linea):
    """Colorea una línea de Python al estilo VS Code."""
    salida = []
    patron = re.compile(r'(#.*$)|("[^"]*"|\'[^\']*\')|(\b\d+(?:\.\d+)?\b)|([A-Za-z_áéíóúñ][A-Za-z_0-9áéíóúñ]*)|(\s+)|(.)')
    previo = ""
    for m in patron.finditer(linea):
        com, cad, num, pal, esp, otro = m.groups()
        if com:
            salida.append((com, _VS["com"]))
        elif cad:
            salida.append((cad, _VS["str"]))
        elif num:
            salida.append((num, _VS["num"]))
        elif pal:
            resto = linea[m.end():]
            if pal in _CONTROL:
                c = _VS["kw"]
            elif pal in _DEF:
                c = _VS["def"]
            elif previo == "def" or pal in _BUILTIN or resto.startswith("("):
                c = _VS["fn"]
            else:
                c = "9CDCFE"
            salida.append((pal, c))
            previo = pal
        elif esp:
            salida.append((esp, _VS["txt"]))
        else:
            salida.append((otro, _VS["txt"]))
    return salida


def codigo(formas, x, y, w, h, fuente_py, tam=12, etiqueta="Python", numeros=True, relleno=PIZARRA):
    """Recuadro oscuro con código coloreado. Regresa la altura de renglón (in) y la y del renglón 1."""
    caja(formas, x, y, w, h, relleno, None, 0.08)
    if etiqueta:
        texto(formas, x + 0.22, y + 0.12, w - 0.4, 0.2, etiqueta, 11, GRIS, True)
    y0 = y + (0.42 if etiqueta else 0.18)
    tb = formas.add_textbox(Inches(x + 0.18), Inches(y0), Inches(w - 0.3), Inches(h - (y0 - y) - 0.1))
    tf = tb.text_frame
    tf.word_wrap = False
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    lineas = fuente_py.rstrip("\n").split("\n")
    ancho = len(str(len(lineas)))
    for i, linea in enumerate(lineas):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.line_spacing = 1.0
        if numeros:
            r = p.add_run()
            r.text = f"{i + 1:>{ancho}}  "
            _fuente(r, tam, _VS["lin"], fuente=MONO)
        for t, c in (_tokens(linea) or [(" ", _VS["txt"])]):
            r = p.add_run()
            r.text = t
            _fuente(r, tam, c, fuente=MONO)
    alto_renglon = tam * 1.2 / 72
    return alto_renglon, y0


# ---------------------------------------------------------------- líneas y flechas
def flecha(formas, x1, y1, x2, y2, color=TEXTO, grosor=1.5, punta=True, punteada=False):
    c = formas.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    c.line.color.rgb = rgb(color)
    c.line.width = Pt(grosor)
    ln = c.line._get_or_add_ln()
    if punteada:
        d = etree.SubElement(ln, qn("a:prstDash"))
        d.set("val", "dash")
    if punta:
        t = etree.SubElement(ln, qn("a:tailEnd"))
        t.set("type", "triangle")
        t.set("w", "med")
        t.set("len", "med")
    return c


def estado(formas, cx, cy, r, nombre, aceptacion=False, relleno=BLANCO, borde=AZUL_OSC, tam=13,
           color=MARINO):
    """Círculo de un autómata; doble círculo si es de aceptación."""
    s = formas.add_shape(MSO_SHAPE.OVAL, Inches(cx - r), Inches(cy - r), Inches(2 * r), Inches(2 * r))
    s.fill.solid(); s.fill.fore_color.rgb = rgb(relleno)
    s.line.color.rgb = rgb(borde); s.line.width = Pt(2)
    s.shadow.inherit = False
    if aceptacion:
        r2 = r - 0.07
        t = formas.add_shape(MSO_SHAPE.OVAL, Inches(cx - r2), Inches(cy - r2), Inches(2 * r2), Inches(2 * r2))
        t.fill.background(); t.line.color.rgb = rgb(borde); t.line.width = Pt(1.5)
        t.shadow.inherit = False
    texto(formas, cx - r, cy - 0.15, 2 * r, 0.3, nombre, tam, color, True, "c", "m")
    return s


def bucle(formas, cx, cy, r, etiqueta="", angulo=90, rb=None, color=MARINO, color_etiqueta=AZUL, tam=14,
          fuente=MONO, grosor=2):
    """Transición de un estado a sí mismo: un lazo grande que sale del círculo (cx, cy, r) y vuelve a
    entrar con punta de flecha. angulo: 90 = arriba, 270 = abajo, 0 = derecha, 180 = izquierda."""
    import math
    rb = rb or max(0.3, r * 0.6)
    d = r + rb * 0.45
    a = math.radians(angulo)
    ox, oy = cx + d * math.cos(a), cy - d * math.sin(a)

    def punto(t):
        return ox + rb * math.cos(t), oy - rb * math.sin(t)

    def fuera(t):
        x, y = punto(t)
        return math.hypot(x - cx, y - cy) > r + 0.01
    paso = math.radians(1)
    t_izq = a
    while fuera(t_izq + paso):
        t_izq += paso
    t_der = a
    while fuera(t_der - paso):
        t_der -= paso
    puntos = []
    t = t_izq
    while t >= t_der:
        puntos.append(punto(t))
        t -= paso
    puntos.append(punto(t_der))
    emu = [(int(Inches(x)), int(Inches(y))) for x, y in puntos]
    fb = formas.build_freeform(emu[0][0], emu[0][1], scale=1.0)
    fb.add_line_segments(emu[1:], close=False)
    s = fb.convert_to_shape()
    s.fill.background()
    s.line.color.rgb = rgb(color)
    s.line.width = Pt(grosor)
    s.shadow.inherit = False
    ln = s.line._get_or_add_ln()
    t_ = etree.SubElement(ln, qn("a:tailEnd"))
    t_.set("type", "triangle"); t_.set("w", "med"); t_.set("len", "med")
    if etiqueta:
        ex, ey = cx + (d + rb + 0.2) * math.cos(a), cy - (d + rb + 0.2) * math.sin(a)
        texto(formas, ex - 0.9, ey - 0.17, 1.8, 0.34, etiqueta, tam, color_etiqueta, True, "c", "m", fuente=fuente)
    return s


# ---------------------------------------------------------------- animaciones
_P = "http://schemas.openxmlformats.org/presentationml/2006/main"


def _efecto(cid, spid, entrada, primero):
    clase = "entr" if entrada else "exit"
    nodo = "clickEffect" if primero else "withEffect"
    valor = "visible" if entrada else "hidden"
    return (f'<p:par><p:cTn id="{cid}" presetID="1" presetClass="{clase}" presetSubtype="0" fill="hold" '
            f'nodeType="{nodo}"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>'
            f'<p:set><p:cBhvr><p:cTn id="{cid + 1}" dur="1" fill="hold"><p:stCondLst><p:cond delay="0"/>'
            f'</p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl><p:attrNameLst>'
            f'<p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr><p:to>'
            f'<p:strVal val="{valor}"/></p:to></p:set></p:childTnLst></p:cTn></p:par>')


def animar(lamina, clics):
    """clics: lista de clics; cada clic es una lista de (forma, True=aparece / False=desaparece)."""
    clics = [c for c in clics if c]
    if not clics:
        return
    cid = 3
    pasos = []
    for clic in clics:
        efectos = []
        externo, interno = cid, cid + 1
        cid += 2
        for k, (forma, entrada) in enumerate(clic):
            efectos.append(_efecto(cid, forma.shape_id, entrada, k == 0))
            cid += 2
        pasos.append(f'<p:par><p:cTn id="{externo}" fill="hold"><p:stCondLst><p:cond delay="indefinite"/>'
                     f'</p:stCondLst><p:childTnLst><p:par><p:cTn id="{interno}" fill="hold"><p:stCondLst>'
                     f'<p:cond delay="0"/></p:stCondLst><p:childTnLst>{"".join(efectos)}</p:childTnLst>'
                     f'</p:cTn></p:par></p:childTnLst></p:cTn></p:par>')
    xml = (f'<p:timing xmlns:p="{_P}"><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" '
           f'nodeType="tmRoot"><p:childTnLst><p:seq concurrent="1" nextAc="seek"><p:cTn id="2" '
           f'dur="indefinite" nodeType="mainSeq"><p:childTnLst>{"".join(pasos)}</p:childTnLst></p:cTn>'
           f'<p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond>'
           f'</p:prevCondLst><p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/>'
           f'</p:tgtEl></p:cond></p:nextCondLst></p:seq></p:childTnLst></p:cTn></p:par></p:tnLst>'
           f'</p:timing>')
    sld = lamina._element
    viejo = sld.find(qn("p:timing"))
    if viejo is not None:
        sld.remove(viejo)
    nodo = etree.fromstring(xml)
    ext = sld.find(qn("p:extLst"))
    if ext is not None:
        ext.addprevious(nodo)
    else:
        sld.append(nodo)


# ---------------------------------------------------------------- mazo
class Mazo:
    def __init__(self):
        self.prs = Presentation()
        self.prs.slide_width = Inches(13.333)
        self.prs.slide_height = Inches(7.5)
        self.notas = []
        self._clics = {}

    def _nueva(self, fondo=None, notas=""):
        lamina = self.prs.slides.add_slide(self.prs.slide_layouts[6])
        if fondo:
            caja(lamina.shapes, 0, 0, 13.333, 7.5, fondo, None, 0)
        self.notas.append(notas)
        self._clics[id(lamina)] = []
        return lamina

    def numero(self, lamina, oscuro=False):
        n = len(self.prs.slides)
        texto(lamina.shapes, 12.3, 7.07, 0.6, 0.18, str(n), 10, "475569" if oscuro else GRIS, alinear="r")

    def lamina(self, titulo, subtitulo="", notas=""):
        l = self._nueva(notas=notas)
        texto(l.shapes, 0.55, 0.4, 12.2, 0.5, titulo, 28, MARINO, True)
        if subtitulo:
            texto(l.shapes, 0.55, 1.0, 12.2, 0.3, subtitulo, 15, TENUE)
        self.numero(l)
        return l

    def oscura(self, notas=""):
        l = self._nueva(MARINO, notas)
        self.numero(l, True)
        return l

    def separador(self, contador, titulo, texto_, color="F87171", notas=""):
        l = self.oscura(notas)
        texto(l.shapes, 0.8, 2.55, 11, 0.3, contador, 14, color, True)
        texto(l.shapes, 0.8, 2.95, 11.5, 0.8, titulo, 40, BLANCO, True)
        texto(l.shapes, 0.8, 3.9, 11, 0.8, texto_, 17, "CBD5E1")
        return l

    # --- clics
    def grupo(self, lamina):
        """Grupo nuevo: lo que se dibuje en g.shapes aparece en un mismo clic."""
        return lamina.shapes.add_group_shape()

    def clic(self, lamina, *formas, salen=()):
        """Registra un clic: las `formas` aparecen y las de `salen` desaparecen."""
        self._clics[id(lamina)].append([(f, True) for f in formas] + [(f, False) for f in salen])

    def guardar(self, ruta):
        for lamina in self.prs.slides:
            animar(lamina, self._clics.get(id(lamina), []))
        self.prs.save(ruta)
        return ruta

    def clics_totales(self):
        return sum(len([c for c in v if c]) for v in self._clics.values())


# ---------------------------------------------------------------- diagramas de flujo (estilo Clase 15 / plataforma)
FL_FLECHA = "64748B"
_FL = {"terminal": ("1E293B", None, "FFFFFF", True), "proceso": ("DBEAFE", "2563EB", "1E3A8A", False),
       "decision": ("FEF3C7", "D97706", "92400E", False), "ciclo": ("DCFCE7", "16A34A", "166534", False),
       "salida": ("EDE9FE", "7C3AED", "5B21B6", False)}


def fl_figura(formas, tipo, cx, y, w, h, contenido, tam=10):
    """Figura de diagrama de flujo centrada en cx: terminal, proceso, decision, ciclo o salida.
    Regresa (arriba, abajo, izquierda, derecha) como puntos (x, y) para conectar flechas."""
    relleno, borde, color, negritas = _FL[tipo]
    forma = {"terminal": MSO_SHAPE.ROUNDED_RECTANGLE, "proceso": MSO_SHAPE.RECTANGLE,
             "decision": MSO_SHAPE.DIAMOND, "ciclo": MSO_SHAPE.HEXAGON, "salida": MSO_SHAPE.PARALLELOGRAM}[tipo]
    x = cx - w / 2
    s = formas.add_shape(forma, Inches(x), Inches(y), Inches(w), Inches(h))
    if tipo == "terminal":
        s.adjustments[0] = 0.5
    if tipo == "ciclo":
        s.adjustments[0] = 0.3
    s.fill.solid(); s.fill.fore_color.rgb = rgb(relleno)
    if borde:
        s.line.color.rgb = rgb(borde); s.line.width = Pt(1.25)
    else:
        s.line.fill.background()
    s.shadow.inherit = False
    texto(formas, x - 0.3, y, w + 0.6, h, contenido, tam, color, negritas, "c", "m", fuente=MONO)
    return (cx, y), (cx, y + h), (x, y + h / 2), (x + w, y + h / 2)


def fl_linea(formas, puntos, punta=True, color=FL_FLECHA):
    """Polilínea de flechas entre puntos (x, y); sólo el último tramo lleva punta."""
    for k in range(len(puntos) - 1):
        (x1, y1), (x2, y2) = puntos[k], puntos[k + 1]
        flecha(formas, x1, y1, x2, y2, color, 1.25, punta=punta and k == len(puntos) - 2)


def fl_etiqueta(formas, x, y, contenido, tam=8.5):
    texto(formas, x, y, 1.0, 0.2, contenido, tam, "334155", True)
