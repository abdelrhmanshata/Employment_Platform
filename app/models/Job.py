from django.db import models
from app.models.Employer import Employer
from app.models.City import City
from app.models.ProgrammingLanguage import ProgrammingLanguage


class Job(models.Model):
    Experience_CHOICES = (("Junior", "Junior"), ("Mid", "Mid"), ("Senior", "Senior"))
    Job_Types = (("Full-Time", "Full-Time"), ("Part-Time", "Part-Time"), ("Temporary", "Temporary"))
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    experience_level = models.CharField(max_length=10, choices=Experience_CHOICES ,default="Junior")
    programming_languages = models.ManyToManyField(ProgrammingLanguage)
    job_types = models.CharField(max_length=10, choices=Job_Types,default="Full-Time")
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

