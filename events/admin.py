from django.contrib import admin
from .models import Event  # Importamos el modelo Event que hemos creado

# Registramos el modelo Event con el sitio de administración
admin.site.register(Event)
