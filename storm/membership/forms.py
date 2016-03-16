from django import forms
from django.utils.translation import ugettext_lazy as _

from django_select2 import forms as select2

from storm.commons.forms import LocalizedCountryField, LocalizedCityField
from . import models


class ContactForm(forms.ModelForm):
    nationality = LocalizedCountryField(
        label=_('Nationality'),
        required=False,
    )
    city = LocalizedCityField(
        label=_('City'),
        required=False,
    )
    country = LocalizedCountryField(
        label=_('Country'),
        required=False,
    )

    def clean(self):
        cleaned_data = super(ContactForm, self).clean()

        city, country = cleaned_data['city'], cleaned_data['country']

        if city and not country:
            self.add_error('country', forms.ValidationError(
                _('A country is required when defining a city.'),
                code='required',
            ))
        elif city and city.country != country:
            city_name = LocalizedCityField.label_from_instance(city)
            country_name = LocalizedCountryField.label_from_instance(country)
            self.add_error('city', forms.ValidationError(
                _('%(city)s is not a city in %(country)s.'),
                code='country_mismatch',
                params={'city': city_name, 'country': country_name},
            ))

    class Meta:
        model = models.Contact
        fields = [
            'first_name',
            'last_name',
            'birthday',
            'nationality',
            'gender',
            'address',
            'zip_code',
            'city',
        ]
        widgets = {
            'gender':  select2.Select2Widget(attrs={
                'data-minimum-results-for-search': 'Infinity',
                'data-placeholder': _('Gender'),
            }),
            'address': forms.Textarea(attrs={'rows': 2}),
        }


class AddTypeToPeriodForm(forms.ModelForm):
    def __init__(self, period, *args, **kwargs):
        super(AddTypeToPeriodForm, self).__init__(*args, **kwargs)
        self._period = period

        type_queryset = models.MembershipType.objects.exclude(
            membership_periods__period=period)
        self.fields['type'].queryset = type_queryset
        if type_queryset.exists():
            self.fields['type'].empty_label = None

    def save(self, *args, **kwargs):
        self.instance.period = self._period
        return super(AddTypeToPeriodForm, self).save(*args, **kwargs)

    class Meta:
        model = models.PeriodType
        fields = [
            'type',
            'price'
        ]
