from django.db import models
class design(models.Model):
    drawing_no=models.CharField(max_length=255)
    pdf_drw=models.FileField(upload_to="design/pdf")
    dxf_drw=models.FileField(upload_to="design/dxf")
    
# Create your models here.
