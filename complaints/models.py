from django.db import models
from django.contrib.auth.models import User


class Complaint(models.Model):

    CATEGORY_CHOICES = [
        ('Electrical', 'Electrical'),
        ('Plumbing', 'Plumbing'),
        ('Cleaning', 'Cleaning'),
        ('WiFi', 'WiFi'),
        ('Furniture', 'Furniture'),
        ('Other', 'Other'),
    ]

    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]

    STATUS_CHOICES = [
        ('Submitted', 'Submitted'),
        ('Assigned', 'Assigned'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='complaints'
    )

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )

    location = models.CharField(
        max_length=200
    )

    description = models.TextField()

    image = models.ImageField(
        upload_to='complaints/',
        blank=True,
        null=True
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='Medium'
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='Submitted'
    )

    assigned_staff = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_complaints'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"CMP-{self.id} - {self.category}"