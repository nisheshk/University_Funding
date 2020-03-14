from rest_framework import serializers
from campaign.models import CampaignModel, CampaignStatusModel


class CampaignMGOActionSerializer(serializers.ModelSerializer):
    status_type     = serializers.CharField(write_only = True)

    class Meta:
        model = CampaignModel
        fields = ['id', 'status_type']

    def validate_status_type(self, val):
        obj = CampaignStatusModel.objects.filter(status=val).distinct()
        if not obj.exists():
            raise serializers.ValidationError("Invalid status code")
        print (obj[0])
        return obj[0]

    def update(self, upd_obj, data):
        upd_obj.status_id = data.get("status_type")
        upd_obj.save()
        return upd_obj
