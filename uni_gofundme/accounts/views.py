from django.contrib.auth        import authenticate
from rest_framework.views       import APIView
from rest_framework.response    import Response
from django.db.models           import Q
from .utils                     import GenerateToken
from .models                    import User
from rest_framework             import serializers

class LoginView(APIView, GenerateToken):
    authentication_classes  = []
    permission_classes      = []

    def post(self, request, format=None):
        print (request.data)
        if request.user.is_authenticated:
            return Response({'Error':'User is already authenticated'}, status=200)
            #return serializers.ValidationError('User is already authenticated')
        username = request.data['username']
        password = request.data['password']
        print (request.data)
        user_obj = User.objects.all()
        user_obj = user_obj.filter(Q(username__exact = username)
                                    ).distinct()
        if len(user_obj) == 1:
            user = authenticate(username=user_obj[0].username, password=password)
            print (user)
            if user is None:
                return Response({'Error':'Incorrect Password'}, status=401)
            #self.get_tokens_for_user()
            token = self.return_token(user)
            print (token)
            return Response(token)
        return Response({'Error':'Incorrect email address'}, status=401)
