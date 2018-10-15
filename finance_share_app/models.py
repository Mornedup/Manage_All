from django.db import models
from django.utils import timezone
from auth_app.models import CUser


# Create your models here.
def file_path(filename):
    return 'documents/{}'.format(filename)


class Document(models.Model):
    owner = models.ForeignKey(CUser, on_delete=models.CASCADE, )
    docref = models.CharField(max_length=200)
    purchasedate = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    file = models.FileField(upload_to='docs/', blank=True)

    def __str__(self):
        return '{}'.format(self.pk)


class Claim(models.Model):
    description = models.CharField(max_length=200)
    ammount = models.DecimalField(decimal_places=2, max_digits=10)
    notes = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    docref = models.ForeignKey(Document, on_delete=models.CASCADE)

    def __str__(self):
        return self.pk


class UserClaimAllocate(models.Model):
    user = models.ForeignKey(CUser, related_name='users', on_delete=models.CASCADE)
    claim = models.ForeignKey(Claim, related_name='claims', on_delete=models.CASCADE)
    share_ammount = models.DecimalField(default=0, max_digits=8, decimal_places=2)

    def __str__(self):
        return self.pk
