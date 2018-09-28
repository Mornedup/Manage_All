from django.db import models
from django.utils import timezone
from django.conf import settings
from . import logic

# Create your models here.
class Allocation(models.Model):
    identifier = models.AutoField(primary_key=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.CharField(max_length=200, blank=True, null=True)
    total_ammount = models.DecimalField(decimal_places=2, max_digits=10)
    created_date = models.DateTimeField(default=timezone.now)
    start_date = models.DateTimeField(default=GetDefaultStartDate)
    end_date = models.DateTimeField(default=timezone.now.replace(day=25))
    claim_list = models.CharField(max_length=999)

    def __str__(self):
        return self.title
