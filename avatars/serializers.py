from rest_framework import serializers
from avatars.models import AvatarModel


class AvatarSerializer(serializers.ModelSerializer):
    avatar = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = AvatarModel
        fields = "__all__"
