"""
Django settings for efcorps project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import pymlconf
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

GLOBAL_CONFIG_DIR = '/etc/efcorps'
# Load configuration from conf.d directories #
# default configuration in repo:
config = pymlconf.ConfigManager(
    dirs=[os.path.join(BASE_DIR, 'conf.d')],
    filename_as_namespace=False
)
if os.path.isdir(GLOBAL_CONFIG_DIR):
    config.load_dirs(
        [os.path.join(GLOBAL_CONFIG_DIR, 'conf.d')],
        filename_as_namespace=False
    )
locals().update((key.upper(), value) for key, value in config.items())

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1b4kjfz1qubau-ubgg$(@pwt_n73%cr-4#tbrkd$e8b_jh#i_)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'magnus',
    'south',
)

MIDDLEWARE_CLASSES = ()

ROOT_URLCONF = 'efcorps.urls'

WSGI_APPLICATION = 'efcorps.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
