from django.db import models
from django.contrib.auth.models import User
# from django.template.defaultfilters import slugify

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='profilepic', blank = True)
    
    """ slug = models.SlugField(default="", null=False)

    def save(self, *args, **kwargs):
        
        self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)
         """