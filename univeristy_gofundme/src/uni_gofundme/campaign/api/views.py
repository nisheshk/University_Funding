from rest_framework.generics    import ListAPIView
from campaign.models            import CampaignModel, PriceUnitModel
from accounts.models            import User
from campaign.api.serializers   import CampaignModelSerializer
from rest_framework.views       import APIView
from rest_framework             import serializers
from rest_framework.response    import Response
from django.db.models           import F
from django.db.models           import Q
from django.core                import serializers


class CampaignListApiView(APIView):
    permission_classes      = []
    authentication_classes  = []
    foreign_key_fields      = {'unit_id':[PriceUnitModel,'unit'],
                                'created_by_id':[User,'username']}

    def get_campaign_object(self):
        obj = CampaignModel.objects.values('title', 'description',
                                            'amount',
                                             'inventory', 'created_on',
                                            'modified_on',
                                            unit=F('unit_id__unit'),
                                            username=F('created_by_id__username'),firstname=F\
                                            ('created_by_id__first_name'),lastname=F\
                                            ('created_by_id__last_name'))
        print (obj)
        return obj

    def build_filter(self, fitler_key, filter_val, filter_cond=''):
        kwargs = {}
        kwargs['{0}{1}'.format(fitler_key, filter_cond)] = filter_val
        return kwargs


    def get(self, request, format=None):
        query = request.data
        obj = self.get_campaign_object()

        if query:
            for filters in query:
                kwargs = self.build_filter(fitler_key=filters, filter_val=query[filters])
            obj = obj.filter(**kwargs)
        print (obj, '***')
        serializer  = CampaignModelSerializer(obj, many= True, context=\
                                                {"request":self.request})
        print (serializer.data)
        return Response(serializer.data)

    def get_foreign_key_val(self, data, condition=''):
        for fields in data:
            if fields in self.foreign_key_fields:
                kwargs = self.build_filter(self.foreign_key_fields[fields][1],\
                                             data[fields], condition)
                query = self.foreign_key_fields[fields][0].objects.filter\
                                            (**kwargs).distinct()
                if len(query) == 1:
                    data[fields] = query[0].id
                else:
                    return ('Error value on field ' + fields, 0)
        print (data , '*************')
        return data, 1

    def post(self, request, format=None):
        try:
            post_data, status   = self.get_foreign_key_val(data=request.data)
            print (post_data)
            if status:
                serializer  = CampaignModelSerializer(data=post_data, context=\
                                                        {"request":self.request})
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors)
            return Response({'Error':post_data})
        except Exception as e:
            print (e)
            return Response({'Error':'Check the logs'})

    def put(self, request, format=None):
        query = request.data
        print (query)
        if 'id' in query:
            obj = CampaignModel.objects.get(pk=query['id'])
            serializer = CampaignModelSerializer( obj , data=request.data)
        else:
            serializer = CampaignModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status = 400)
