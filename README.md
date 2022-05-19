# Clicoh API

## Índice ##

1. [Instalación](#1-instalación)
2. [Ejecutar](#2-ejecutar)
3. [Ejecutar Tests](#3-ejecutar-Tests)


### 1. Instalación ###

- **Crear el virtualenv:** `python3 -m venv myvirtual`
- **Activar el virtualvenv:** `source /path/to/virtualvenv/activate`
- **Clonar el Proyecto.**
- **Instalar las dependencias dev:** `pip install -r requirements.txt`
- **Migrate:** `python manage.py migrate`
- **Crear superuser:** `python manage.py createsuperuser`


### 2. Ejecutar ###

- **Ejecutar el servidor:** `python manage.py runserver`
- **Ir al navegador:** `http://localhost:8000`, `http://localhost:8000/admin`


### 3. Ejecutar Tests ###

- Ejecutar: `pytest`