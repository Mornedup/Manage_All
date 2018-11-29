from django.db import models
from django.utils import timezone
from accounts_app.models import CUser


# Create your models here.
def file_path(filename):
    return 'documents/{}'.format(filename)


class Document(models.Model):
    owner = models.ForeignKey(CUser, on_delete=models.CASCADE)
    docref = models.CharField(max_length=200)
    purchasedate = models.DateTimeField()
    notes = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    file = models.FileField(upload_to='docs/')

    REQUIRED_FIELDS = ['file', 'purchasedate', 'docref']

    def __str__(self):
        return '{}'.format(self.pk)

    @property
    def convert_to_date(self):
        return self.created_date.date()


class Claim(models.Model):
    description = models.CharField(max_length=200)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    notes = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    docref = models.ForeignKey(Document, on_delete=models.CASCADE)

    REQUIRED_FIELDS = ['description', 'amount']

    def __str__(self):
        return '{}'.format(self.pk)


class UserClaimAllocate(models.Model):
    user = models.ForeignKey(CUser, related_name='users', on_delete=models.CASCADE)
    claim = models.ForeignKey(Claim, related_name='claims', on_delete=models.CASCADE)
    share_amount = models.DecimalField(default=0, max_digits=8, decimal_places=2)

    def __str__(self):
        return '{}'.format(self.pk)
