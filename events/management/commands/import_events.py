import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand
from events.models import Event
from datetime import datetime
from django.utils import timezone
from datetime import timezone as dt_timezone


class Command(BaseCommand):
    help = 'Importa los eventos desde un archivo XML'

    def handle(self, *args, **kwargs):
        xml_file = 'eventos.xml'

        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()

            imported_count = 0
            updated_count = 0

            for base_event in root.findall('.//base_event'):
                sell_mode = base_event.get('sell_mode')
                if sell_mode != 'online':
                    continue  # Ignoramos los que no sean online

                title = base_event.get('title')
                base_event_id = base_event.get('base_event_id')

                for event in base_event.findall('event'):
                    event_start_date = timezone.make_aware(datetime.fromisoformat(
                        event.get('event_start_date')), dt_timezone.utc)
                    event_end_date = timezone.make_aware(datetime.fromisoformat(
                        event.get('event_end_date')), dt_timezone.utc)
                    sell_from = timezone.make_aware(datetime.fromisoformat(
                        event.get('sell_from')), dt_timezone.utc)
                    sell_to = timezone.make_aware(datetime.fromisoformat(
                        event.get('sell_to')), dt_timezone.utc)
                    sold_out = event.get('sold_out') == 'false'
                    event_id = event.get('event_id')

                    for zone in event.findall('zone'):
                        zone_id = zone.get('zone_id')

                        # Buscamos por base_event_id, event_id y zone_id
                        obj, created = Event.objects.update_or_create(
                            base_event_id=base_event_id,
                            event_id=event_id,
                            zone_id=zone_id,
                            defaults={
                                'title': title,
                                'event_start_date': event_start_date,
                                'event_end_date': event_end_date,
                                'sell_from': sell_from,
                                'sell_to': sell_to,
                                'sold_out': sold_out,
                                'capacity': zone.get('capacity'),
                                'price': zone.get('price'),
                                'name': zone.get('name'),
                                'numbered': zone.get('numbered') == 'true',
                                'sell_mode': sell_mode
                            }
                        )

                        if created:
                            imported_count += 1
                        else:
                            updated_count += 1

            self.stdout.write(self.style.SUCCESS(
                f'Importación finalizada: {imported_count} nuevos, {updated_count} actualizados.'
            ))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(
                f'Error: El archivo "{xml_file}" no fue encontrado en la misma carpeta.'))
        except ET.ParseError as e:
            self.stdout.write(self.style.ERROR(
                f'Error al parsear el archivo XML: {e}'))
        except ValueError as e:
            self.stdout.write(self.style.ERROR(
                f'Error de formato en el archivo XML: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f'Ocurrió un error inesperado: {e}'))
