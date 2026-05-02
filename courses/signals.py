from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token # ✅ Token ke liye
from .models import Profile # ✅ Profile ke liye

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def handle_new_user_setup(sender, instance, created, **kwargs):
    if created:
        # 1. API Token generate karega (Taki login ke baad error na aaye)
        Token.objects.create(user=instance)
        
        # 2. User Profile generate karega
        Profile.objects.get_or_create(user=instance)
        
        # 3. Notification Logic (DEBUG ke liye print kar raha hoon)
        # Yahan aap apna Notification model ya FCM trigger dal sakte hain
        print(f"🔥 Success: Token & Profile created for {instance.username}")