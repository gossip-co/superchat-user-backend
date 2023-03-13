from rest_framework.serializers import ModelSerializer

from .models import Shoutouts
from account.serializers import UserSerializer

class ShoutoutSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Shoutouts
        fields = ['id', 'user', 'message', 'is_read', 'is_published']