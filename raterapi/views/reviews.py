from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from raterapi.models import Review
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name"]


class ReviewSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = Review
        fields = ["id", "game_id", "user_id", "review", "user"]


class ReviewViewSet(viewsets.ViewSet):

    def list(self, request):
        # Get gameId from request query parameters
        gameId = request.query_params.get("gameId")

        # Check if gameId is provided
        if gameId is not None:
            # Filter reviews by gameId
            reviews = Review.objects.filter(game_id=gameId)
        else:
            # If gameId is not provided, return all reviews
            reviews = Review.objects.all()

        serializer = ReviewSerializer(reviews, many=True, context={"request": request})
        return Response(serializer.data)

    def create(self, request):
        try:
            # Get the data from the client's JSON payload
            game = request.data.get("game_id")
            review = request.data.get("review")

            review = Review.objects.create(
                user=request.user,
                game_id=game,
                review=review,
            )

            serializer = ReviewSerializer(review, context={"request": request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
