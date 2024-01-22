from .base import *
 
DEBUG = True
ALLOWED_HOSTS = []
 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'proyecto_3',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '',

	}
}
