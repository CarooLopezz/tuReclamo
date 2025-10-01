TuReclamo es una app que busca agilizar un reclamo de ciudadano ante un municipio de Mendoza.
Integrantes:
Adriana Antunez
Iara Fernandez
Lara Magallanes
Carolina Lopez

Entidades principales (mínimo 3)

USUARIO

    PK: id_usuario

    Atributos: nombre, apellido, DNI, correo, direccion, tipo_usuario (puede ser vecino o administrador)

RECLAMO 

    PK: id_reclamo

    Atributos: descripcion, fecha_creacion, estado, ubicacion

FK:

     id_vecino → referencia a Usuario (cuando es tipo "vecino")

     id_administrador → referencia a Usuario (cuando es tipo "administrador")

     id_sector → referencia a Sector

SECTOR (o DirectorSector)

     PK: id_sector

    Atributos: nombre_sector, descripcion

    Relación: un sector puede tener reclamos asociados y un director responsable.


![Diagrama de Reclamos](IMAGEN/captura.png)


TuReclamo es una app que busca agilizar un reclamo de ciudadano ante un municipio de Mendoza.
Integrantes:
Adriana Antunez
Iara Fernandez
Lara Magallanes
Carolina Lopez


# Flask API RESTful CRUD

Este es un proyecto que consiste en una aplicación CRUD usando Flask, SQLAlchemy y MySQL.

## Requisitos

- Python 3
- MySQL

## Configuración del entorno

### 1. Crear un entorno virtual

#### En Linux / macOS:
```sh
python3 -m venv <nombre_del_entorno>
```

#### En Windows:
```sh
python -m venv <nombre_del_entorno>
```

### 2. Activar el entorno virtual

#### En Linux / macOS:
```sh
source <nombre_del_entorno>/bin/activate
```

#### En Windows:
```sh
<nombre_del_entorno>\Scripts\activate
```

### 3. Instalar dependencias

```sh
pip install Flask Flask-SQLAlchemy PyMySQL python-dotenv
```

## Configuración de la base de datos

Antes de ejecutar la aplicación, debes configurar las siguientes variables de entorno:

```sh
MYSQL_USER=<tu_usuario>
MYSQL_PASSWORD=<tu_contraseña>
MYSQL_DATABASE=<nombre_de_la_base_de_datos>
MYSQL_HOST=<host_de_mysql>
```

## Instalación y ejecución

1. Clona el repositorio:
```sh
git clone <url_del_repositorio>
```

2. Accede al directorio del proyecto:
```sh
cd <nombre_del_proyecto>
```

3. Instala las dependencias desde el archivo `requirements.txt`:
```sh
pip install -r requirements.txt
```

4. Ejecuta la aplicación:
```sh
python app.py