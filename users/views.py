from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.hashers import check_password


from users.models import User
from users.serializers import UserSerializer
from users.filters import UserFilter


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("created")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter

    def update(self, request, pk=None):
        try:
            instance = self.get_object()
            old_user = self.get_serializer(instance).data
            user = self.request.user
            if user.id != old_user["id"]:
                return Response({"detail" :f"id entered does not match your profile"}, status=400)

            if not "old_password" in request.data:
                 return Response({"detail" :f"your registered password must be informed"}, status=400)

            if not check_password(request.data["old_password"], old_user["password"]):
                return Response({"detail" :f"password wrong"}, status=400)

            data = {
                "name" : request.data["new_name"],
                "password" : request.data["new_password"]
            }

            serializer = self.get_serializer(instance, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        except Exception as e:
            return Response({"detail" :f"Failure to update user data: {e}"} , status=500)

    def destroy(self, request, pk=None):
        try:
            instance = self.get_object()
            old_user = self.get_serializer(instance).data
            user = self.request.user
            if (user.id != old_user["id"]) and (user.is_superuser != True):
                return Response({"detail" :f"id entered does not match your profile"}, status=400)

            self.perform_destroy(instance)
            return Response(status=204)
        except Exception as e:
            return Response({"detail" :f"Failure to delete user data: {e}"} , status=500)
