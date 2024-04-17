from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from datetime import datetime
from documents.models import document
class work_type(models.Model):
    #type_name	initial
    type_name=models.CharField(max_length=255)
    initial=models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.type_name
#person_id	post	name
from django.contrib.auth import get_user_model
User=get_user_model()
class designer(models.Model):
    person_id=models.CharField( max_length=20)
    post=models.CharField( max_length=50)
    name=models.CharField( max_length=255)
    user_name=models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self) -> str:
        return self.name+"\n"+self.post
#mile_stone_name	initial	progress
class progress_mile_stone(models.Model):
    mile_stone_name=models.CharField(max_length=50)
    initial=models.CharField(max_length=10)
    progress=models.DecimalField(max_digits=5,decimal_places=4)
    
    def __str__(self) -> str:
        return str(round(self.progress*100,0))+"%:"+self.mile_stone_name
    
#inital	office_name	xen	phone_no	email_id
class filed_office(models.Model):
    inital=models.CharField(max_length=15)
    office_name=models.CharField(max_length=50)
    xen=models.CharField(max_length=40,blank=True,null=True)
    phone_no=PhoneNumberField(blank=True,null=True)
    email_id=models.EmailField(blank=True,null=True)
    
    def __str__(self) -> str:
        return self.office_name
    
 #division	designer	checker	reviewer	approver

class design_work(models.Model):
    work_name=models.CharField(max_length=350)
    project_name=models.ForeignKey('bwdb_project',related_name="project",on_delete=models.CASCADE,null=True)    
    division_name=models.ForeignKey('filed_office',related_name="division",on_delete=models.CASCADE,null=True)
    
    designer_name=models.ForeignKey('designer',related_name="designer_id",on_delete=models.CASCADE,null=True)
    checker_name=models.ForeignKey('designer',related_name="checker_id",on_delete=models.CASCADE,null=True)
    
    reviewer_name=models.ForeignKey('designer',related_name="reviewer_id",on_delete=models.CASCADE,null=True) 
    approver_name=models.ForeignKey('designer',related_name="approver_id",on_delete=models.CASCADE,null=True)   
    work_completion_status=models.ForeignKey('design_work_completion_status',related_name="completion_status",on_delete=models.CASCADE,null=True)
    def __str__(self) -> str:
        return self.work_name
    
    
class bwdb_project(models.Model):        
    project_name=models.CharField(max_length=255)
    short_name=models.CharField(max_length=25,null=True)
    
    def __str__(self) -> str:
        return self.short_name
    
    
from django.utils import timezone as tz
#Work_ID	Progress_Mile_Stone	Date
class design_work_progress(models.Model):
    #project_name=models.ForeignKey('bwdb_project',related_name="project",on_delete=models.CASCADE,null=True)
    work_name=models.ForeignKey('design_work',related_name="work",on_delete=models.CASCADE,null=True)
    work_status=models.ForeignKey('progress_mile_stone',related_name="status",on_delete=models.CASCADE,null=True)    
    update_date=models.DateField(default=tz.now)
    
    def __str__(self) -> str:
        return str(self.work_status)

class design_work_completion_status(models.Model):
    work_status=models.CharField(max_length=50)
    initial=models.CharField(max_length=10)
    
    def __str__(self) -> str:
        return str(self.initial)


class design_document(models.Model):
    design=models.ForeignKey('design_work',related_name="design_id",on_delete=models.CASCADE,null=True)
    document=models.ForeignKey(document,related_name="document_id",on_delete=models.CASCADE,null=True)
    
    
class design_data(models.Model):
    pass
    
    

    

    

# Create your models here.

