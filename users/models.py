from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    """Exends BaseUserManager"""

    def create_user(self, email, first_name, last_name, access_level, password=None):
        """Create a user and save to DB

        Args:
            email ([str]): valid email address
            first_name ([str]): first name
            last_name ([str]): last name
            password ([str], optional): password. Defaults to None.

        Raises:
            ValueError: email or first name or last name is missing

        Returns:
            [User]: Custom user, an extension of AbstractBaseUser
        """
        if not email or not first_name or not last_name:
            raise ValueError("User must have email address, first name, and last name. ")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name.title(),
            last_name=last_name.title(),
            name = first_name.title() + " " + last_name.title(),
            access_level = access_level
        )
        user.is_admin = True if access_level == "Administrator" else False
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        """Creates super user. Used mostly in terminal

        Args:
            email ([str]): valid email address
            first_name ([str]): first name
            last_name ([str]): last name
            password ([str], optional): password. Defaults to None.

        Raises:
            ValueError: email or first name or last name is missing

        Returns:
            [User]: Custom user, an extension of AbstractBaseUser. This User is 
                    admin and is active.
        """
        if not email or not first_name or not last_name:
            raise ValueError("User must have email address, first name, and last name. ")

        user = self.create_user(
            email=self.normalize_email(email),
            first_name=first_name.title(),
            last_name=last_name.title(),
            access_level = "Administrator"
        )
        user.is_admin=True
        user.is_active=True
        user.set_password(password)
        user.save(using=self._db)
        return user
    


class User(AbstractBaseUser):
    """Extends the base user class to encoperate more fields. 

        This class should not be created directly, but through UserManager()
    """
    first_name      = models.CharField(max_length=30)
    last_name       = models.CharField(max_length=30)
    name            = models.CharField(max_length=60, default="NONE")
    email           = models.EmailField(verbose_name="email", max_length=60, unique=True)
    data_joined     = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login      = models.DateTimeField(verbose_name="last login", auto_now_add=True)    
    is_admin        = models.BooleanField(default=False)
    access_level    = models.CharField(max_length=13, default="NONE")
    is_active       = models.BooleanField(default=False) 

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def is_staff(self,):
        return self.is_admin

    def email_account_approval(self,):
        if self.email in ["jkready@ualr.edu",'abaker@ualr.edu']: #Blocking emails to test accounts
            status = send_mail(
                subject="Determined account approved!",
                message="""This email is to infom you that your account at Determined.edu is approved!
                You can now login here: http://144.167.35.152:8000""",
                from_email="determinedwebapp@gmail.com",
                recipient_list=[self.email]
            )
            if status == 0: print("Sent mail, but non delivered. There might be a problem with mail settings")

    def email_account_deny(self,):
        if self.email in ["jkready@ualr.edu",'abaker@ualr.edu']: #Blocking emails to test accounts
            status = send_mail(
                subject="Determined account",
                message="""This email is to infom you that your account at Determined.edu could not be approved at this time. 
                If you believe there was a mistake, please contact determinedwebapp@gmail.com. """,
                from_email="determinedwebapp@gmail.com",
                recipient_list=[self.email]
            )
            if status == 0: print("Sent mail, but non delivered. There might be a problem with mail settings")