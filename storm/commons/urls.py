from django.conf.urls import url


from . import views

urlpatterns = [
    url(r'^__select2__/countries/',
        views.CountryAutocompleteView.as_view(),
        name='country_autocomplete'),
    url(r'^__select2__/cities/',
        views.CityAutocompleteView.as_view(),
        name='city_autocomplete'),
]
