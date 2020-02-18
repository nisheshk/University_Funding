from rest_framework import serializers
from campaign.models import CampaignModel

class CampaignModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CamapaignModel
        fields = ['title',
                  'description',
                  'unit',
                  'amount',
                  'inventory',
                  'created_on',
                        ]
