# Convención: toda variable o parámetro que guarda una lista empieza con lista_


# ---------------------------------------------------------------------------
# FUNCIONES Y VARIABLES
# ---------------------------------------------------------------------------


# Estructura general declaración de función:
def nombre_funcion(par_1, par_2, par_n):
    # La lógica de la función va aquí
    return 0


print(nombre_funcion(1, 2, 3))  # 0


# Estructura general declaración de variables:
def crear_perfil():
    usuario = "ana_gamer"  # Texto (str)
    nivel = 42  # Entero (int)
    horas_jugadas = 310.5  # Decimal (float)
    es_premium = True  # Booleano (bool)
    lista_juegos = ["Minecraft", "Fortnite", "Mario Kart"]  # Lista (list)
    perfil = {  # Diccionario (dict): junta todos los datos del perfil
        "usuario": usuario,
        "nivel": nivel,
        "horas_jugadas": horas_jugadas,
        "es_premium": es_premium,
        "juegos": lista_juegos,
    }
    return perfil


perfil_ana = crear_perfil()
print(perfil_ana["usuario"])  # ana_gamer
print(perfil_ana["juegos"])  # ['Minecraft', 'Fortnite', 'Mario Kart']


# ---------------------------------------------------------------------------
# CONDICIONALES
# ---------------------------------------------------------------------------


# Estructura general if sin else, uso 1: cambiar un valor por defecto
# (si no se cumple, el valor por defecto se queda como está):
def primera_cancion(lista_playlist):
    cancion = None  # valor por defecto
    if len(lista_playlist) > 0:
        cancion = lista_playlist[0]  # sólo cambia si se cumple la condición
    return cancion


print(primera_cancion(["Tusa", "La Bachata", "Ojitos Lindos"]))  # Tusa


# Estructura general if sin else, uso 2: validar un edge case
# (si se cumple, la función TERMINA con return; si no, sigue con el caso normal):
def primera_cancion(lista_playlist):
    if len(lista_playlist) == 0:  # edge case: la playlist está vacía
        return None  # la función termina aquí
    return lista_playlist[0]  # caso normal: sólo se llega si hay canciones


print(primera_cancion([]))  # None
print(primera_cancion(["Tusa", "La Bachata", "Ojitos Lindos"]))  # Tusa


# Estructura general if-else (dos caminos: siempre se toma uno de los dos):
def es_mayor_edad(edad):
    if edad >= 18:
        return True
    else:
        return False


print(es_mayor_edad(20))  # True


# La misma función, ahora la mayoría de edad también es un parámetro:
def es_mayor_edad(edad, mayoria_edad):
    if edad >= mayoria_edad:
        return True
    else:
        return False


print(es_mayor_edad(20, 21))  # False


# Estructura general if-elif-else (sólo se ejecuta UN camino, el primero que se cumple):
def plan_de_viernes(lista_amigos):
    if len(lista_amigos) == 0:
        return "maratón de series en casa"
    elif len(lista_amigos) == 1:
        return "ir al cine"
    elif len(lista_amigos) <= 5:
        return "noche de videojuegos"
    else:
        return "fiesta"


print(plan_de_viernes(["Ana", "Beto", "Caro"]))  # noche de videojuegos


# Estructura general ifs anidados (un if dentro de otro):
def acceso_concierto(lista_con_boleto, nombre, edad):
    if nombre in lista_con_boleto:
        if edad >= 18:
            return "pasa con pulsera de mayor de edad"
        else:
            return "pasa sin pulsera"
    else:
        return "no tienes boleto"


print(acceso_concierto(["Ana", "Beto", "Caro"], "Beto", 17))  # pasa sin pulsera


# Estructura general and (deben cumplirse las dos):
def puede_votar(edad, nacionalidad):
    return edad >= 18 and nacionalidad == "mexicana"


print(puede_votar(18, "mexicana"))  # True


# Estructura general or (basta con que se cumpla una):
def descuento_en_cine(dia, es_estudiante):
    return dia == "miercoles" or es_estudiante


print(descuento_en_cine("sabado", True))  # True


# Estructura general not (voltea True <-> False):
def falta_en_playlist(lista_playlist, cancion):
    return not (cancion in lista_playlist)


print(falta_en_playlist(["Tusa", "La Bachata"], "Ojitos Lindos"))  # True


