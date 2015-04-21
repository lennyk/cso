import os

from configurations import Configuration
import dj_database_url


class Base(Configuration):
    # --------------------------------------------------
    # Django
    # --------------------------------------------------

    BASE_DIR = os.path.dirname(os.path.realpath(os.path.dirname(__file__)))

    # replaced during deployment
    SECRET_KEY = ')7d1%c_xmmm2yf82(2=ar0dmmwf-=d9zbhae3w@w51t35m&b6n'

    DEBUG = False
    TEMPLATE_DEBUG = True

    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = 'America/Los_Angeles'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True

    TEMPLATE_DIRS = (
        os.path.join(BASE_DIR, 'templates'),
    )

    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    STATICFILES_DIRS = (
        os.path.abspath(os.path.join(BASE_DIR, './bower_components/bootstrap-sass-official/assets')),
        os.path.abspath(os.path.join(BASE_DIR, './bower_components/bootstrap-social')),
        os.path.abspath(os.path.join(BASE_DIR, './bower_components/font-awesome')),
        os.path.abspath(os.path.join(BASE_DIR, './bower_components/jquery/dist')),
        os.path.abspath(os.path.join(BASE_DIR, './bower_components/jquery.payment/lib')),
        os.path.abspath(os.path.join(BASE_DIR, './bower_components/lightbox2')),
    )

    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        'compressor.finders.CompressorFinder',
    )

    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.abspath(os.path.join(BASE_DIR, './media'))

    ROOT_URLCONF = 'cso.urls'

    WSGI_APPLICATION = 'cso.wsgi.application'

    SITE_ID = 2

    LOGIN_REDIRECT_URL = '/registration/'

    AUTH_USER_MODEL = 'cso.CSOUser'

    INSTALLED_APPS = (
        'django_admin_bootstrapped',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.sites',
        'debug_toolbar',
        'revproxy',
    )

    # cso apps
    INSTALLED_APPS += (
        'cso',
        'events',
        'registration',
    )

    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
    )

    MIDDLEWARE_CLASSES = (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'sslify.middleware.SSLifyMiddleware',
    )

    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.contrib.auth.context_processors.auth',
        'django.core.context_processors.debug',
        'django.core.context_processors.i18n',
        'django.core.context_processors.media',
        'django.core.context_processors.static',
        'django.core.context_processors.tz',
        'django.contrib.messages.context_processors.messages',
    )

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, '../database/db.sqlite3'),
        }
    }

    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    # --------------------------------------------------
    # logging
    # --------------------------------------------------

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'standard': {
                'format': '[%(asctime)s] [%(levelname)s] [%(name)s:%(lineno)s]: %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
        },
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse',
            }
        },
        'handlers': {
            'cso': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': '../logs/cso.log',
                'maxBytes': 1024 * 1024 * 5,  # 5 MB
                'backupCount': 5,
                'formatter': 'standard',
            },
            'django': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': '../logs/django.log',
                'maxBytes': 1024 * 1024 * 5,  # 5 MB
                'backupCount': 5,
                'formatter': 'standard',
            },
            'django_db': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': '../logs/django_db.log',
                'maxBytes': 1024 * 1024 * 5,  # 5 MB
                'backupCount': 5,
                'formatter': 'standard',
            },
            'others': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': '../logs/others.log',
                'maxBytes': 1024 * 1024 * 5,  # 5 MB
                'backupCount': 5,
                'formatter': 'standard',
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
                'filters': ['require_debug_false'],
            },
        },
        'loggers': {
            'cso': {
                'handlers': ['cso', 'console'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'events': {
                'handlers': ['cso', 'console'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'registration': {
                'handlers': ['cso', 'console'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'django': {
                'handlers': ['django', 'console'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'django.db': {
                'handlers': ['django_db', 'console'],
                'level': 'DEBUG',
                'propagate': False,
            },
            '': {
                'handlers': ['others', 'console'],
                'level': 'DEBUG',
                'propagate': True,
            },
        }
    }

    # --------------------------------------------------
    # stripe
    # --------------------------------------------------

    STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY', 'pk_test_RD2zQX55ntmRV0O4FvnSyZ0M')
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY', 'sk_test_vPjofGnYgo95XmxmI1ZwMvEs')

    # --------------------------------------------------
    # allauth
    # --------------------------------------------------

    INSTALLED_APPS += (
        'allauth',
        'allauth.account',
        'allauth.socialaccount',
        'allauth.socialaccount.providers.facebook',
        'allauth.socialaccount.providers.google',
    )

    AUTHENTICATION_BACKENDS += (
        'allauth.account.auth_backends.AuthenticationBackend',
    )

    TEMPLATE_CONTEXT_PROCESSORS += (
        'django.core.context_processors.request',
        'allauth.account.context_processors.account',
        'allauth.socialaccount.context_processors.socialaccount',
    )

    ACCOUNT_AUTHENTICATION_METHOD = 'email'
    ACCOUNT_EMAIL_REQUIRED = True
    ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
    ACCOUNT_USERNAME_REQUIRED = False
    ACCOUNT_SESSION_REMEMBER = True
    ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'
    ACCOUNT_SIGNUP_FORM_CLASS = 'registration.forms.RegistrationForm'
    # ACCOUNT_USER_DISPLAY = lambda user: user.get_full_name()
    SOCIALACCOUNT_AUTO_SIGNUP = False
    SOCIALACCOUNT_EMAIL_VERIFICATION = None
    SOCIALACCOUNT_PROVIDERS = {'facebook': {'METHOD': 'oauth2', 'VERIFIED_EMAIL': True}}
    SOCIALACCOUNT_ADAPTER = 'cso.adapter.CSOSocialAccountAdapter'

    # --------------------------------------------------
    # front end
    # --------------------------------------------------

    INSTALLED_APPS += (
        'compressor',
        'columns',
        'bootstrap3',
    )

    COMPRESS_PRECOMPILERS = (
        ('text/x-sass', 'django_libsass.SassCompiler'),
        ('text/x-scss', 'django_libsass.SassCompiler'),
    )

    # django messages w/ bootstrap
    from django.contrib import messages

    MESSAGE_TAGS = {messages.ERROR: 'danger'}


class Dev(Base):
    DEBUG = True

    SSLIFY_DISABLE = True

    ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http'

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


class Live(Base):
    DATABASES = {'default': dj_database_url.config()}

    PIWIK_SITE_ID = '2'
    PIWIK_DOMAIN_PATH = 'www.cso.dance/analytics'

    ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'

    COMPRESS_OFFLINE = True

    ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS'] if 'ALLOWED_HOSTS' in os.environ else None
    SECRET_KEY = os.environ['SECRET_KEY'] if 'SECRET_KEY' in os.environ else None

    EMAIL_HOST_USER = os.environ['SENDGRID_USERNAME'] if 'SENDGRID_USERNAME' in os.environ else None
    EMAIL_HOST = 'smtp.sendgrid.net'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_PASSWORD = os.environ['SENDGRID_PASSWORD'] if 'SENDGRID_PASSWORD' in os.environ else None

    LOGGING = Base.LOGGING
    LOGGING['handlers'] = {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'filters': ['require_debug_false'],
        }
    }
    LOGGING['loggers']['cso']['handlers'] = ['console']
    LOGGING['loggers']['events']['handlers'] = ['console']
    LOGGING['loggers']['registration']['handlers'] = ['console']
    LOGGING['loggers']['django']['handlers'] = ['console']
    LOGGING['loggers']['django.db']['handlers'] = ['console']
    LOGGING['loggers']['']['handlers'] = ['console']


class Sandbox(Live):
    PIWIK_SITE_ID = '4'

    SSLIFY_DISABLE = True

    ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http'
