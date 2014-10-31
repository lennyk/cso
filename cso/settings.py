import os
from configurations import Configuration


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
    STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, '../static'))
    STATICFILES_DIRS = (
        os.path.abspath(os.path.join(BASE_DIR, '../bower_components')),
    )

    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.abspath(os.path.join(BASE_DIR, '../media'))

    ROOT_URLCONF = 'cso.urls'

    WSGI_APPLICATION = 'cso.wsgi.application'

    SITE_ID = 2

    LOGIN_REDIRECT_URL = '/registration/'

    AUTH_USER_MODEL = 'cso.CSOUser'

    INSTALLED_APPS = (
        'django_admin_bootstrapped.bootstrap3',
        'django_admin_bootstrapped',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.sites',
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
    )

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, '../database/db.sqlite3'),
        }
    }

    # --------------------------------------------------
    # pipeline
    # --------------------------------------------------

    INSTALLED_APPS += (
        'pipeline',
    )

    MIDDLEWARE_CLASSES += (
        'pipeline.middleware.MinifyHTMLMiddleware',
    )

    STATICFILES_FINDERS = (
        'pipeline.finders.FileSystemFinder',
        'pipeline.finders.AppDirectoriesFinder',
        'pipeline.finders.PipelineFinder',
        'pipeline.finders.CachedFileFinder',
    )

    STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

    PIPELINE_COMPILERS = (
        'pipeline.compilers.sass.SASSCompiler',
    )

    PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.yuglify.YuglifyCompressor'
    PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.yuglify.YuglifyCompressor'
    PIPELINE_YUGLIFY_BINARY = os.path.abspath(os.path.join(BASE_DIR, '../node_modules/yuglify/bin/yuglify'))

    PIPELINE_JS = {
        'vendor': {
            'source_filenames': (
                'jquery/dist/jquery.js',
                'bootstrap-sass-official/assets/javascripts/bootstrap.js',  # TODO: use individual components instead
            ),
            'output_filename': 'js/vendor.js',
        },
        'cso': {
            'source_filenames': (
                'base.js',
            ),
            'output_filename': 'js/cso.js',
        },
        'home': {
            'source_filenames': (
                'home.js',
            ),
            'output_filename': 'js/home.js',
        },
        'registration': {
            'source_filenames': (
                'registration.js',
            ),
            'output_filename': 'js/registration.js',
        },
    }

    PIPELINE_CSS = {
        'vendor': {
            'source_filenames': (
                'bootstrap_custom.sass',
                'font-awesome/scss/font-awesome.scss',
                'bootstrap-social/bootstrap-social.scss',
            ),
            'output_filename': 'css/vendor.css',
        },
        'cso': {
            'source_filenames': {
                'base.css',
            },
            'output_filename': 'css/cso.css',
        },
        'home': {
            'source_filenames': {
                'home.css',
            },
            'output_filename': 'css/home.css',
        },
        'registration': {
            'source_filenames': {
                'registration.css',
            },
            'output_filename': 'css/registration.css',
        },
    }

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
        'bootstrap3',
    )

    # django messages w/ bootstrap
    from django.contrib import messages

    MESSAGE_TAGS = {messages.ERROR: 'danger'}


class Dev(Base):
    DEBUG = True

    SOCIAL_AUTH_FACEBOOK_KEY = '1522981811246933'
    SOCIAL_AUTH_FACEBOOK_SECRET = 'aed08816076d87b3c0ce13d8f3906fd1'

    ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http'

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


class Sandbox(Base):
    SOCIAL_AUTH_FACEBOOK_KEY = '1522982181246896'
    SOCIAL_AUTH_FACEBOOK_SECRET = 'cf50b5154294cda7bd6e1a43f8a4104f'
    # from instance_settings import ALLOWED_HOSTS, SECRET_KEY


class Live(Base):
    SOCIAL_AUTH_FACEBOOK_KEY = '1522387657973015'
    SOCIAL_AUTH_FACEBOOK_SECRET = '8d2a32053ea6d493b2c3130d20137178'
    # from instance_settings import ALLOWED_HOSTS, SECRET_KEY
