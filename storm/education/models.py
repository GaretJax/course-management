from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.functional import cached_property


from storm.membership.models import Contact


# TODO REFACTOR: The following models should be moved into their own module

class Location(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name


# END REFACTOR


class Teacher(models.Model):
    contact = models.OneToOneField(Contact)


class Course(models.Model):
    identifier = models.SlugField(unique=True, max_length=255)
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=False)
    confirmed = models.BooleanField(default=False)
    start = models.DateField()
    end = models.DateField()
    location = models.ForeignKey(Location)

    def __unicode__(self):
        return '{} ({})'.format(self.name, self.identifier)


class SessionManager(models.Manager):
    use_for_related_fields = True


class Session(models.Model):
    course = models.ForeignKey(Course, related_name='sessions')
    start = models.DateTimeField()
    end = models.DateTimeField()
    location = models.ForeignKey(Location, null=True, blank=True)
    # type

    objects = SessionManager()

    class Meta:
        ordering = ('course', 'start')

    @property
    def actual_location(self):
        return self.location or self.course.location

    @cached_property
    def attendees_pks(self):
        return frozenset(
            self.attendees
            .filter(attended=True)
            .values_list('attendee', flat=True)
        )

    @cached_property
    def coaches_pks(self):
        return frozenset(
            self.coaches
            .filter(attended=True)
            .values_list('attendee', flat=True)
        )


class CourseCoach(models.Model):
    course = models.ForeignKey(Course, related_name='coaches')
    contact = models.ForeignKey(Contact)

    class Meta:
        unique_together = ('course', 'contact')
        verbose_name = 'coach'
        verbose_name_plural = 'coaches'

    def __unicode__(self):
        return '{} / {}'.format(self.course, self.contact)


class Registration(models.Model):
    course = models.ForeignKey(Course, related_name='registrations')
    contact = models.ForeignKey(Contact, related_name='registrations')

    class Meta:
        unique_together = ('course', 'contact')
        ordering = ('contact__first_name', 'contact__last_name')

    def __unicode__(self):
        return '{} / {}'.format(self.course, self.contact)


class AttendanceBase(models.Model):
    filled_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  null=True, blank=True)
    filled_at = models.DateTimeField(default=timezone.now)
    attended = models.BooleanField(default=True)

    class Meta:
        abstract = True


class SessionCoach(AttendanceBase):
    session = models.ForeignKey(Session, related_name='coaches')
    attendee = models.ForeignKey(CourseCoach)

    class Meta:
        unique_together = ('session', 'attendee')


class Attendance(AttendanceBase):
    session = models.ForeignKey(Session, related_name='attendees')
    attendee = models.ForeignKey(Registration)

    class Meta:
        unique_together = ('session', 'attendee')
