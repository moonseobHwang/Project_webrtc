from django.db import models

# Create your models here.

class Board(models.Model):
    id = models.AutoField(primary_key=True)
    drone = models.CharField(max_length=50)
    path = models.CharField(max_length=100)
    filename = models.CharField(max_length=100)
    datetime = models.DateTimeField()
    ip = models.CharField(max_length=50)
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.filename
