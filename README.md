# Diseño de algoritmos

Material del curso de Diseño de algoritmos: presentaciones y código de cada clase,
y las actividades que se califican.

## Actividades y fechas de entrega

| Actividad | Instrucciones | Fecha de entrega |
|---|---|---|
| Primer parcial | — | Jueves 8 de octubre de 2026 |
| Actividad 1: Variables, tipos de datos, funciones y ciclos | [instrucciones_actividad_1.md](actividades/instrucciones_actividad_1.md) | Martes 13 de octubre de 2026 |
| Actividad 2: Recursividad | [instrucciones_actividad_2.md](actividades/instrucciones_actividad_2.md) | Jueves 15 de octubre de 2026 |

## Cómo entregar una actividad

Envía tu actividad por correo a **marco.monroy.engineer@gmail.com**.

Los correos se revisan con un programa automático, así que es muy importante que
sigas **exactamente** este formato. Si no lo sigues, tu actividad podría no registrarse.

### Reglas

1. Manda **un correo por actividad**.
2. Adjunta **solo** tu archivo `.py`, con el nombre exacto que pide la actividad
   (por ejemplo, `actividad_2.py`). No lo mandes en `.zip`, ni como enlace de Drive,
   ni pegado en el cuerpo del correo.
3. Copia el asunto y el cuerpo de la plantilla y **cambia solo los datos de ejemplo** por los tuyos.
   No cambies las palabras antes de los dos puntos (`:`).
4. Si necesitas corregir algo, manda un correo nuevo con el mismo formato.
   Se califica el **último** correo que llegue antes de la fecha de entrega.

### Plantilla

**Asunto:**

```
[DISENIO-ALGORITMOS] actividad_2 - 312345678
```

**Cuerpo:**

```
Nombre: Ana López García
Grupo: 1101
Numero de cuenta: 312345678
Actividad: actividad_2
```

**Archivo adjunto:** `actividad_2.py`

En el asunto, cambia `actividad_2` por la actividad que entregas y `312345678` por tu
número de cuenta (solo números, sin espacios ni guiones).

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

## Instalar Python y VS Code

Para el curso necesitas dos programas:

- **Python** (versión **3.10 o más nueva**): el lenguaje con el que vamos a programar.
- **Visual Studio Code (VS Code)**: el editor donde vas a escribir y ejecutar tu código.

Sigue solo las instrucciones de tu sistema operativo.

### Windows

**Python**

1. Entra a [python.org/downloads](https://www.python.org/downloads/) y descarga la versión
   más reciente con el botón amarillo **Download Python 3.x.x**.
2. Abre el instalador. **Antes de dar clic en "Install Now"**, marca la casilla
   **"Add python.exe to PATH"** (abajo de la ventana).
   > Si no marcas esta casilla, la terminal no va a reconocer el comando `python`.
   > Si ya instalaste sin marcarla, vuelve a abrir el instalador, elige **Modify** y actívala,
   > o desinstala Python y vuelve a instalarlo.
3. Da clic en **Install Now** y espera a que termine.
4. Abre **PowerShell** (búscalo en el menú Inicio) y escribe:
   ```powershell
   python --version
   ```
   Debe aparecer algo como `Python 3.13.1`.

> **Importante:** en Windows el comando es **`python`**, no `python3`. En todas las
> instrucciones del curso, cuando veas `python3`, escribe `python`.
> Si al escribir `python` se abre la Microsoft Store, Python no quedó en el PATH: revisa el paso 2.

**VS Code**

1. Entra a [code.visualstudio.com](https://code.visualstudio.com/) y descarga la versión para Windows.
2. Abre el instalador y acepta las opciones. En la pantalla **"Select Additional Tasks"**
   deja marcada la opción **"Add to PATH"**.
3. Cuando termine, abre VS Code.

### macOS

**Python**

macOS puede traer un Python antiguo o ninguno, así que instala uno nuevo:

1. Entra a [python.org/downloads](https://www.python.org/downloads/) y descarga la versión
   más reciente para macOS (**Download Python 3.x.x**).
2. Abre el archivo `.pkg` y sigue los pasos del instalador.
3. Abre la app **Terminal** (búscala con `Cmd + Espacio`) y escribe:
   ```bash
   python3 --version
   ```
   Debe aparecer algo como `Python 3.13.1`.

> Si ya usas [Homebrew](https://brew.sh/), también puedes instalarlo con `brew install python`.
>
> En macOS el comando es **`python3`** (no `python`).

**VS Code**

1. Entra a [code.visualstudio.com](https://code.visualstudio.com/) y descarga la versión para macOS.
2. Abre el archivo descargado y **arrastra Visual Studio Code a la carpeta Aplicaciones**.
3. Abre VS Code desde Aplicaciones.
4. (Opcional) Para abrir VS Code desde la terminal con el comando `code`: en VS Code presiona
   `Cmd + Shift + P`, escribe **Shell Command: Install 'code' command in PATH** y presiona Enter.

### Linux

**Python**

La mayoría de las distribuciones ya traen Python 3. Revisa tu versión en una terminal:

```bash
python3 --version
```

Además necesitas instalar los paquetes para crear entornos virtuales y usar `pip`:

- **Ubuntu / Debian / Linux Mint:**
  ```bash
  sudo apt update
  sudo apt install python3 python3-venv python3-pip
  ```
- **Fedora:**
  ```bash
  sudo dnf install python3 python3-pip
  ```

> En Ubuntu, si te falta `python3-venv`, el comando `python3 -m venv .venv` falla con el
> error `ensurepip is not available`.

**VS Code**

- **Ubuntu / Debian / Linux Mint:** descarga el archivo **.deb** de
  [code.visualstudio.com](https://code.visualstudio.com/) y, desde la carpeta de descargas, ejecuta:
  ```bash
  sudo apt install ./code_*.deb
  ```
- **Fedora:** descarga el archivo **.rpm** de [code.visualstudio.com](https://code.visualstudio.com/) y ejecuta:
  ```bash
  sudo dnf install ./code-*.rpm
  ```

### Configurar VS Code (todos los sistemas)

1. Abre VS Code y ve a la sección de **Extensiones** (el ícono de cuadritos en la barra
   izquierda, o `Ctrl + Shift + X`; en Mac `Cmd + Shift + X`).
2. Busca **Python** e instala la extensión de **Microsoft**.
3. Abre la carpeta del repositorio con **File → Open Folder...** (Archivo → Abrir carpeta).
4. Abre una terminal dentro de VS Code con **Terminal → New Terminal**. Ahí vas a escribir
   los comandos de la siguiente sección.
5. Después de crear el entorno virtual (paso 1 de la siguiente sección), presiona
   `Ctrl + Shift + P` (en Mac `Cmd + Shift + P`), escribe **Python: Select Interpreter**
   y elige el que dice **`.venv`**.

## Cómo revisar una actividad

Cada actividad trae un archivo de pruebas (`test_actividad_N.py`) que califica tu trabajo
automáticamente con `pytest`.

> **En Windows:** escribe `python` en lugar de `python3`. Si al activar el entorno virtual
> en PowerShell aparece un error que menciona *"running scripts is disabled"*, ejecuta una sola vez
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, responde `S` (o `Y`) y vuelve a intentarlo.

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
