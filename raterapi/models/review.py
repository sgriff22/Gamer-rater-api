from django.db import models
from django.contrib.auth.models import User

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="games_reviewed")
    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name="game")
    review = models.TextField(max_length=255)