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

    @property
    def average_rating(self):
        """Average rating calculated attribute for each game"""
        ratings = self.ratings.all()

        # Sum all of the ratings for the game
        total_rating = 0
        try:
            for rating in ratings:
                total_rating += rating.rating

            # Calculate the average and return it.
            average = total_rating / len(ratings)
            # Round the average to one decimal point
            average = round(average, 1)

        except ZeroDivisionError:
            average = 0

        return average
