from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager
from django.dispatch import receiver
from django.db.models.signals import post_save
from simple_history.models import HistoricalRecords


# Create your models here.
class UserManager(BaseUserManager):

 def create_user(self, email, username, password=None):
  if not email:
   raise ValueError('Users need an E-Mail address.')
  if not username:
   raise ValueError('Users need an Username address.')

  user = self.model(
         email=self.normalize_email(email),
         username=username,
  )

  user.set_password(password)  
  user.save(using=self._db)
  return user

 def create_superuser(self, email, username, password=None):
  if not email:
   raise ValueError('Users need an E-Mail address.')
  if not username:
   raise ValueError('Users need an Username address.')

  user = self.create_user(
         email=self.normalize_email(email),
         password= password,
         username=username,
  ) 
  user.is_admin = True
  user.is_staff = True
  user.is_superuser = True
  user.save(using=self._db)
  return user 

class User(AbstractUser, PermissionsMixin):
 username = models.CharField(primary_key=True ,max_length=20, unique=True)
 email = models.EmailField(unique=True)
 date_joined = models.DateTimeField(auto_now_add=True)

 USERNAME_FIELD = 'username'
 REQUIRED_FIELDS = ['email']
 objects = UserManager()
 deleted = models.BooleanField(default=False)
 is_admin = models.BooleanField(default=False)
 is_active = models.BooleanField(default=True)
 is_staff = models.BooleanField(default=False)
 is_superuser = models.BooleanField(default=False)
 def __str__(self):
  return self.username
 

class Balance(models.Model):
 user = models.OneToOneField('users.User', primary_key=True, on_delete=models.CASCADE)
 amount = models.DecimalField(default=0,max_digits=8, decimal_places=2)
 history = HistoricalRecords()

@receiver(post_save, sender=User)
def create_user_Balance(sender, instance, created, **kwargs):
 if (not Balance.objects.filter(user=instance).exists()): 
  Balance(user=instance).save()

