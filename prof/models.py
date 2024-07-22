from django.db import models
from django.contrib.auth.models import User
# from django.template.defaultfilters import slugify
from django.core.cache import cache 
import datetime
from mysite import settings

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='profilepic', blank = True)
    online_now = models.BooleanField(default=True)

    """ slug = models.SlugField(default="", null=False)

    def save(self, *args, **kwargs):
        
        self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)
         """
    
    def last_seen(self):
        return cache.get('seen_%s' % self.user.username)

    def online(self):
        if self.last_seen():
            now = datetime.datetime.now()
            if now > self.last_seen() + datetime.timedelta(
                         seconds=settings.USER_ONLINE_TIMEOUT):
                return False
            else:
                return True
        else:
            return False 