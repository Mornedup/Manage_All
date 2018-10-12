from django.db import models
from django.utils import timezone
from django.conf import settings
from docmanage.models import Doc
from authapp.models import CUser

# Create your models here.
class Claim(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    ammount = models.DecimalField(decimal_places=2, max_digits=10)
    notes = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    docref = models.ForeignKey(Doc, on_delete=models.CASCADE)
    alocated = models.BooleanField(default=False)

    def __str__(self):
        return self.pk
