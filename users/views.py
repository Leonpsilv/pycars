from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
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

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]

    def create(self, request):
        try:
            cpf = request.data["cpf"]

            if type(cpf) == str:  # filtering just numbers in cpf
                dirt_cpf = request.data["cpf"]
                numbers_of_cpf = [char for char in dirt_cpf if char.isdigit()]
                cpf = "".join(numbers_of_cpf)

            data = {
                "cpf": cpf,
                "name": request.data["name"],
                "email": request.data["email"],
                "password": request.data["password"],
            }

            serializer = UserSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        except Exception as e:
            return Response(
                {"detail": f"Failure to process user data: {e}"}, status=500
            )

    def update(self, request, pk=None):
        try:
            instance = self.get_object()
            old_user = self.get_serializer(instance).data
            user = self.request.user
            if user.id != old_user["id"]:
                return Response(
                    {"detail": f"id entered does not match your profile"}, status=400
                )

            if not "old_password" in request.data:
                return Response(
                    {"detail": f"your registered password must be informed"}, status=400
                )

            if not check_password(request.data["old_password"], old_user["password"]):
                return Response({"detail": f"password wrong"}, status=400)

            data = {
                "name": request.data["new_name"],
                "password": request.data["new_password"],
            }

            serializer = self.get_serializer(instance, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        except Exception as e:
            return Response({"detail": f"Failure to update user data: {e}"}, status=500)

    def destroy(self, request, pk=None):
        try:
            instance = self.get_object()
            old_user = self.get_serializer(instance).data
            user = self.request.user
            if (user.id != old_user["id"]) and (user.is_superuser != True):
                return Response(
                    {"detail": f"id entered does not match your profile"}, status=400
                )

            self.perform_destroy(instance)
            return Response(status=204)
        except Exception as e:
            return Response({"detail": f"Failure to delete user data: {e}"}, status=500)
