from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils import timezone


# TODO REFACTOR: The following models should be moved into their own module

class Location(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class Contact(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
#    title
#    gender
#    birthday
#    address1
#    address2
#    zip
#    city
#    state
#    country
#    phone
#    email

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def __unicode__(self):
        return self.get_full_name()


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

    objects = SessionManager()

    class Meta:
        ordering = ('course', 'start')

    @property
    def actual_location(self):
        return self.location or self.course.location


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


class SessionCoach(models.Model):
    session = models.ForeignKey(Session, related_name='coaches')
    coach = models.ForeignKey(CourseCoach)
    filled_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  null=True, blank=True)
    filled_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('session', 'coach')


class Attendance(models.Model):
    session = models.ForeignKey(Session, related_name='attendees')
    registration = models.ForeignKey(Registration)
    filled_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  null=True, blank=True)
    filled_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('session', 'registration')
