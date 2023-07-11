from rest_framework import viewsets
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend

from avatars.models import AvatarModel
from avatars.serializers import AvatarSerializer


class AvatarViewSet(viewsets.ModelViewSet):
    queryset = AvatarModel.objects.all()
    serializer_class = AvatarSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["user_id"]

    # def create(self, request):
    #     try:
    #         # upload avatar to aws s3     
    #     except:
    #         return 
