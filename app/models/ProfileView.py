from django.db import models
from app.models.Employer import Employer
from app.models.Employee import Employee


class ProfileView(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    viewing_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employer.user.username} - {self.employee.user.username}"
