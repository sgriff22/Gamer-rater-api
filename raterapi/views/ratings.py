from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from raterapi.models import Rating


class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = ["id", "game_id", "user_id", "rating"]


class RatingViewSet(viewsets.ViewSet):

    def create(self, request):
        try:
            # Get the data from the client's JSON payload
            game = request.data.get("game_id")
            rating = request.data.get("rating")

            rating = Rating.objects.create(
                user=request.user,
                game_id=game,
                rating=rating,
            )

            serializer = RatingSerializer(rating, context={"request": request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
