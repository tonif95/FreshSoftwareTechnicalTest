from django.db import models

# models.py
class Event(models.Model):
    base_event_id = models.IntegerField()
    title = models.CharField(max_length=200)
    event_start_date = models.DateTimeField()
    event_end_date = models.DateTimeField()
    sell_from = models.DateTimeField()
    sell_to = models.DateTimeField()
    sold_out = models.BooleanField()
    zone_id = models.IntegerField()
    capacity = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    name = models.CharField(max_length=100)
    numbered = models.BooleanField()
    sell_mode = models.CharField(max_length=50, default='online')  # <-- NUEVO
    event_id = models.CharField(max_length=100)


    def __str__(self):
        return f"{self.title} ({self.event_start_date})"