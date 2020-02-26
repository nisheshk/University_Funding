from rest_framework import serializers
from campaign.models import CampaignModel
from django.db import models

class CampaignModelSerializer(serializers.ModelSerializer):
    unit            = serializers.SerializerMethodField()
    email           = serializers.SerializerMethodField()
    firstname       = serializers.SerializerMethodField()
    lastname        = serializers.SerializerMethodField()
    class Meta:
        model = CampaignModel
        fields = ['title',
                  'description',
                  'unit',
                  'created_by_id',
                  'unit_id',
                  'amount',
                  'firstname',
                  'lastname',
                  'inventory',
                  'email',
                  'created_on',
                  'modified_by',
                  'modified_on',
                  ]


    def get_unit(self, obj):
        if self.context['request'] == 'GET':
            return obj['unit']

    def get_firstname(self, obj):
        if self.context['request'] == 'GET':
            return obj['firstname']

    def get_lastname(self, obj):
        if self.context['request'] == 'GET':
            return obj['lastname']

    def get_email(self, obj):
        if self.context['request'] == 'GET':
            return obj['username']

    def validate_amount(self, val):
        if val > 10000000:
            raise serializers.ValidationError('Amount is too high')
        return val
