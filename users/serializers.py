from rest_framework.serializers import ModelSerializer

from users.models import Payment, User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'last_login']


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"

