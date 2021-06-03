from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class ClientPreferenceModel(models.Model): 
    user = models.OneToOneField(to = User,on_delete=models.CASCADE)
    sendEmailOnLogin = models.BooleanField(default=True)

    def __str__(self):
        return str(self.user) + 's' + 'preferences' 