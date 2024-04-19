from rest_framework import viewsets, status
from rest_framework import serializers
from rest_framework.response import Response
from raterapi.models import GameCategory


class GameCategorySerializer(serializers.ModelSerializer):
    """JSON serializer"""

    class Meta:
        model = GameCategory
        fields = ["id", "game", "category"]


class GameCategoryViewSet(viewsets.ViewSet):

    def list(self, request):
        # Get game from request query parameters
        gameId = request.query_params.get("gameId")

        # Check if gameId is provided
        if gameId is not None:
            # Filter reviews by gameId
            gameCats = GameCategory.objects.filter(game_id=gameId)
        else:
            # If gameId is not provided, return all reviews
            gameCats = GameCategory.objects.all()

        serializer = GameCategorySerializer(
            gameCats, many=True, context={"request": request}
        )
        return Response(serializer.data)
