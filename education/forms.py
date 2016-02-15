from django import forms

from . import models


class PaginateByForm(forms.Form):
    paginate_by = forms.ChoiceField()

    def __init__(self, choices, *args, **kwargs):
        super(PaginateByForm, self).__init__(*args, **kwargs)
        self.fields['paginate_by'].choices = [(n, n) for n in choices]


class AddParticipantForm(forms.ModelForm):

    def __init__(self, course, *args, **kwargs):
        super(AddParticipantForm, self).__init__(*args, **kwargs)
        self._course = course
        contact_queryset = models.Contact.objects.exclude(
            registrations__course=course)
        self.fields['contact'].queryset = contact_queryset
        if contact_queryset.exists():
            self.fields['contact'].empty_label = None

    def save(self, *args, **kwargs):
        self.instance.course = self._course
        return super(AddParticipantForm, self).save(*args, **kwargs)

    class Meta:
        model = models.Registration
        fields = [
            'contact',
        ]
