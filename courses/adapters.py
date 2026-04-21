from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_field

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        Agar user already email se register hai, toh use social account se link kar do
        taaki 'user with this email already exists' ka error na aaye.
        """
        pass

    def populate_user(self, request, sociallogin, data):
        """
        Google se milne wale data se user fields populate karna.
        """
        user = super().populate_user(request, sociallogin, data)
        # Username ko unique banane ke liye email use karna sabse best hai
        email = data.get("email")
        if email:
            user_field(user, "username", email.split("@")[0]) # email ka pehla part username banayega
        return user

    def authentication_error(self, request, provider_id, error=None, exception=None, extra_context=None):
        print(f"DEBUG LOGIN ERROR: {error}, {exception}, {extra_context}")