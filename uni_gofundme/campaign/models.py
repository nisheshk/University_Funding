from django.db import models
from datetime import datetime
from accounts.models import User
from django.contrib.postgres.fields import ArrayField


class PriceUnitModel(models.Model):
    unit            = models.CharField(max_length = 10, blank=False)
    description     = models.CharField(max_length = 100, blank=True, null = True)

    class Meta:
        db_table = "campaign_price_unit"

class CampaignStatusModel(models.Model):
    """
        0 -> Waiting for approval, 1-> Approved, 2-> Rejected
    """
    status          = models.CharField(max_length = 25)
    remarks         = models.CharField(max_length = 200, blank=True, null = True)

    class Meta:
        db_table = "campaign_status"

def upload_image(instance, filename):
    return "campaign/{0}/{1}".format(instance.created_by_id, filename)


class CampaignModel(models.Model):
    title           = models.CharField(max_length = 200, blank=False, null = False)
    description     = models.TextField(null = False, blank=False)
    unit_id         = models.ForeignKey(PriceUnitModel, on_delete=models.CASCADE, db_column='unit_id', null=True, blank=True, related_name='unit_type')
    amount          = models.DecimalField(max_digits=19, decimal_places=2, blank = True, null=True)
    inventory       = ArrayField(models.CharField(max_length=300), blank=True, null=True)
    image           = models.ImageField(upload_to= upload_image, null=True, blank=True)
    created_by_id   = models.ForeignKey(User, on_delete=models.CASCADE, db_column='created_by_id', related_name='user')
    created_on      = models.DateTimeField(default=datetime.now, null=True)
    status_id       = models.ForeignKey(CampaignStatusModel, on_delete=models.CASCADE, db_column='status_id', related_name='status_code', default=0)
    modified_by_id  = models.ForeignKey(User, on_delete=models.CASCADE, db_column='modified_by_id', null=True, related_name='modified_by')
    modified_on     = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "campaign_details"
        ordering = ["-created_on"]

    @property
    def unit_type(self):
        return self.unit_id.unit

    @property
    def status_type(self):
        return self.status_id.status


    @property
    def modified_by(self):
        return self.modified_by_id.username

    @property
    def owner(self):
        return self.created_by_id
