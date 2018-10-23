from django.db import models
from accounts_app.models import CUser

# Create your models here.
class UserApp(models.Model):
    user = models.ForeignKey(CUser, on_delete=models.CASCADE)
    #app =

    def __str__(self):
        return '{}'.format(self.user)