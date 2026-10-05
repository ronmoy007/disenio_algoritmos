# Diseño de algoritmos

Material del curso de Diseño de algoritmos: presentaciones y código de cada clase,
y las actividades que se califican.

## Actividades y fechas de entrega

| Actividad | Instrucciones | Fecha de entrega |
|---|---|---|
| Primer parcial | — | Jueves 8 de octubre de 2026 |
| Actividad 1: Variables, tipos de datos, funciones y ciclos | [instrucciones_actividad_1.md](actividades/instrucciones_actividad_1.md) | Martes 13 de octubre de 2026 |

## Estructura del repositorio

```
disenio_algoritmos/
├── README.md
├── actividades/      ← instrucciones y pruebas automáticas de cada actividad
└── sesiones/         ← material de cada clase, en carpetas MM_DD (mes_día)
```

## Sesiones

| Fecha | Clase | Carpeta |
|---|---|---|
| 10 de septiembre | Clase 2: Diseño de algoritmos | [sesiones/09_10](sesiones/09_10) |
| 17 de septiembre | Clase 3: Ciclo de vida de un programa | [sesiones/09_17](sesiones/09_17) |
| 22 de septiembre | Clase 4: Entorno de Python | [sesiones/09_22](sesiones/09_22) |
| 24 de septiembre | Clase 5: Estructura e identificadores | [sesiones/09_24](sesiones/09_24) |
| 29 de septiembre | Clase 6: Big O, variables y tipos de datos | [sesiones/09_29](sesiones/09_29) |
| 1 de octubre | Clase 7: Recursividad, arreglos y registros | [sesiones/10_01](sesiones/10_01) |

## Cómo revisar una actividad

Cada actividad trae un archivo de pruebas (`test_actividad_N.py`) que califica tu trabajo
automáticamente con `pytest`.

1. Crea un entorno virtual e instala pytest (solo la primera vez).
   Abre una terminal en la **carpeta principal del repositorio** y ejecuta:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate        # En Windows: .venv\Scripts\activate
   python3 -m pip install pytest
   ```
2. Cada vez que abras una terminal nueva, activa el entorno virtual, entra a la carpeta
   `actividades` y corre las pruebas de la actividad (por ejemplo, la 1):
   ```bash
   source .venv/bin/activate        # En Windows: .venv\Scripts\activate
   cd actividades
   pytest test_actividad_1.py -v
   ```

Los detalles de cada actividad están en su archivo de instrucciones.
