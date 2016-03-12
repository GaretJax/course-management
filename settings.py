INSTALLED_APPS = []
TEMPLATES = []
TEMPLATE_CONTEXT_PROCESSORS = []
MIDDLEWARE_CLASSES = []
DATABASES = {}

INSTALLED_ADDONS = [
    # <INSTALLED_ADDONS DISABLED>  # Warning: text inside the INSTALLED_ADDONS tags is auto-generated. Manual changes will be overwritten.
    'aldryn-addons',
    'aldryn-django',
    'aldryn-sso',
    #'aldryn-django-cms',
    'aldryn-devsync',
    # </INSTALLED_ADDONS>
]

import aldryn_addons.settings
aldryn_addons.settings.load(locals())

USE_L10N = False
LANGUAGE_CODE = 'it'

DATETIME_INPUT_FORMATS = [
    '%d/%m/%Y %H:%M',
]
DATE_INPUT_FORMATS = [
    '%d/%m/%Y',
]

# all django settings can be altered here

# INSTALLED_APPS.insert(0, 'suit')
INSTALLED_APPS.extend([
    'django.contrib.gis',
    'storm.menu',
    'storm.membership.apps.ContactConfig',
    'storm.education.apps.EducationConfig',
    'bootstrap3',
    'django_gravatar',
    'cities',
])

ROOT_URLCONF = 'storm.urls'

WSGI_APPLICATION = 'storm.wsgi.application'

LOGIN_URL = 'login'

TEMPLATES[0]['OPTIONS']['context_processors'].extend([
    'storm.context_processors.version',
    'storm.menu.context_processors.main_menu',
    'storm.menu.context_processors.sidebar_menu',
])

MIDDLEWARE_CLASSES.extend([])

del TEMPLATE_CONTEXT_PROCESSORS  # Deprecated in django 1.9


DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'

# django-cities config
CITIES_LOCALES = ['und', 'LANGUAGES']
CITIES_POSTAL_CODES = ['CH', 'IT', 'DE', 'FR']
CITIES_IGNORE_EMPTY_REGIONS = True
CITIES_FILES = {
    'city': {
       'filenames': ['CH.zip', 'IT.zip', 'DE.zip', 'FR.zip'],
    },
}
