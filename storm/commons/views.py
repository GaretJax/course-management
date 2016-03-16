from django.utils.translation import get_language
from django.http import JsonResponse
from django.views.generic import View
from django.db.models import Q

from cities.models import City, Country, AlternativeName

from .forms import get_translated_place_name, get_translated_city_name


class PlaceAutocompleteView(View):
    min_term_length = 3
    max_results = 50
    model = None

    def get_alt_names(self, term, language):
        filter = {
            'language': language,
            'name__icontains': term,
            '{}__isnull'.format(self.model._meta.model_name): False,
        }
        return AlternativeName.objects.filter(**filter)

    def get_translated_name(self, place):
        return get_translated_place_name(place)

    def get(self, request):
        term = request.GET.get('term', '')
        if len(term) < self.min_term_length:
            return JsonResponse({'results': []})

        names = self.get_alt_names(term, get_language())
        places = self.model.objects.filter(
            Q(alt_names__in=names) |
            Q(name__icontains=term)
        ).distinct()

        results = [
            {'id': place.id, 'text': self.get_translated_name(place)}
            for place in places[:self.max_results].iterator()
        ]

        results = sorted(results, key=lambda p: p['text'])

        return JsonResponse({'results': results})


class CountryAutocompleteView(PlaceAutocompleteView):
    model = Country


class CityAutocompleteView(PlaceAutocompleteView):
    model = City

    def get_translated_name(self, place):
        return get_translated_city_name(place)
