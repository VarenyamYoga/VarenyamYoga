from django.db import models
from django.contrib.auth.models import User


class CorporateInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Name = models.CharField(max_length=15, blank=True)
    DOB = models.CharField(max_length=50, blank=True)
    BloodGroup = models.CharField(max_length=50, blank=True)
    Height = models.CharField(max_length=50, blank=True)
    Weight = models.CharField(max_length=50, blank=True)
    waist = models.CharField(max_length=50, blank=True)
    heap = models.CharField(max_length=50, blank=True)
    Diseases = models.CharField(max_length=50, blank=True)
    Company = models.CharField(max_length=50, blank=True)
    Designation = models.CharField(max_length=50, blank=True)
    picture = models.ImageField(upload_to = 'corporate_profile_pics', blank=True)


    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name_plural = 'Corporate Info'