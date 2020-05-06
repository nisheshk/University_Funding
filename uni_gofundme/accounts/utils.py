from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class GenerateToken(TokenObtainPairSerializer):
    # def get_tokens_for_user(user):
    #     refresh = RefreshToken.for_user(user)

    def return_token(self, user=None):
        refresh = self.get_token(user)
        data={}
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add extra responses here
        data['username'] = user.username
        data['user_id'] = user.id
        data['first_name'] = user.first_name
        data['last_name'] = user.last_name
        data['user_type'] = user.type
        #data['groups'] = user.groups.values_list('name', flat=True)
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = GenerateToken
