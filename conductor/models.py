from django.db import models
from django.contrib.auth.models import User
from usuario.models import TipoDoc, Status


# Create your models here.
class Conductor(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="conductor_profile",
    )
    doc_type = models.ForeignKey(TipoDoc, on_delete=models.PROTECT)
    doc = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    cel = models.CharField(max_length=15)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)

    def delete(self, using=None, keep_parents=False):
        self.user.delete()
        super(Conductor, self).delete()

    def __str__(self):
        return self.user.first_name


class Vehiculo(models.Model):
    placa = models.CharField(max_length=10)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    color = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.placa} - {self.marca}"