# ---------------------------------------------------------------------------
# CICLO FOR Y ACUMULADORES
# ---------------------------------------------------------------------------


# Estructura general for por elementos + acumulador de suma:
def duracion_playlist(lista_minutos):
    total = 0  # 1. valor inicial del acumulador
    for minutos in lista_minutos:  # 2. recorrer
        total = total + minutos  # 3. actualizar el acumulador
    return total  # 4. regresar, FUERA del ciclo


print(duracion_playlist([3, 4, 2, 5]))  # 14


# Estructura general contador (acumulador que suma 1 si se cumple algo):
def contar_victorias(lista_resultados):
    victorias = 0
    for resultado in lista_resultados:
        if resultado == "G":
            victorias = victorias + 1
    return victorias


print(contar_victorias(["G", "P", "G", "E", "G"]))  # 3


# Estructura general acumulador multiplicativo (empieza en 1, no en 0):
def combinaciones_outfit(lista_opciones):
    combinaciones = 1
    for opciones in lista_opciones:
        combinaciones = combinaciones * opciones
    return combinaciones


print(combinaciones_outfit([3, 2, 4]))  # 24


# Estructura general acumulador del mínimo (empieza con el primer elemento):
def mejor_vuelta(lista_segundos):
    mejor = lista_segundos[0]
    for segundos in lista_segundos:
        if segundos < mejor:
            mejor = segundos
    return mejor


print(mejor_vuelta([92, 87, 95]))  # 87


# Estructura general acumulador de lista (construir una lista nueva):
def precios_al_alcance(lista_precios, presupuesto):
    lista_alcanzables = []
    for precio in lista_precios:
        if precio <= presupuesto:
            lista_alcanzables.append(precio)
    return lista_alcanzables


print(precios_al_alcance([1200, 499, 899, 1500], 900))  # [499, 899]


# Estructura general varios acumuladores en el mismo ciclo:
def promedio_goles(lista_goles):
    total = 0
    partidos = 0
    for goles in lista_goles:
        total = total + goles
        partidos = partidos + 1
    return total / partidos


print(promedio_goles([2, 0, 3, 1]))  # 1.5


# Estructura general for con índices (cuando importa la POSICIÓN):
def posicion_de_cancion(lista_playlist, cancion):
    for i in range(0, len(lista_playlist), 1):  # i = 0, 1, 2, ..., len - 1
        if lista_playlist[i] == cancion:
            return i  # termina la función en cuanto la encuentra
    return -1  # sólo llega aquí si revisó todo y no la encontró


print(posicion_de_cancion(["Tusa", "La Bachata", "Ojitos Lindos"], "La Bachata"))  # 1


# ---------------------------------------------------------------------------
# DIRECCIÓN DEL RECORRIDO
# ---------------------------------------------------------------------------


# Estructura general de izquierda a derecha:
def jornada_primera_victoria(lista_resultados):
    for i in range(0, len(lista_resultados), 1):  # 0, 1, 2, ..., len - 1
        if lista_resultados[i] == "G":
            return i + 1  # las posiciones empiezan en 0, las jornadas en 1
    return -1  # no hubo ninguna victoria


print(jornada_primera_victoria(["P", "G", "E", "G", "P"]))  # 2


# Estructura general de derecha a izquierda:
def jornada_ultima_victoria(lista_resultados):
    for i in range(len(lista_resultados) - 1, -1, -1):  # len - 1, ..., 2, 1, 0
        if lista_resultados[i] == "G":
            return i + 1  # las posiciones empiezan en 0, las jornadas en 1
    return -1  # no hubo ninguna victoria


print(jornada_ultima_victoria(["P", "G", "E", "G", "P"]))  # 4


# Estructura general de los dos extremos al centro, al mismo tiempo:
def es_palindromo(gamertag):
    izquierda = 0
    derecha = len(gamertag) - 1
    while izquierda < derecha:
        if gamertag[izquierda] != gamertag[derecha]:
            return False
        izquierda = izquierda + 1
        derecha = derecha - 1
    return True


print(es_palindromo("otto"))  # True


# Estructura general dos listas al mismo tiempo (mismo índice en ambas):
def aciertos_quiniela(lista_pronosticos, lista_resultados):
    aciertos = 0
    for i in range(0, len(lista_resultados), 1):
        if lista_pronosticos[i] == lista_resultados[i]:
            aciertos = aciertos + 1
    return aciertos


