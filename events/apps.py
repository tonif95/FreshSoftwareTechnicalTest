from django.apps import AppConfig
import subprocess
import sys
import os


class EventsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'events'

    def ready(self):
        if 'runserver' in sys.argv and os.environ.get('RUN_MAIN') == 'true':
            print("Importando eventos al iniciar Django...")
            subprocess.run(['python', 'manage.py', 'import_events'])
