from django.db import models
from django.utils import timezone
from django.conf import settings

# Create your models here.
def file_path(instance, filename):
    return 'docs/{}'.format(filename)


class Doc(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    docref = models.CharField(max_length=200)
    purchasedate = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    file = models.FileField(upload_to='docs/', blank=True)

    def __str__(self):
        return '{}'.format(self.pk)
