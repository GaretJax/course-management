from django import forms
from django.utils.translation import get_language

from django_select2 import forms as select2

from cities.models import Country, City


def get_translated_place_name(place):
    name = (place.alt_names
            .filter(is_preferred=True)
            .filter(language=get_language())
            .first())
    return name.name if name else place.name


def get_translated_city_name(city):
    return u'{} ({})'.format(
        get_translated_place_name(city),
        city.country.code,
    )


class HeavySelect2Widget(select2.ModelSelect2Widget):
    def render_options(self, *args):
        """Render only selected options."""
        try:
            selected_choices, = args
        except ValueError:
            choices, selected_choices = args
            from itertools import chain
            choices = chain(self.choices, choices)
        else:
            choices = self.choices
        selected_choices = {v for v in selected_choices if v}

        output = [
            '<option></option>'
            if not (self.is_required or selected_choices) else ''
        ]

        selected_instances = (self.choices.queryset
                              .filter(pk__in=selected_choices)
                              .iterator())

        choices = {self.choices.choice(obj) for obj in selected_instances}

        for option_value, option_label in choices:
            output.append(self.render_option(
                selected_choices,
                option_value,
                option_label,
            ))

        return '\n'.join(output)


class LocalizedPlaceField(forms.ModelChoiceField):
    data_view = None
    model = None

    def __init__(self, **kwargs):
        kwargs.setdefault('queryset', self.model.objects.all())
        kwargs.setdefault('widget', HeavySelect2Widget(
            data_view=self.data_view,
            attrs={
                'data-minimum-input-length': 3,
                'data-ajax--delay': 250,
                'data-placeholder': kwargs.get('label', ''),
            },
            queryset=kwargs['queryset'],
        ))
        super(LocalizedPlaceField, self).__init__(**kwargs)

    @staticmethod
    def label_from_instance(self, obj):
        return get_translated_place_name(obj)


class LocalizedCountryField(LocalizedPlaceField):
    data_view = 'country_autocomplete'
    model = Country


class LocalizedCityField(LocalizedPlaceField):
    data_view = 'city_autocomplete'
    model = City

    @staticmethod
    def label_from_instance(obj):
        return get_translated_city_name(obj)
