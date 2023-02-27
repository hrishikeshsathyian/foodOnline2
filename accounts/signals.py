from django.db.models.signals import post_save,pre_save
from .models import User, UserProfile
from django.dispatch import receiver

def post_save_create_profile_receiver(sender,instance,created,**kwargs):
    print(created)
    if created:
        UserProfile.objects.create(user=instance)
        print('user profile is created')
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except:
            # create the user profile if it does not exist
            UserProfile.objects.create(user=instance)
            print('profile did not exist, but I created one')
        print('user is updated')  
post_save.connect(post_save_create_profile_receiver,sender=User)

@receiver(pre_save,sender=User)
def pre_save(sender,instance,**kwargs):
    print(instance.username,"this user is being saved")
