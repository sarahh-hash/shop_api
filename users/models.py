from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from users.managers import CustomUserManager
class  CustomUser(AbstractBaseUser,PermissionsMixin):
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    hands = models.IntegerField(default=2)
    phone_number = models.CharField(max_length=12, blank=True,null=True)
    objects = CustomUserManager()
    REQUIRED_FIELDS = ["hands", "phone_number"]
    USERNAME_FIELD = "email"
    def __str__(self)->str:
        return self.email or  "ничего"
    
class ConfirmationCode(models.Model):
    user = models.OneToOneField(CustomUser,on_delete = models.CASCADE,related_name='confirmation_code')
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add = True)

   
    def __str__(self):
        return f"Код подтверждения для {self.user.email}"
    