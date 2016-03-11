from django.contrib import admin
from django.forms import ModelForm

from suit.widgets import SuitDateWidget, SuitSplitDateTimeWidget

from . import models


class CourseChangeForm(ModelForm):
    class Meta:
        model = models.Course
        exclude = []
        widgets = {
            'start': SuitDateWidget,
            'end': SuitDateWidget,
        }


class SessionChangeForm(ModelForm):
    class Meta:
        model = models.Session
        exclude = []
        widgets = {
            'start': SuitSplitDateTimeWidget,
            'end': SuitSplitDateTimeWidget,
        }


class SessionCoachChangeForm(ModelForm):
    class Meta:
        model = models.SessionCoach
        exclude = []
        widgets = {
            'filled_at': SuitSplitDateTimeWidget,
        }


class AttendanceChangeForm(ModelForm):
    class Meta:
        model = models.Attendance
        exclude = []
        widgets = {
            'filled_at': SuitSplitDateTimeWidget,
        }


class LocationAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Location, LocationAdmin)


class SessionInline(admin.TabularInline):
    model = models.Session
    form = SessionChangeForm
    suit_classes = 'suit-tab suit-tab-dates'


class CourseCoachInline(admin.TabularInline):
    model = models.CourseCoach
    suit_classes = 'suit-tab suit-tab-general'


class RegistrationInline(admin.TabularInline):
    model = models.Registration
    suit_classes = 'suit-tab suit-tab-registrations'


class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'identifier',
        'name',
        'start',
        'end',
        'location',
        'active',
        'confirmed',
        'sessions_count',
        'participants_count'
    )
    form = CourseChangeForm
    inlines = [
        CourseCoachInline,
        SessionInline,
        RegistrationInline,
    ]
    suit_form_tabs = (
        ('general', 'General'),
        ('dates', 'Dates'),
        ('registrations', 'Registrations'),
    )
    fieldsets = [
        (None, {
            'classes': ('suit-tab', 'suit-tab-general',),
            'fields': [
                'identifier',
                'name',
                'start',
                'end',
                'location',
                'active',
                'confirmed',
            ],
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-dates',),
            'fields': [],
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-registrations',),
            'fields': [],
        }),
    ]

    def sessions_count(self, obj):
        return obj.sessions.count()
    sessions_count.short_description = 'sessions'

    def participants_count(self, obj):
        return obj.registrations.count()
    participants_count.short_description = 'participants'
admin.site.register(models.Course, CourseAdmin)


class SessionCoachInline(admin.TabularInline):
    model = models.SessionCoach
    form = SessionCoachChangeForm
    suit_classes = 'suit-tab suit-tab-attendances'


class AttendanceInline(admin.TabularInline):
    model = models.Attendance
    form = AttendanceChangeForm
    suit_classes = 'suit-tab suit-tab-attendances'


class SessionAdmin(admin.ModelAdmin):
    list_display = (
        'course',
        'actual_location',
        'start',
        'end',
        'attendees_count'
    )
    form = SessionChangeForm
    inlines = [
        SessionCoachInline,
        AttendanceInline,
    ]
    suit_form_tabs = (
        ('general', 'General'),
        ('attendances', 'Attendances'),
    )
    fieldsets = [
        (None, {
            'classes': ('suit-tab', 'suit-tab-general',),
            'fields': [
                'start',
                'end',
                'location',
            ],
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-attendances',),
            'fields': [],
        }),
    ]

    def attendees_count(self, obj):
        return '{}/{}'.format(
            obj.attendees.filter(attended=True).count(),
            obj.course.registrations.count(),
        )
    attendees_count.short_description = 'attendees'
admin.site.register(models.Session, SessionAdmin)
