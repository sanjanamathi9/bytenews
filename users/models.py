from django.db import models
from django.contrib.auth.models import User
from news.models import Category  # Assuming this is your category model

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_categories = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"