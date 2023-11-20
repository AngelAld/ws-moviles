from django.db import models


class Config(models.Model):
    """
    Configuration model
    """

    name = models.CharField(max_length=255, unique=True)
    valor = models.CharField(max_length=255)

    def __str__(self):
        return self.name
