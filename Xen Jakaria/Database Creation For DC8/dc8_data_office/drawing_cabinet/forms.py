from django import forms
from . models import design
class design_form(forms.ModelForm):
    class Meta:
        model=design
        fields=("drawing_no","pdf_drw","dxf_drw")