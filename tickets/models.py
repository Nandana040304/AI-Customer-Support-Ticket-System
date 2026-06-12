from django.db import models
from django.contrib.auth.models import User

class Ticket(models.Model):

    STATUS_CHOICES = [
        ('OPEN', 'OPEN'),
        ('IN_PROGRESS', 'IN_PROGRESS'),
        ('RESOLVED', 'RESOLVED'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=200)

    description = models.TextField()

    category = models.CharField(
        max_length=100,
        blank=True
    )

    ai_response = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='OPEN'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title