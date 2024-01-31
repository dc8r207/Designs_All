from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Role(models.Model):
    role_name=models.CharField(max_length=20)
    def __str__(self):
        return self.role_name
class Profile(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    cellNo=PhoneNumberField(null=True,blank=True)
    role=models.ForeignKey(Role,on_delete=models.CASCADE,default=12)
    def __str__(self):
        return self.user.last_name +'_'+ self.role.role_name

# Create your models here.
