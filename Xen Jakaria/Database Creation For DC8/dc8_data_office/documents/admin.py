from django.contrib import admin

# Register your models here.
from .models import document_type,document
admin.site.register(document_type)
admin.site.register(document)