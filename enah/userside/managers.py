from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):

    def create_user(self,email,password=None,phone=None,name=None):

        if not email:
            raise ValueError("The Email field must be set")
        email=self.normalize_email(email)
        user=self.model(name=name,email=email,phone=phone,password=password)
        user.set_password(password)
        user.save()

        return user