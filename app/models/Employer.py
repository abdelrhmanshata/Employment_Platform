from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    company_description = models.TextField()
    logo = models.ImageField(upload_to='logos/', null=True, blank=True,default='company_logo.png')

    def __str__(self):
        return self.user.username
