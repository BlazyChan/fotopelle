"""
Django iestatījumi projektam "fotopelle".
Koda ģenerēšanai tika izmantots Django 4.0.4.

https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path

# Ceļus uz failiem projektā var veidot izmantojot: BASE_DIR / 'apakšdirektorija'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Informāciju par iestatījumiem priekš ražošanas (production) režīma var atrast te:
# https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# DROŠĪBAS BRĪDINĀJUMS: ražošanas (production) režīmā šai atslēgai jābūt slepanai!
SECRET_KEY = 'django-insecure-!d90xqu7z#-u=bs1ugn#k#=u2+)nm1raochvh2@@fcn#(-xi+r'

# DROŠĪBAS BRĪDINĀJUMS: ražošanas (production) režīmā atkļūdošanai (debug) jābūt izslēgtam!
DEBUG = True

ALLOWED_HOSTS = []


# Lietojumprogrammas definīcija:

INSTALLED_APPS = [
    # Django lietotnes:
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Paštaisītās lietotnes:
    'pakalpojumi',
    'lietotaji',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'fotopelle.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'fotopelle.wsgi.application'


# Datubāzes iestatījumi:
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Paroles validācija:
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internacionalizācija:
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'lv-lav'

TIME_ZONE = 'Europe/Riga'

USE_I18N = True

USE_TZ = True


# Statiskie faili (CSS, JavaScript, Bildes):
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Papildus vietas statiskajiem failiem, kuras projektā tiek izmantotas:
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Vieta lietotāja augšupielādētajiem failiem:
MEDIA_ROOT = BASE_DIR / 'media/'

# Noklusētais primāro atslēgu lauku veids:
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Lietotāja modelis:
AUTH_USER_MODEL = 'lietotaji.Lietotajs'
