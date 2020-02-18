from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer
from rest_framework.generics import CreateAPIView

class RegisterAPIView(CreateAPIView):
    permission_classes      = []
    authentication_classes  = []
    #queryset                = User.objects.all()
    serializer_class         = RegisterSerializer
