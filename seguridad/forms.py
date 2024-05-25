from django import forms
from .models import residents

class Residents(forms.ModelForm):
    
    class Meta:
        model = residents
        fields = "__all__"