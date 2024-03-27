from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from raterapi.models import Game
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
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
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

        # Establish the many-to-many relationships
        category_ids = request.data.get("categories", [])
        game.categories.set(category_ids)

        serializer = GameSerializer(game, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
