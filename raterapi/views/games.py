from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from raterapi.models import Game, Category, GameCategory
from .categories import CategorySerializer


class GameSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)

    class Meta:
        model = Game
        fields = [
            "id",
            "user_id",
            "title",
            "designer",
            "year",
            "number_of_players",
            "play_time",
            "age",
            "categories",
            "average_rating",
        ]


class GameViewSet(viewsets.ViewSet):

    def list(self, request):
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True, context={"request": request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single item

        Returns:
            Response -- JSON serialized instance
        """
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game, context={"request": request})
            return Response(serializer.data)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        try:
            # Get the data from the client's JSON payload
            title = request.data.get("title")
            designer = request.data.get("designer")
            year = request.data.get("year")
            number_of_players = request.data.get("number_of_players")
            play_time = request.data.get("play_time")
            age = request.data.get("age")

            game = Game.objects.create(
                user=request.user,
                title=title,
                designer=designer,
                year=year,
                number_of_players=number_of_players,
                play_time=play_time,
                age=age,
            )

            # Get the category IDs from the request data
            category_ids = request.data.get("categories", [])

            # Create GameCategory instances and associate them with the game
            for category in category_ids:
                category = Category.objects.get(pk=category)
                GameCategory.objects.create(game=game, category=category)

            serializer = GameSerializer(game, context={"request": request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            game = Game.objects.get(pk=pk)

            # Update the fields based on the data from the request
            game.title = request.data.get("title")
            game.designer = request.data.get("designer")
            game.year = request.data.get("year")
            game.number_of_players = request.data.get("number_of_players")
            game.play_time = request.data.get("play_time")
            game.age = request.data.get("age")
            # Save the changes to the game instance
            game.save()

            # Get the category IDs from the request data
            category_ids = request.data.get("categories")
            # Check if the game has any existing GameCategory instances
            existing_game_categories = game.categories.exists()

            if existing_game_categories:
                # Clear the existing GameCategory instances
                game.categories.clear()

            # Create GameCategory instances and associate them with the game
            for category in category_ids:
                category = Category.objects.get(pk=category)
                GameCategory.objects.create(game=game, category=category)

            serializer = GameSerializer(game, context={"request": request})
            return Response(serializer.data)

        except Game.DoesNotExist:
            return Response(
                {"error": "Game does not exist."}, status=status.HTTP_404_NOT_FOUND
            )

        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
