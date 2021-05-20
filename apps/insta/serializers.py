# rest framework
from rest_framework import serializers

from apps.insta.models import InstaStalkUsers


class InstaStalkUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstaStalkUsers
        fields = ["insta_username"]