print(aciertos_quiniela(["L", "E", "V", "L"], ["L", "V", "V", "L"]))  # 3


# Estructura general recorrido circular con % (al llegar al final, vuelve al inicio):
def turnos_dj(lista_amigos, posicion_inicial, cantidad_canciones):
    lista_turnos = []
    posicion = posicion_inicial
    for turno in range(0, cantidad_canciones, 1):
        lista_turnos.append(lista_amigos[posicion])
        posicion = (posicion + 1) % len(lista_amigos)
    return lista_turnos


print(turnos_dj(["Ana", "Beto", "Caro"], 2, 4))  # ['Caro', 'Ana', 'Beto', 'Caro']


# ---------------------------------------------------------------------------
# CICLO WHILE
# ---------------------------------------------------------------------------


# Estructura general while (el mismo recorrido que un for, pero a mano):
def duracion_con_while(lista_minutos):
    total = 0
    i = 0  # 1. inicio
    while i < len(lista_minutos):  # 2. condición para seguir
        total = total + lista_minutos[i]
        i = i + 1  # 3. avance (sin esta línea, el ciclo es infinito)
    return total


print(duracion_con_while([3, 4, 2, 5]))  # 14


# Estructura general while que se detiene por una condición
# (no sabemos de antemano cuántas vueltas dará):
def semanas_para_boleto(lista_ahorros, precio):
    total = 0
    semanas = 0
    while semanas < len(lista_ahorros) and total < precio:
        total = total + lista_ahorros[semanas]
        semanas = semanas + 1
    if total < precio:  # edge case: se acabaron las semanas y no alcanzó
        return -1
    return semanas


print(semanas_para_boleto([200, 150, 300, 250], 500))  # 3
print(semanas_para_boleto([100, 50], 500))  # -1


# ---------------------------------------------------------------------------
# FOR DENTRO DE FOR
# ---------------------------------------------------------------------------


# Estructura general for dentro de for (lista de listas):
def goles_del_torneo(lista_jornadas):
    total = 0
    for lista_partidos in lista_jornadas:  # ciclo de afuera: cada jornada
        for goles in lista_partidos:  # ciclo de adentro: cada partido de esa jornada
            total = total + goles
    return total


print(goles_del_torneo([[2, 1, 3], [0, 4, 1]]))  # 11


# Estructura general for dentro de for (comparar cada elemento con los demás):
def parejas_de_juegos(lista_precios, presupuesto):
    parejas = 0
    for i in range(0, len(lista_precios), 1):
        for j in range(i + 1, len(lista_precios), 1):  # j empieza después de i
            if lista_precios[i] + lista_precios[j] <= presupuesto:
                parejas = parejas + 1
    return parejas


print(parejas_de_juegos([300, 500, 200, 700], 800))  # 3


# ---------------------------------------------------------------------------
# RECURSIVIDAD
# ---------------------------------------------------------------------------


# Estructura general recursividad (una función que se llama a sí misma):
def duracion_recursiva(lista_minutos):
    if len(lista_minutos) == 0:  # caso base: el problema más pequeño
        return 0
    else:  # caso recursivo: la primera canción + la duración del resto
        return lista_minutos[0] + duracion_recursiva(lista_minutos[1:])


print(duracion_recursiva([3, 4, 2, 5]))  # 14


# Estructura general recursividad con índice (sin crear listas nuevas):
def duracion_recursiva_indice(lista_minutos, i):
    if i == len(lista_minutos):  # caso base: ya no quedan canciones
        return 0
    else:
        return lista_minutos[i] + duracion_recursiva_indice(lista_minutos, i + 1)


print(duracion_recursiva_indice([3, 4, 2, 5], 0))  # 14


# ---------------------------------------------------------------------------
# LISTA DE DICCIONARIOS
# ---------------------------------------------------------------------------


# Estructura general recorrer una lista de diccionarios:
def goleadores(lista_jugadores):
    lista_goleadores = []
    for jugador in lista_jugadores:
        if jugador["goles"] >= 5:
            lista_goleadores.append(jugador["nombre"])
    return lista_goleadores


lista_equipo = [
    {"nombre": "Ana", "goles": 7},
    {"nombre": "Beto", "goles": 2},
    {"nombre": "Caro", "goles": 5},
]
print(goleadores(lista_equipo))  # ['Ana', 'Caro']

