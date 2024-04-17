from django import forms
from . models import document
class document_form(forms.ModelForm):
    class Meta:
        model=document
        fields='__all__'