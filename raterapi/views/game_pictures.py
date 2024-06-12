from rest_framework import viewsets, status
from rest_framework import serializers
from rest_framework.response import Response
from raterapi.models import GamePicture
import uuid
import base64
from django.core.files.base import ContentFile


class GamePictureSerializer(serializers.ModelSerializer):
    """JSON serializer"""

    class Meta:
        model = GamePicture
        fields = ["id", "game", "action_pic"]


class GamePictureViewSet(viewsets.ViewSet):

    def create(self, request):

        new_pic = GamePicture()

        try:
            # Get the data from the client's JSON payload
            new_pic.game_id = request.data.get("game_id")

            # Format image
            image_data = request.data.get("action_pic")
            format, imgstr = image_data.split(";base64,")
            ext = format.split("/")[-1]
            image_data = ContentFile(
                base64.b64decode(imgstr), name=f"user_image-{uuid.uuid4()}.{ext}"
            )
            new_pic.action_pic = image_data

            new_pic.save()

            serializer = GamePictureSerializer(new_pic)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        # Get game from request query parameters
        gameId = request.query_params.get("gameId")

        # Check if gameId is provided
        if gameId is not None:
            # Filter game pictures by gameId
            game_pics = GamePicture.objects.filter(game_id=gameId)
        else:
            # If gameId is not provided, return all pictures
            game_pics = GamePicture.objects.all()

        serializer = GamePictureSerializer(
            game_pics, many=True, context={"request": request}
        )
        return Response(serializer.data)
