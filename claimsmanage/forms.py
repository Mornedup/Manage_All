from django import forms
from .models import Claim

class ClaimUploadForm(forms.ModelForm):
    class Meta:
        model=Claim
        fields = (
        'description',
        'ammount',
        'notes',
        'docref',
        )

"""    def save(self, commit=True):
        claim = super(ClaimUploadForm, self).save(commit=False)
        claim.owner = self.cleaned_data['owner']
        claim.ammount = self.cleaned_data['ammount']
        claim.notes = self.cleaned_data['notes']


        if commit:
            claim.save()

        return claim"""

#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        self.fields['docref'].queryset = """Query for list of docs uploaded by user"""
