from django import forms
from .models import Claim
from authapp.models import CUser

class ClaimUploadForm(forms.ModelForm):

    class Meta:
        model=Claim
        fields = (
        'description',
        'ammount',
        'notes',
        'docref',
        )
        
