from django.contrib import admin
from .models import User, DonorProfile, FundRaiserProfile, MGOProfile
# Register your models here.

admin.site.register(User)
admin.site.register(DonorProfile)
admin.site.register(FundRaiserProfile)
admin.site.register(MGOProfile)
