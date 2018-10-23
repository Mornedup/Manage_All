from django import forms
from finance_share_app.models import *

class DocUploadForm(forms.ModelForm):

    class Meta:
        model = Document
        fields = (
        'docref',
        'purchasedate',
        'notes',
        'file',
        )

class ClaimUploadForm(forms.ModelForm):

    class Meta:
        model=Claim
        fields = (
        'description',
        'amount',
        'notes',
        'docref',
        )
