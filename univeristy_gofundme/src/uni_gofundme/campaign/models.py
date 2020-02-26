from django.db import models
from datetime import datetime
from accounts.models import User
from django.contrib.postgres.fields import ArrayField


class PriceUnitModel(models.Model):
    unit            = models.CharField(max_length = 10, blank=False)
    description     = models.CharField(max_length = 100, blank=True, null = True)

    class Meta:
        db_table = "campaign_price_unit"


class CampaignModel(models.Model):
    title           = models.CharField(max_length = 200, blank=False, null = True)
    description     = models.TextField(blank=False, null = True)
    unit_id         = models.ForeignKey(PriceUnitModel, on_delete=models.CASCADE, db_column='unit_id', null=True, blank=True)
    amount          = models.DecimalField(max_digits=19, decimal_places=2, blank = True, null=True)
    inventory       = ArrayField(models.CharField(max_length=300), blank=True, null=True)
    created_by_id   = models.ForeignKey(User, on_delete=models.CASCADE, db_column='created_by_id', null=True, blank=True)
    created_on      = models.DateTimeField(default=datetime.now, null=True)
    modified_by     = models.CharField(max_length=100, blank=True, null=True)
    modified_on     = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "campaign_details"
