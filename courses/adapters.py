from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_field
from allauth.account.models import EmailAddress
from users.models import User  # Aapka custom user model

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        Agar email pehle se exists karta hai, toh auto-link kar do 
        taaki 'signup' page na dikhe.
        """
        # Agar user pehle se logged in hai, toh kuch na karein
        if sociallogin.is_existing:
            return

        # Google se milne wali email check karein
        email = sociallogin.account.extra_data.get('email')
        if not email:
            return

        try:
            # Check karein kya yeh email hamare database mein hai
            user = User.objects.get(email__iexact=email)
            # Existing user ko social login se link karein
            sociallogin.connect(request, user)
        except User.DoesNotExist:
            # Naya user hai, toh default behaviour chalne dein
            pass

    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        email = data.get("email")
        if email:
            # Username ko email ka pehla part banayein
            user_field(user, "username", email.split("@")[0])
        return user