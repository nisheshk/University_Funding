from rest_framework.views       import APIView
from campaign.models            import CampaignModel
from rest_framework             import serializers
from rest_framework.response    import Response
from .custom_permissions        import CampaignMGOActionPermission
from .serializers import CampaignMGOActionSerializer
import logging
import traceback

logger = logging.getLogger(__name__)

class CampaignMGOAction(APIView):
    def patch(self, request, format=None):
        try:
            query = request.data
            if CampaignMGOActionPermission().has_permission(request, CampaignMGOAction):
                if query.get("id", None) and query.get("status_type",None):
                    obj = CampaignModel.objects.all()
                    obj = obj.get(pk=query['id'])
                    serializer = CampaignMGOActionSerializer(obj, data=query, partial=True)

                    if serializer.is_valid():
                        serializer.save()
                        return Response({"Success":"Campaign updated"}, status=200)

                    return Response(serializer.errors,status=400)
                return Response({"Error":"Either id or status not provided"}, status=400)
            return Response({"Error":"Permission Denied"}, status=401)

        except:
            logger.error("Error: %s", traceback.format_exc())
            return Response({"Error": "Check the logs"}, status=400)
