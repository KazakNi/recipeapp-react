from djoser.serializers import UserCreateSerializer
from users.models import MyUser

class UserRegistrationSerialzer(UserCreateSerializer):
    class Meta:
        model = MyUser
        fields = ('email', 'username', 'first_name', 'last_name', 'password',)