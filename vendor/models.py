from django.db import models
from accounts.models import User, UserProfile
from accounts.utils import send_notification
# Create your models here.
class Vendor(models.Model):
    user = models.OneToOneField(User, related_name='user',on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile,related_name='userprofile',on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=60)
    vendor_license = models.ImageField(upload_to="vendor/license",blank=True,null=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name
    
    def save(self,*args,**kwargs):
        if self.pk is not None:
            # checks if item is being saved for the first time (Created) or if it is being updated
            orig = Vendor.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                context = {
                    'user': self.user,
                    'is_approved': self.is_approved,
                }
                if self.is_approved == True :
                    # send  email
                    mail_subject = "Congratulations! Your Restaurant has been approved!"
                    mail_template = 'accounts/emails/admin_approval_email.html'
                    send_notification(mail_subject,mail_template,context)
                else:
                    #send email
                    mail_subject = "Unfortunately your isting has not been approved by the admin"
                    mail_template = 'accounts/emails/admin_approval_email.html'
                    send_notification(mail_subject,mail_template,context)

        return super(Vendor,self).save(*args,**kwargs)