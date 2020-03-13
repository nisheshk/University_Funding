from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import user_logged_in, user_logged_out
from django.contrib.sessions.models import Session


# Create your models here.
class User(AbstractUser):
    type        = models.CharField(blank=True, null=True,max_length=1)

    @property
    def is_donor(self):
        """
            This method checks is the user is donor.
            Returns
            -------
            True
        """
        if type == 'd':
            return True

    @property
    def is_mgo(self):
        """
            This method checks is the user is Major Gift Officer.
            Returns
            -------
            True
        """
        if type == 'm':
            return True

    @property
    def is_fundraiser(self):
        """
            This method checks is the user is fund raiser.
            Returns
            -------
            True
        """
        if type == 'f':
            return True

class DonorProfile(models.Model):
    user =  models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    location = models.CharField(max_length=100, blank=True, null=True)

class FundRaiserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

class MGOProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

#This method needs to be changed later. It should be when user registers as
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):

    """
        It saves the new users into its respecitve user type profile.
        This method is trigerred after the user is saved.

        Parameters:
        -----------
        sender: User object
        instance: User object
        created: boolean
        kwargs: dic

        Returns
        --------
        Does not return anythin; since its just a signal.
    """

    try:
        if instance.type == 'd':
            DonorProfile.objects.get_or_create(user = instance)
        elif instance.type == 'f':
            FundRaiserProfile.objects.get_or_create(user = instance)
        elif instance.type == 'm':
            MGOProfile.objects.get_or_create(user = instance)
    except:
        logger.error("Error: %s", traceback.format_exc())
        return Response({"Error": "Check the logs"})
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
