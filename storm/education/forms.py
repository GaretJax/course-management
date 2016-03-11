from django import forms
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from . import models


class PaginateByForm(forms.Form):
    paginate_by = forms.ChoiceField()

    def __init__(self, choices, *args, **kwargs):
        super(PaginateByForm, self).__init__(*args, **kwargs)
        self.fields['paginate_by'].choices = [(n, n) for n in choices]


class SessionPlanningForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SessionPlanningForm, self).__init__(*args, **kwargs)
        self.fields['location'].empty_label = _('Use course default')

    class Meta:
        model = models.Session
        fields = [
            'start',
            'end',
            'location',
        ]


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


class _SessionsForm(forms.Form):
    sessions = forms.ModelMultipleChoiceField(queryset=None, required=False)

    def __init__(self, course, *args, **kwargs):
        super(_SessionsForm, self).__init__(*args, **kwargs)
        self.fields['sessions'].queryset = course.sessions


class AttendanceForm(forms.Form):
    def __init__(self, course, data=None, *args, **kwargs):
        super(AttendanceForm, self).__init__(data, *args, **kwargs)
        self.course = course
        if data:
            sessions_form = _SessionsForm(course, data)
            if sessions_form.is_valid():
                self.sessions = sessions_form.cleaned_data['sessions']
            else:
                self.sessions = []

            for s in self.sessions:
                key = 'attendees_{}'.format(s.pk)
                self.fields[key] = forms.ModelMultipleChoiceField(
                    queryset=self.course.registrations,
                    required=False,
                )
                key = 'coaches_{}'.format(s.pk)
                self.fields[key] = forms.ModelMultipleChoiceField(
                    queryset=self.course.coaches,
                    required=False,
                )

    def save_attendances(self, session, user, now, key, model):
        participants = self.cleaned_data['{}_{}'.format(key, session.pk)]
        getattr(session, key).update(
            attended=False,
            filled_at=now,
            filled_by=user,
        )
        for participant in participants:
            attendance, created = model.objects.get_or_create(
                session=session, attendee=participant, defaults={
                    'attended': True,
                    'filled_at': now,
                    'filled_by': user,
                })
            if not created:
                attendance.attended = True
                attendance.filled_at = now
                attendance.filled_by = user
                attendance.save()

    def save(self, user):
        now = timezone.now()
        for session in self.sessions:
            self.save_attendances(session, user, now, 'attendees',
                                  models.Attendance)
            self.save_attendances(session, user, now, 'coaches',
                                  models.SessionCoach)
