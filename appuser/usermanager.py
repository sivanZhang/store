from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,PermissionsMixin
)
import pdb
 

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username = name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,  password, name):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
            password=password,
            username = name
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    
    def uniqueUsername(self, username):
        """
        check if the username is unique
        if unique, return True
        else return False
        """
        try: 
            self.get(username=username)
            return False
        except self.model.DoesNotExist:
            return True
        except self.model.MultipleObjectsReturned:
            return False
    
    def uniqueEmail(self, email):
        """
        check if the email is unique
        if unique, return True
        else return False
        """
        try: 
            self.get(email=email)
            return False
        except self.model.DoesNotExist:
            return True
        except self.model.MultipleObjectsReturned:
            return False

class AdaptorUserManager(UserManager):
    pass