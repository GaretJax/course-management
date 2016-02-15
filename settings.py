INSTALLED_APPS = []
# TEMPLATE_CONTEXT_PROCESSORS = []
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

# all django settings can be altered here

# INSTALLED_APPS.insert(0, 'suit')
INSTALLED_APPS.extend([
    'menu',
    'education',
    'bootstrap3',
])

# TEMPLATE_CONTEXT_PROCESSORS.extend([])

MIDDLEWARE_CLASSES.extend([])
