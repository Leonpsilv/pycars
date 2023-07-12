from datetime import datetime
import os

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from avatars.models import AvatarModel
from avatars.provider import AWSProvider
from avatars.serializers import AvatarSerializer

awsProvider = AWSProvider()

class AvatarViewSet(viewsets.ModelViewSet):
    queryset = AvatarModel.objects.all()
    serializer_class = AvatarSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["user_id"]

    def create(self, request):
        try:
            if not "file" in request.data:
                return Response({"file": ["a file must be informed."]}, status=400)

            # if not "user_id" in request.data:
            #     return Response({"user": ["a user must be informed"]}, status=400)

            file = request.data["file"]
            user = self.request.user
            filename = f"{user.id}-{datetime.now().strftime('%H%M%S')}"

            photo_path = f'./files/avatar-{datetime.now().strftime("%H%M%S-%F")}.png'
            with open(photo_path, "wb+") as archive:
                archive.write(file.file.read())

            url_photo = awsProvider.upload_file_s3(
                f"users-avatar/{filename}.png", photo_path
            )
            os.remove(photo_path)

            data = {
                "user_id": user.id,
                "file": file,
                "url": url_photo,
                "filename": filename
            }
            serializer = AvatarSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            
            path = f"users-avatar/{filename}.png"
            awsProvider.delete_file(path)
            return Response(serializer.errors, status=400)
        except Exception as e:
            return Response(f"Failure to process avatar data: {e}", status=500)
