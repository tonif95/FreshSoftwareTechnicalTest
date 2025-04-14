from datetime import datetime, timezone as dt_timezone

from django.utils import timezone
from events.models import Event

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Definición de parámetros Swagger
starts_at_param = openapi.Parameter(
    'starts_at',
    openapi.IN_QUERY,
    description='Fecha de inicio en formato ISO 8601 (YYYY-MM-DDTHH:MM:SS)',
    type=openapi.TYPE_STRING,
    required=True
)

ends_at_param = openapi.Parameter(
    'ends_at',
    openapi.IN_QUERY,
    description='Fecha de fin en formato ISO 8601 (YYYY-MM-DDTHH:MM:SS)',
    type=openapi.TYPE_STRING,
    required=True
)

# Vista de la API con documentación Swagger
@swagger_auto_schema(
    method='get',
    manual_parameters=[starts_at_param, ends_at_param],
    responses={
        200: openapi.Response(
            description="Lista de eventos en el rango de fechas",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'events': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'title': openapi.Schema(type=openapi.TYPE_STRING),
                                'start_date': openapi.Schema(type=openapi.TYPE_STRING, format='date-time'),
                                'end_date': openapi.Schema(type=openapi.TYPE_STRING, format='date-time'),
                                'price': openapi.Schema(type=openapi.TYPE_STRING),
                                'zone': openapi.Schema(type=openapi.TYPE_STRING),
                            }
                        )
                    )
                }
            )
        ),
        400: openapi.Response(
            description='Error por falta de parámetros',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        )
    }
)

@api_view(['GET'])
def get_events(request):
    starts_at = request.GET.get('starts_at')
    ends_at = request.GET.get('ends_at')

    if not starts_at or not ends_at:
        return Response({'error': 'Faltan parámetros "starts_at" o "ends_at"'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        starts_at_naive = datetime.fromisoformat(starts_at)
        ends_at_naive = datetime.fromisoformat(ends_at)
    except ValueError:
        return Response({'error': 'Formato de fecha inválido. Usa formato ISO 8601 (YYYY-MM-DDTHH:MM:SS)'}, status=status.HTTP_400_BAD_REQUEST)

    # Convertir a timezone-aware
    starts_at = timezone.make_aware(starts_at_naive, dt_timezone.utc)
    ends_at = timezone.make_aware(ends_at_naive, dt_timezone.utc)

    # Consultar eventos filtrados
    events = Event.objects.filter(
        event_start_date__gte=starts_at,
        event_end_date__lte=ends_at,
        sell_mode='online'
    )

    events_data = [
        {
            'title': event.title,
            'start_date': event.event_start_date.isoformat(),
            'end_date': event.event_end_date.isoformat(),
            'price': str(event.price),
            'zone': event.name,
        }
        for event in events
    ]

    return Response({'events': events_data}, status=status.HTTP_200_OK)


