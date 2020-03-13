from rest_framework.generics    import ListAPIView
from campaign.models            import CampaignModel
from accounts.models            import User
from campaign.api.serializers   import ( CampaignModelSerializer,
                                        CampaignModelGetSerializer)
from rest_framework.views       import APIView
from rest_framework             import serializers
from rest_framework.response    import Response
from .custom_permissions        import *
from rest_framework             import  authentication, permissions
import logging
import traceback
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers     import MultiPartParser, FormParser, JSONParser


logger = logging.getLogger(__name__)

class RetrieveActiveCampaigns(APIView):
        authentication_classes = []
        permission_classes = []
        active_status = 1

        def post(self, request, format=None):
            """
                This post method retrieves just the active campaigns; the status
                id for which is 1.

                Parameters:
                -----------
                request: Django Rest Fraework Request

                Returns
                --------
                serializer.data : Response
                    serializer.data contains the serialized data which is the
                    part of API output
            """
            try:
                obj = CampaignModel.objects.all()
                obj = obj.filter(status_id=self.active_status)
                serializer= CampaignModelGetSerializer(obj, many= True, context=\
                                                        {"request":self.request})

                return Response(serializer.data)

            except:
                logger.error("Error: %s", traceback.format_exc())
                return Response({"Error": "Check the logs"})


class RetrieveOnWaitingCampaigns(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        """
            This post method retrieves the campaigns that are not yet approved
            by the MGO; the status id for which is 0.

            Parameters:
            -----------
            request: Django Rest Fraework Request

            Returns
            --------
            serializer.data : Response
                serializer.data contains the serialized data which is the
                part of API output
        """
        try:
            status_id = 0
            obj = CampaignModel.objects.all()

            #Fetching the values from the session variables.
            user_type = request.session.get("user_type", None)
            user_id = request.session.get("user_id", None)
            print (user_type)
            if user_id:

                #If user type is fundraiser, only that particular user's
                #unapproved campaign should be returned back.
                if user_type == "f":
                    obj = obj.filter(status_id=status_id, created_by_id=user_id)

                #If user type is mgo, all unapproved campaign should be returned
                elif user_type == "m":
                    obj = obj.filter(status_id=status_id)
                else:
                    return Response({"Error": "Permission Denied"}, status=400)

                serializer= CampaignModelGetSerializer(obj, many= True, context=\
                                                    {"request":self.request})
                return Response(serializer.data)

        except:
            logger.error("Error: %s", traceback.format_exc())
            return Response({"Error": "Check the logs"})



class CampaignRetrieveApiView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        try:
            query = request.data
            obj = CampaignModel.objects.all()
            if query:
                obj = obj.filter(**query)
            serializer  = CampaignModelGetSerializer(obj, many= True, context=\
                                                    {"request":self.request})
            return Response(serializer.data)

        except:
            logger.error("Error: %s", traceback.format_exc())
            return Response({"Error": "Check the logs"})


class CampaignCUDApiView(APIView):
    authentication_classes = [JWTAuthentication]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def post(self, request, format=None):
        # try:
            if CampaignPostPermission().has_permission(request, CampaignCUDApiView):
                post_data = request.data
                print (post_data)
                print (request.session)
                print ("Session variable print ******", request.session['username'])
                print ("************")
                print (post_data.get('image'))
                if CampaignPostPermission().has_status_update_permission\
                    (request, CampaignCUDApiView, post_data):
                    serializer  = CampaignModelSerializer(data=post_data,context=\
                                                            {"request":self.request})
                    if serializer.is_valid():
                        serializer.save()
                        return Response({"Success": "Campaign posted"}, status=201)
                    return Response(serializer.errors, status=400)

            return Response({"Error": "Permission denied"}, status=400)

        # except:
        #     logger.error("Error: %s", traceback.format_exc())
        #     return Response({"Error": "Check the logs"})


    def put(self, request, format=None):
        try:
            query = request.data
            if 'id' in query:
                obj = CampaignModel.objects.filter(pk=query['id']).distinct()
                print (obj)
                if obj.exists():
                    if CampaignPutDelPermission().has_object_permission\
                            (request, CampaignCUDApiView, obj[0]) and\
                        CampaignPutDelPermission().has_status_update_permission\
                            (request, CampaignCUDApiView, obj[0], query):
                        serializer = CampaignModelSerializer( obj , data=query, \
                                                            context={"request":self.request})
                        if serializer.is_valid():
                            serializer.save()
                            return Response({"Success": "Campaign updated"}, \
                                            status=201)
                        return Response(serializer.errors, status = 400)

                    return Response({"Error": "Permission denied"}, status = 400)
            return Response({"Error":"ID does not exist"}, status = 400)

        except:
            logger.error("Error: %s", traceback.format_exc())
            return Response({"Error": "Check the logs"})


    def delete(self, request, format=None):
        try:
            query = request.GET
            print (query)
            if 'id' in query:
                obj = CampaignModel.objects.filter(pk=query['id']).distinct()
                if obj.exists():
                    if CampaignPutDelPermission().has_object_permission\
                                    (request, CampaignCUDApiView, obj[0]):
                        obj.delete()
                        return Response({"Success": "Campaign deleted"}, status=201)

                    return Response({"Error": "Permission denied"}, status = 400)
            return Response({"Error": "Campaign not found"}, status = 400)

        except:
            logger.error("Error: %s", traceback.format_exc())
            return Response({"Error": "Check the logs"})
