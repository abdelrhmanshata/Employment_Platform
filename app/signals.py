from django.db.models.signals import post_save
from django.dispatch import receiver
from app.models import Job
from app.utils import mail


@receiver(post_save, sender=Job)
def notify_employees_on_job_creation(sender, instance, created, **kwargs):
    if created:
        mail.notify_matching_employees(instance)
