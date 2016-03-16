from django.conf.urls import url, include

from aldryn_django.utils import i18n_patterns

import aldryn_addons.urls


urlpatterns = [
    url(r'^__ajax__/select2/', include('django_select2.urls')),
] + aldryn_addons.urls.patterns() + i18n_patterns(
    url('^', include('storm.commons.urls')),
    url('^', include('django.contrib.auth.urls')),
    url('^coaching/', include('storm.education.urls')),
    url('^members/', include('storm.membership.urls')),
    *aldryn_addons.urls.i18n_patterns()  # MUST be the last entry!
)
