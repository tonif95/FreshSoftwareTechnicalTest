# Fresh Software Code Challenge

Este proyecto ha sido desarrollado como parte de la prueba técnica para Fresh Software. La finalidad es crear un microservicio que integre eventos de un proveedor externo y los exponga mediante un endpoint con filtros de fechas y modo de venta.

## 📌 Tecnologías utilizadas

- Python 3.x
- Django
- Django REST Framework
- SQLite
- drf-yasg (Swagger)
- autopep8

## 📚 Descripción

El microservicio expone un único endpoint `/api/events/` que permite obtener los eventos disponibles en un rango de fechas dado, aplicando los siguientes filtros:

- **Solo eventos cuyo `sell_mode` sea `online`**
- **Solo eventos cuya fecha esté dentro del rango proporcionado en los parámetros `starts_at` y `ends_at`**

Dado que la API de ejemplo no funciona, se ha adaptado el sistema para obtener los eventos desde un archivo XML local con el mismo formato que tendría la API. Este archivo se importa automáticamente a la base de datos SQLite cada vez que se ejecuta el servidor, actualizando o insertando eventos según su `id` único.

## 📖 Endpoints

- `GET /api/events/`: Devuelve los eventos que cumplen con los filtros indicados.
- `GET /documentation/`: Documentación interactiva Swagger/OpenAPI del endpoint.

## 🛠️ Instalación y ejecución

1. Clonar el repositorio.
2. Crear un entorno virtual y activarlo.
3. Instalar las dependencias:  
   `pip install -r requirements.txt`
4. Inicializar el servidor con el comando "python manage.py runserver"
5. Realizar una solicitud GET que contenga los parametros `starts_at` y `ends_at`. Ejemplo: `http://127.0.0.1:8000/api/events/?starts_at=2025-02-01T00:00:00&ends_at=2026-08-01T00:00:00`
