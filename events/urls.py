from django.urls import path
from . import views

urlpatterns = [
    path('events/', views.get_events, name='get_events'), #Ruta del endpoint que usaremos para que nos devuelva los eventos 
]
