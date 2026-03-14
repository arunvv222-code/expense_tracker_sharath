from django.db import models
from django.contrib.auth.models import User

class Expense(models.Model):

    title = models.CharField(max_length=200)

    amount = models.PositiveIntegerField()

    category = models.CharField(max_length=200)

    description = models.TextField()

    date = models.DateTimeField(auto_now_add=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expenses")

    

