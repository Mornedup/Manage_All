from django.db import models
from django.utils import timezone
from django.conf import settings
from authapp.models import CUser
from claimsmanage.models import Claim

# Create your models here.
class UserClaimAllocate(models.Model):
    user=models.ForeignKey(CUser, related_name='users')
    claim=models.ForeignKey(Claim, related_name='claims')
    share_ammount=models.DecimalField(default=0, max_digits=8, decimal_places=2)
    created_date = models.DateTimeField(default=timezone.now)
