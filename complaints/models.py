from django.db import models
from django.contrib.auth.models import User

# Create your models here.

STATUS_CHOICES = [
    ('open', 'Open'),
    ('in_progress', 'In Progress'),
    ('resolved', 'Resolved'),
]

class Agency(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Agencies"

class Complaint(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    ]

    citizen_name = models.CharField(max_length=100)
    citizen_email = models.EmailField()
    category = models.CharField(max_length=100)
    description = models.TextField()
    agency = models.ForeignKey('Agency', on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    response = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.category} - {self.citizen_name}"

