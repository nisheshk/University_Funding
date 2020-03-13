from django.contrib import admin
from campaign.models import (PriceUnitModel,
                            CampaignModel,
                            CampaignStatusModel
                            )

admin.site.register(PriceUnitModel)
admin.site.register(CampaignModel)
admin.site.register(CampaignStatusModel)
