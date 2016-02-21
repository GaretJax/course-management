INSTALLED_APPS = []
TEMPLATES = []
TEMPLATE_CONTEXT_PROCESSORS = []
MIDDLEWARE_CLASSES = []

INSTALLED_ADDONS = [
    # <INSTALLED_ADDONS DISABLED>  # Warning: text inside the INSTALLED_ADDONS tags is auto-generated. Manual changes will be overwritten.
    'aldryn-addons',
    'aldryn-django',
    'aldryn-sso',
    # 'aldryn-django-cms',
    'aldryn-devsync',
    # </INSTALLED_ADDONS>
]

import aldryn_addons.settings
aldryn_addons.settings.load(locals())

USE_L10N = False
LANGUAGE_CODE = 'it_CH'

DATETIME_INPUT_FORMATS = [
    '%d/%m/%Y %H:%M',
]

# all django settings can be altered here

# INSTALLED_APPS.insert(0, 'suit')
INSTALLED_APPS.extend([
    'menu',
    'education',
    'bootstrap3',
    'django_gravatar',
])

LOGIN_URL = 'login'

TEMPLATES[0]['OPTIONS']['context_processors'].extend([
    'education.context_processors.version',
])

MIDDLEWARE_CLASSES.extend([])

del TEMPLATE_CONTEXT_PROCESSORS  # Deprecated in django 1.9
