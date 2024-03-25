from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="games_created"
    )
    title = models.CharField(max_length=255)
    designer = models.CharField(max_length=255)
    year = models.IntegerField()
    number_of_players = models.IntegerField()
    play_time = models.IntegerField()
    age = models.CharField(max_length=255)
    categories = models.ManyToManyField(
        "Category", through="GameCategory", related_name="games"
    )
