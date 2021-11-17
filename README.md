# prof
###### Full Django User Registration System (signup, login, logout, change username, change password, reset password)

[![prof](https://img.shields.io/badge/build-passing-brightgreen.svg)]()
[![version](https://img.shields.io/badge/version-2.0-green.svg)]()
[![status](https://img.shields.io/badge/status-stable-brightgreen.svg)]()
[![python](https://img.shields.io/badge/python-3-blue.svg)](http://www.python.org/download/)
[![django](https://img.shields.io/badge/django-3-blue.svg)](https://pypi.org/project/Django/)

## REQUIREMENTS
- Python-3 --> http://www.python.org/download/
- Django-3 --> https://pypi.org/project/Django/
- Django REST framework --> https://www.django-rest-framework.org/#installation
- six --> https://pypi.org/project/six/
- django-crispy-forms --> https://pypi.org/project/django-crispy-forms/

## Notes
- You can easily edit templates (or project).
- Very simple and easy to use.
- Created for educational purposes.

## V2 What's New:
- Add api.
- User List (You can view other user's information).
- Add more profile informations like Avatar.

## Installation

- Clone this repo and install requirements:
	
	```
	$ git clone https://github.com/AI35/prof
	$ pip install -r requirements.txt
	```

## Configuration

#### settings.py:
- INSTALLED_APPS :
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'prof',
    'crispy_forms',
    'six',
    'rest_framework',
    'profile_api',
]
```
- TEMPLATES :
```
import os

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'prof/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```
- Add LOGIN_URL and DATA_UPLOAD_MAX_NUMBER_FIELDS :
```
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240
LOGIN_URL = '/login/'
```
- Add Media settings :
```
MEDIA_URL = '/media/'
MEDIA_ROOT=os.path.join(BASE_DIR,'prof/media')
```
- Add Rest Framework settings :
```
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
```
- Add EMAIL settings:
	- if you want use gmail account don't forget enable low secure app in your google account settings.
```
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'example@gmail.com'
EMAIL_HOST_PASSWORD = '*****'
EMAIL_PORT = 587
```
#### urls.py:
- Project urls.py, not app urls :
```
from django.urls import path, include
from rest_framework import routers
from profile_api import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('prof.urls')),
    path('api/', include(router.urls)),
    path('api/', include('rest_framework.urls', namespace='rest_framework')),
]

```

## Run project:
- First you need to create Database:
```
$ python manage.py makemigrations
$ python manage.py makemigrations prof
$ python manage.py migrate
```
- Open 127.0.0.1:8000 in Browser
- To use api go to 127.0.0.1:8000/api

###### ALI .B .OTH
