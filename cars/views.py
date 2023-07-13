from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend


from cars.models import CarModel
from cars.serializers import CarSerializer
from cars.filters import CarFilter


class CarViewSet(viewsets.ModelViewSet):
    queryset = CarModel.objects.all().order_by("created")
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CarFilter

    def create(self, request):
        try:
            user = self.request.user
            data = {
                "name" : request.data["name"],
                "color" : request.data["color"],
                "brand" : request.data["brand"],
                "year" : request.data["year"],
                "type" : request.data["type"],
                "km" : request.data["km"],
                "price" : request.data["price"],
                "new" : request.data["new"],
                "vin" : request.data["vin"],
                "user_id": user.id
            }

            serializer = CarSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        except Exception as e:
            return Response(
                {"detail": f"Failure to process car data: {e}"}, status=500
            )

    def update(self, request, pk=None):
        try:
            instance = self.get_object()
            old_car = self.get_serializer(instance).data
            user = self.request.user
            if user.id != old_car['user_id']:
                return Response({"detail" :f"this car does not belong to the logged user"}, status=400)

            data = {
                "color" : request.data["color"],
                "km" : request.data["km"],
                "price" : request.data["price"],
                "new" : request.data["new"],
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
            old_car = self.get_serializer(instance).data
            user = self.request.user
            if user.id != old_car['user_id']:
                return Response({"detail" :f"this car does not belong to the logged user"}, status=400)

            self.perform_destroy(instance)
            return Response(status=204)
        except Exception as e:
            return Response({"detail": f"Failure to delete user data: {e}"}, status=500)
