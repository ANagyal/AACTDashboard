from django.db import models
from django.contrib.auth.models import User

class DashboardUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, blank=True)
    trials = models.JSONField(default=list)

    def __str__(self):
        return self.user.username