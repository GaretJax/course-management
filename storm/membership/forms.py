from django import forms

from . import models


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
