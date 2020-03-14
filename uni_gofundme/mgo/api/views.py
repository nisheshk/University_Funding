from rest_framework.views       import APIView
from campaign.models            import CampaignModel
from rest_framework             import serializers
from rest_framework.response    import Response
from .custom_permissions        import CampaignMGOActionPermission
from .serializers import CampaignMGOActionSerializer


class CampaignMGOAction(APIView):
    def patch(self, request, format=None):
        query = request.data
        if CampaignMGOActionPermission().has_permission(request, CampaignMGOAction):
            obj = CampaignModel.objects.all()
            if query.get("id", None):
                print ("Entered***")
                obj = obj.get(pk=query['id'])
                print ("Entered***")
                serializer = CampaignMGOActionSerializer(obj, data=query, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"Success":"Campaign updated"})
                return Response(serializer.errors,status=400)
            return Reponse({"Error":"Id does not exist"})
        else:
            return Response({"Error":"Permission Denied"}, status=400)
