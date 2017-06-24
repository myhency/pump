from django.db import models

class Trade(models.Model):
    coin = models.CharField(max_length=200)

