from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from PIL import Image

# Create your models here.


class User(AbstractUser):
    ROLES = (('0','Admin'),('1','Reporter'),('2','Guest'))
    role = models.CharField(choices=ROLES, default='2', max_length= 1)
    email = models.EmailField(_('email address'), unique=True)
    REQUIRED_FIELDS = ('email',)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(null= True, blank = True)
    address = models.CharField(max_length=100, blank=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pic')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)