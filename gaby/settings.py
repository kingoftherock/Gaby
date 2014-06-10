# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'gn8s*f9l67vvart0bhp5ov-o2xelo5s!c&#1&ia+d!x(6sb^g7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = TEMPLATE_DEBUG = True
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social.apps.django_app.default',
    'home',
    'userProfiles',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

ROOT_URLCONF = 'gaby.urls'

WSGI_APPLICATION = 'gaby.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', #'django.db.backends.sqlite3',
        'NAME': 'dd25tcisks81d3',
        'USER': 'uuibrcybxqbuur',
        'PASSWORD': 'XNiMRNDYlMtc5gsZy7dKj2v0Ox',
        'HOST': 'ec2-54-243-48-227.compute-1.amazonaws.com', #'localhost', #
        'PORT': '5432',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'es-MX'

TIME_ZONE = 'America/Mexico_City'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'



STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

#API KEYS SOCIAL LOGIN
TwitterKey = "gxYSOaOmg1ePKG5N1IKAw"
TwitterSecret = "I26ZcyTQHZsRv9XSoZbH8hcih26tTuFRGlwuebcjWC4"
FacebookKey = 280417938784662
FacebookSecret = "242ab47423894dc7a69315245c0ffec6"

#Twitter
SOCIAL_AUTH_TWITTER_KEY = TwitterKey
SOCIAL_AUTH_TWITTER_SECRET = TwitterSecret

#Facebook

SOCIAL_AUTH_FACEBOOK_KEY = FacebookKey
SOCIAL_AUTH_FACEBOOK_SECRET = FacebookSecret

AUTHENTICATION_BACKENDS = (
    'social.backends.twitter.TwitterOAuth',
    'social.backends.facebook.FacebookAppOAuth2',
    'social.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_LOGIN_REDIRECT_URL = 'alumno'
SOCIAL_AUTH_LOGIN_URL = 'log-out'
SOCIAL_AUTH_BACKEND_ERROR_URL = 'gaby'
SOCIAL_AUTH_LOGIN_ERROR_URL = 'gaby'

#Emails
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'dreediMX@gmail.com'
EMAIL_HOST_PASSWORD = 'dreediBatiz123'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
