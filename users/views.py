from rest_framework import viewsets
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend


from users.models import User
from users.serializers import UserSerializer
from users.filters import UserFilter


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("created")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter

    # def create(self, request):     
    #     return
