from django.contrib.auth        import authenticate
from rest_framework.views       import APIView
from rest_framework.response    import Response
from django.db.models           import Q
from .utils                     import GenerateToken
from .models                    import User
from rest_framework             import serializers
from uni_gofundme.api_conf      import exp_time_mins
import logging
import traceback

logger = logging.getLogger(__name__)


class LoginView(APIView, GenerateToken):
    authentication_classes  = []
    permission_classes      = []

    def set_cookie_values(self, request, data):

        """
            This method sets the cookie values for the new logged in user

            Parameters:
            -----------
            data: dic
                It contains the user data along with refresh/access token.

            Returns
            --------
            Nothing.
        """

        #Session expiry time = Access token expiry time.
        #Changes: Haven't used refresh token; In future needs to be used.
        request.session.set_expiry(exp_time_mins*60)
        request.session['user_id'] = data['user_id']
        request.session['username'] = data['username']
        request.session['user_type'] = data['user_type']
        request.session['access_token'] = data['access']


    def post(self, request, format=None):

        """
            This is a post method for login authentication

            Parameters:
            -----------
            request:
                Rest Framework request unlike normal Django HttpRequest
                request is inherited from HttpRequest, but with exra features.

            Returns
            --------
            Response(token).
                Response(data, status=None, template_name=None, headers=None,
                        content_type=None)
                data = The serialized data for the response.
                token here contains the username, firstname, lastname and
                token.
        """

        try:

            #Check is user is already authenticated
            #Changes: This logic is not working
            if request.user.is_authenticated:
                return Response({'Error':'User is already authenticated'}, status=403)

            username = request.data['username']
            password = request.data['password']

            user_obj = User.objects.all()
            user_obj = user_obj.filter(Q(username__exact = username)
                                        ).distinct()

            #CHeck if username exists in the database
            if len(user_obj) == 1:

                #Validate the password
                user = authenticate(username=user_obj[0].username, password=password)
                if user is None:
                    return Response({'Error':'Incorrect Password'}, status=401)

                #If valid user, set tokens for the user
                token = self.return_token(user)
                self.set_cookie_values(request, token)
                response = Response(token, status=200)
                return response

            return Response({'Error':'Incorrect email address'}, status=401)

        except:
            logger.error("Error: %s", traceback.format_exc())
            return Response({"Error": "Check the logs"})

class LogoutView(APIView):
    # authentication_classes  = []
    # permission_classes      = []

    def get(self, request, format=None):

        """
            This is a get method for logging out the user

            Parameters:
            -----------
            request

            Returns
            --------
            Response.
        """

        try:
            #Clear the session from the database
            if request.user.is_authenticated:
                if request.session.has_key('user_id'):
                    request.session.flush()
                return Response({"Success":"Logged out"}, status = 200)
            else:
                return Response({"Error":"User should be logged in order to "
                                    "log out."}, status = 403)
        except:
            logger.error("Error: %s", traceback.format_exc())
            return Response({"Error": "Check the logs"})
