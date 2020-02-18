from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class User(AbstractUser):
    type        = models.CharField(blank=True, null=True,max_length=1)

    @property
    def is_donor(self):
        if type == 'd':
            return True

    @property
    def is_mgo(self):
        if type == 'm':
            return True

    @property
    def is_fundraiser(self):
        if type == 'f':
            return True

class DonorProfile(models.Model):
    user =  models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    location = models.CharField(max_length=100, blank=True, null=True)

class FundRaiserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

class MGOProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    print('**', created)
    print (kwargs)
    print ('Entered')
    if instance.type == 'd':
        DonorProfile.objects.get_or_create(user = instance)
    elif instance.type == 'f':
        FundRaiserProfile.objects.get_or_create(user = instance)
    elif instance.type == 'm':
        MGOProfile.objects.get_or_create(user = instance)
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
# 	# print('_-----')
# 	# # print(instance.internprofile.bio, instance.internprofile.location)
# 	# if instance.is_donor:
# 	# 	instance.intern_profile.save()
# 	# else:
# 	# 	HRProfile.objects.get_or_create(user = instance)
#     pass
