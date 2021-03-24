from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from allauth.account.signals import user_logged_in,user_logged_out
from allauth.socialaccount.models import SocialAccount
from urllib.parse import unquote

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
	instance.profile.save()

# @receiver(user_logged_in)
# def save_dp(request,user,**kwargs):
# 	mine = SocialAccount.objects.filter(user=request.user).first()
# 	profile = Profile.objects.get(user=request.user)
# 	image_url = mine.get_avatar_url()
# 	ind = image_url.index('lh3')
# 	profile.profile_pic = str(image_url[ind:])
# 	print("Hello", profile.profile_pic)
# 	profile.save()