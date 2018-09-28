from django import forms
from .models import Doc

class DocUploadForm(forms.ModelForm):

    class Meta:
        model = Doc
        fields = (
        'notes',
        'file',
        )
