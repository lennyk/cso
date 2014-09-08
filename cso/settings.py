"""
Django settings for cso project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')7d1%c_xmmm2yf82(2=ar0dmmwf-=d9zbhae3w@w51t35m&b6n'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django_admin_bootstrapped.bootstrap3',
    'django_admin_bootstrapped',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social.apps.django_app.default',
    'pages',
    'registration',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)

ROOT_URLCONF = 'cso.urls'

WSGI_APPLICATION = 'cso.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../database/db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, '../static'))

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.abspath(os.path.join(BASE_DIR, '../media'))

AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.google.GoogleOAuth2',
    'social.backends.twitter.TwitterOAuth',
    'django.contrib.auth.backends.ModelBackend',
)

# TODO: this code is scary. should have a more sane way of storing secrets. regenerate secrets when you do that.
import socket
if socket.gethostname() == 'NOT IMPLEMENTED':
    # PRD
    SOCIAL_AUTH_FACEBOOK_KEY = '1522387657973015'
    SOCIAL_AUTH_FACEBOOK_SECRET = '8d2a32053ea6d493b2c3130d20137178'
elif socket.gethostname() == 'cso':
    # SANDBOX
    SOCIAL_AUTH_FACEBOOK_KEY = '1522982181246896'
    SOCIAL_AUTH_FACEBOOK_SECRET = 'cf50b5154294cda7bd6e1a43f8a4104f'
elif socket.gethostname() == 'lennyk-dnb-mbp.local':
    # DEV
    SOCIAL_AUTH_FACEBOOK_KEY = '1522981811246933'
    SOCIAL_AUTH_FACEBOOK_SECRET = 'aed08816076d87b3c0ce13d8f3906fd1'

SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

SOCIAL_AUTH_PIPELINE = (
    # Get the information we can about the user and return it in a simple
    # format to create the user instance later. On some cases the details are
    # already part of the auth response from the provider, but sometimes this
    # could hit a provider API.
    'social.pipeline.social_auth.social_details',

    # Get the social uid from whichever service we're authing thru. The uid is
    # the unique identifier of the given user in the provider.
    'social.pipeline.social_auth.social_uid',

    # Verifies that the current auth process is valid within the current
    # project, this is were emails and domains whitelists are applied (if
    # defined).
    'social.pipeline.social_auth.auth_allowed',

    # Checks if the current social-account is already associated in the site.
    'social.pipeline.social_auth.social_user',

    # Make up a username for this person, appends a random string at the end if
    # there's any collision.
    'social.pipeline.user.get_username',

    # Send a validation email to the user to verify its email address.
    # Disabled by default.
    # 'social.pipeline.mail.mail_validation',

    # Associates the current social details with another user account with
    # a similar email address. Disabled by default.
    # 'social.pipeline.social_auth.associate_by_email',

    # Create a user account if we haven't found one yet.
    'social.pipeline.user.create_user',

    # Create the record that associated the social account with this user.
    'social.pipeline.social_auth.associate_user',

    # Populate the extra_data field in the social record with the values
    # specified by settings (and the default ones like access_token, etc).
    'social.pipeline.social_auth.load_extra_data',

    # Update the user record with any changed info from the auth service.
    'social.pipeline.user.user_details',

    # Custom
    'registration.pipeline.create_or_update_registrant',
)

LOGIN_URL = '/registration/login/'
LOGIN_REDIRECT_URL = '/registration/'
LOGOUT_URL = '/'

# Used to redirect the user once the auth process ended successfully. The value of ?next=/foo is used if it was present
# SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/logged-in/'

# URL where the user will be redirected in case of an error
# SOCIAL_AUTH_LOGIN_ERROR_URL = '/login-error/'

# Is used as a fallback for LOGIN_ERROR_URL
# SOCIAL_AUTH_LOGIN_URL = '/login-url/'

# Used to redirect new registered users, will be used in place of SOCIAL_AUTH_LOGIN_REDIRECT_URL if defined.
# SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/new-users-redirect-url/'

# Like SOCIAL_AUTH_NEW_USER_REDIRECT_URL but for new associated accounts (user is already logged in). Used in place of SOCIAL_AUTH_LOGIN_REDIRECT_URL
# SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL = '/new-association-redirect-url/'

# The user will be redirected to this URL when a social account is disconnected
# SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = '/account-disconnected-redirect-url/'

# Inactive users can be redirected to this URL when trying to authenticate.
# SOCIAL_AUTH_INACTIVE_USER_URL = '/inactive-user/'
