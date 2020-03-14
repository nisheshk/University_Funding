from rest_framework import serializers
from campaign.models import CampaignModel, PriceUnitModel, CampaignStatusModel
from accounts.serializers import UserSerializer
from accounts.models import User
from django.utils import timezone
from PIL import Image
import boto3
from django.conf import settings
from django.core.files.storage import default_storage as storage
import io

class CampaignModelGetSerializer(serializers.ModelSerializer):
    unit_type       = serializers.ReadOnlyField()
    status_type     = serializers.ReadOnlyField()
    modified_by     = serializers.ReadOnlyField()
    user            = UserSerializer(read_only = True, source='created_by_id')
    class Meta:
        model = CampaignModel
        fields = ['id',
                  'title',
                  'description',
                  'unit_type',
                  'amount',
                  'status_type',
                  'user',
                  'image',
                  'inventory',
                  'created_on',
                  'modified_by',
                  'modified_on',
                  ]

    def retrieve(self, validated_data):
        print ("Entered")
        return validated_data

class CampaignModelSerializer(serializers.ModelSerializer):
    unit_type       = serializers.CharField(max_length=10, allow_null=True, allow_blank=True, required=False)
    status_type     = serializers.CharField(max_length=25,required=False)
    #image           = serializers.ImageField(allow_empty_file=True)
    class Meta:
        model = CampaignModel
        fields = [
                  'title',
                  'description',
                  'unit_type',
                  'amount',
                  'status_type',
                  'inventory',
                  'image',
                  'created_on',
                  'modified_on',
                  ]

    def get_status_type(self, val):
        request = self.context['request']
        if request.method == "POST":
            return "Waiting for approval"

    def created_or_modified_by(self):
        request = self.context['request']
        # print (request.session['username'])
        username = request.session['username']
        print (username)
        obj = User.objects.filter(username=username).distinct()
        print (obj)
        return obj[0]

    def validate_status_type(self, val):
        obj = CampaignStatusModel.objects.filter(status=val).distinct()
        if not obj.exists():
            raise serializers.ValidationError("Invalid status code")
        return obj[0]

    def validate_created_by(self, val):
        obj = User.objects.filter(username=val).distinct()
        if not obj.exists():
            raise serializers.ValidationError("Invalid username")
        return obj[0]

    def validate_unit_type(self, val):
        if val is not None:
            obj = PriceUnitModel.objects.filter(unit=val).distinct()
            if not obj.exists():
                raise serializers.ValidationError("Invalid unit type for the currency")
            return obj[0]

    def validate_amount(self, val):
        if val is not None and val > 10000000:
            raise serializers.ValidationError('Amount is too high')
        return val

    def validate(self, data):
        if (data.get('amount') is not None) and (data.get('unit_type') is None):
            raise serializers.ValidationError('Unit type can not be null when '
                                               'amount is provided')

        if (data.get('unit_type') is not None) and (data.get('amount') is None):
            raise serializers.ValidationError('Amount can not be null when     '
                                               'unit type is provided')


        if (data.get('amount',None) is None and data.get('inventory') is None):
            raise serializers.ValidationError('Either amount or inventory must '
                                                'be provided')

        return data

    def set_attributes(self, validated_data):
        obj = {"title" :        validated_data.get('title',None),
               "amount" :       validated_data.get('amount',None),
               "description" :  validated_data.get('description',None),
               "inventory" :    validated_data.get('inventory',None),
               "unit_id" :      validated_data.get('unit_type',None),
               "status_id":     validated_data.get('status_type',None),
               "image":         validated_data.get('image',None),
                      }
        obj = { k:v for k, v in obj.items() if v }
        return obj

    def create(self, validated_data):
        print (validated_data)
        obj = self.set_attributes(validated_data)
        obj['created_by_id'] = self.created_or_modified_by()
        CampaignModel(**obj).save()
        return obj

    def update(self, update_obj, validated_data):
        obj = update_obj[0]
        print (obj.title)
        print (validated_data)
        obj.title = validated_data.get('title',None)
        obj.amount = validated_data.get('amount',None)
        obj.description = validated_data.get('description',None)
        obj.inventory = validated_data.get('inventory',None)
        obj.modified_by_id = self.created_or_modified_by()
        obj.modified_on = timezone.now()
        obj.unit_id = validated_data.get('unit_type',None)
        if validated_data.get("status_type", None):
            obj.status_id = validated_data.get("status_type")

        if validated_data.get("image",None):
            obj.image = validated_data.get("image")

        print (obj.title, obj.amount)
        obj.save()
        return obj
