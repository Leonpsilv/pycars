from rest_framework import serializers
from cars.models import CarModel


class CarSerializer(serializers.ModelSerializer):
    car = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = CarModel
        fields = "__all__"