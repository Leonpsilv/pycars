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
    queryset = AvatarModel.objects.all().order_by("created")
    serializer_class = AvatarSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["user_id"]

    def create(self, request):
        try:
            if not "file" in request.data:
                return Response({"file": ["a file must be informed."]}, status=400)

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

            data = {"user_id": user.id, "url": url_photo, "filename": filename}
            serializer = AvatarSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)

            path = f"users-avatar/{filename}.png"
            awsProvider.delete_file(path)
            return Response(serializer.errors, status=400)
        except Exception as e:
            return Response({"detail" :f"Failure to process avatar data: {e}"} , status=500)

    def update(self, request, pk=None):
        try:
            instance = self.get_object()
            old_file = self.get_serializer(instance).data
            old_file_path = f"users-avatar/{old_file['filename']}.png"
            user = self.request.user
            if user.id != old_file['user_id']:
                return Response({"detail" :f"this avatar does not belong to the logged user"}, status=400)

            data = {}
            if "file" in request.data:
                file = request.data["file"]
                data["filename"] = f"{user.id}-{datetime.now().strftime('%H%M%S')}"
                new_file_path = (
                    f'./files/avatar-{datetime.now().strftime("%H%M%S-%F")}.png'
                )

                with open(new_file_path, "wb+") as archive:
                    archive.write(file.file.read())

                new_file_url = awsProvider.upload_file_s3(
                    f"users-avatar/{data['filename']}.png", new_file_path
                )
                data["url"] = new_file_url
                os.remove(new_file_path)
                awsProvider.delete_file(old_file_path)

            serializer = self.get_serializer(instance, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        except Exception as e:
            return Response({"detail" :f"Failure to update avatar data: {e}"} , status=500)
        
    def destroy(self, request, pk=None):
        try:
            instance = self.get_object()
            old_file = self.get_serializer(instance).data
            old_file_path = f"users-avatar/{old_file['filename']}.png"
            user = self.request.user
            if user.id != old_file['user_id']:
                return Response({"detail" :f"this avatar does not belong to the logged user"}, status=400)

            awsProvider.delete_file(old_file_path)

            self.perform_destroy(instance)
            return Response(status=204)
        except Exception as e:
            return Response({"detail" :f"Failure to update avatar data: {e}"} , status=500)
