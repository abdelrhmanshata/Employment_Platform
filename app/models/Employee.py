from django.db import models
from django.contrib.auth import get_user_model
from app.models.City import City
from app.models.ProgrammingLanguage import ProgrammingLanguage

User = get_user_model()


class Employee(models.Model):
    Experience_CHOICES = (("Junior", "Junior"), ("Mid", "Mid"), ("Senior", "Senior"))
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    national_id = models.CharField(max_length=14, unique=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    biography = models.TextField()
    experience_level = models.CharField(max_length=10, choices=Experience_CHOICES)
    programming_languages = models.ManyToManyField(ProgrammingLanguage)

    def __str__(self):
        return self.user.username
