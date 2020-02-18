from rest_framework.generics    import ListAPIView
from campaign.models            import CampaignModel
#from campaign.api.serializers   import CamapaignModelSerializer
from rest_framework.views       import APIView
from rest_framework             import serializers
from rest_framework.response    import Response

class CampaignListApiView(APIView):
    permission_classes      = []
    authentication_classes  = []

    def get(self, request, format=None):
        query = request.GET
        print (query)
        obj = CampaignModel.objects.values('title','description','unit__unit','amount','inventory',
                                    'created_by__username','created_on')
        return Response(obj)
