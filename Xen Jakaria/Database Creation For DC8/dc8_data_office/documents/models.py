from django.db import models

# Create your models here.
class document_type(models.Model):
    #type_name	initial
    type_name=models.CharField(max_length=100)
    description=models.CharField(max_length=400)
    initial=models.CharField(max_length=20)
    
    def __str__(self):
        return self.type_name

class document(models.Model):
    pdf_doc=models.FileField(upload_to="documents/pdf")
    doc_description=models.CharField(max_length=255,null=True,blank=True)
    doc_type=models.ForeignKey('document_type',related_name="doc_class", on_delete=models.CASCADE)
    
    def __str__(self):
        return self.doc_description
