# Variables
PYTHON=python
PIP=pip
MANAGE=$(PYTHON) manage.py

# Targets

.PHONY: run install migrate import_events server format superuser

# Instalar dependencias
install:
	$(PIP) install -r requirements.txt

# Aplicar migraciones
migrate:
	$(MANAGE) migrate

# Importar eventos desde el XML
import_events:
	$(MANAGE) import_events

# Levantar servidor
server:
	$(MANAGE) runserver

# Ejecutar todo lo necesario para correr la aplicación
run: install migrate import_events server

# Formatear el código con autopep8 según PEP8
format:
	autopep8 --in-place --recursive .

# Crear superusuario manualmente (opcional)
superuser:
	$(MANAGE) createsuperuser
