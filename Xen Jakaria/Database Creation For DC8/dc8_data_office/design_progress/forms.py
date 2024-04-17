from django import forms
from . models import design_work,design_work_progress
class design_work_form(forms.ModelForm):
    class Meta:
        model=design_work
        fields="__all__"
        #fields=("drawing_no","pdf_drw","dxf_drw")
from django.utils import timezone as tz
from .models import progress_mile_stone
class design_work_progress_form(forms.Form):
    design_work_name=forms.ModelChoiceField(design_work.objects.all(),widget=forms.Select(attrs={'readonly': 'readonly'}))
    current_progress=forms.ModelChoiceField(progress_mile_stone.objects.all(),widget=forms.Select(attrs={'readonly': 'readonly'}))
    updated_progress=forms.ModelChoiceField(progress_mile_stone.objects.all().order_by("progress"))    
    date=forms.DateField(initial=tz.now)

class design_data_add_form(forms.Form):    
    forawarding=forms.FileField()
    technical_report=forms.FileField()
    cross_section=forms.FileField()
    long_section=forms.FileField()
    bore_log=forms.FileField()
    
    
    pass

    
   
    

    