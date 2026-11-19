"""GIF animados (ilustraciones propias) para la lámina «¿Qué significa autómata?» de la Clase 21.

    python3 herramientas/gifs_automatas.py herramientas/recursos

Genera elevador.gif (un elevador de 3 pisos que responde a sus botones) y semaforo.gif.
"""
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 480, 240
FONDO = (248, 250, 252)
MARINO = (15, 23, 42)
PIEDRA = (226, 232, 240)
PIEDRA_OSC = (148, 163, 184)
MADERA = (180, 83, 9)
MADERA_OSC = (120, 53, 15)
AMBAR = (251, 191, 36)
ROJO = (248, 113, 113)
NARANJA = (249, 115, 22)
VERDE = (74, 222, 128)
AZUL = (96, 165, 250)


def fuente(tam, nombre="Supplemental/Arial.ttf"):
    for ruta in (f"/System/Library/Fonts/{nombre}", "/System/Library/Fonts/Supplemental/Arial.ttf"):
        try:
            return ImageFont.truetype(ruta, tam)
        except OSError:
            continue
    return ImageFont.load_default()


def guardar(cuadros, ruta, duracion=90):
    cuadros[0].save(ruta, save_all=True, append_images=cuadros[1:], duration=duracion, loop=0, optimize=True)


def generar_elevador(ruta):
    """Elevador de 3 pisos: alguien aprieta un botón y el elevador sigue sus reglas."""
    pisos = ["PB", "1", "2"]
    y_piso = {0: 182, 1: 117, 2: 52}
    guion = []  # (posición en pisos, botón apretado, texto del estado)
    guion += [(0, None, "en PB · puertas abiertas")] * 8
    guion += [(0, 2, "en PB · botón 2")] * 4
    guion += [(k / 10, 2, "subiendo") for k in range(1, 21)]
    guion += [(2, None, "en piso 2 · puertas abiertas")] * 8
    guion += [(2, 0, "en piso 2 · botón PB")] * 4
    guion += [(2 - k / 10, 0, "bajando") for k in range(1, 21)]
    cuadros = []
    for posicion, boton, texto_estado in guion:
        im = Image.new("RGB", (W, H), FONDO)
        d = ImageDraw.Draw(im)
        d.rectangle([150, 20, 250, 220], fill=(255, 255, 255), outline=PIEDRA_OSC, width=3)
        for k, nombre in enumerate(pisos):
            y = y_piso[k]
            d.line([(150, y + 38), (250, y + 38)], fill=PIEDRA, width=2)
            d.text((115, y + 8), nombre, font=fuente(18), fill=(71, 85, 105))
        y = 182 - posicion * 65
        abiertas = posicion in (0, 2) and boton is None
        d.rectangle([160, y - 6, 240, y + 36], fill=AZUL if not abiertas else (219, 234, 254), outline=MARINO, width=2)
        if abiertas:
            d.ellipse([190, y + 2, 210, y + 22], fill=MARINO)
        # botonera
        d.rounded_rectangle([300, 40, 380, 200], 10, fill=MARINO)
        for k, nombre in enumerate(reversed(pisos)):
            n = len(pisos) - 1 - k
            cy = 75 + k * 45
            encendido = boton == n
            d.ellipse([322, cy - 16, 358, cy + 16], fill=AMBAR if encendido else (51, 65, 85))
            d.text((340, cy), nombre, font=fuente(14), fill=MARINO if encendido else (255, 255, 255), anchor="mm")
        d.text((W // 2, 226), "estado: " + texto_estado, font=fuente(15), fill=(71, 85, 105), anchor="mm")
        cuadros.append(im)
    guardar(cuadros, ruta, 100)


def generar_semaforo(ruta):
    cuadros = []
    secuencia = [("verde", VERDE)] * 14 + [("amarillo", AMBAR)] * 6 + [("rojo", ROJO)] * 14
    for nombre, activo in secuencia:
        im = Image.new("RGB", (W, H), FONDO)
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([200, 15, 280, 200], 14, fill=MARINO)
        for k, col in enumerate((ROJO, AMBAR, VERDE)):
            y = 48 + k * 58
            d.ellipse([218, y - 23, 262, y + 23], fill=col if col == activo else (51, 65, 85))
        d.text((W // 2, 222), "estado: " + nombre, font=fuente(15), fill=(71, 85, 105), anchor="mm")
        cuadros.append(im)
    guardar(cuadros, ruta, 120)


if __name__ == "__main__":
    destino = Path(sys.argv[1] if len(sys.argv) > 1 else "herramientas/recursos")
    destino.mkdir(parents=True, exist_ok=True)
    generar_elevador(destino / "elevador.gif")
    generar_semaforo(destino / "semaforo.gif")
    print("GIF listos en", destino)
