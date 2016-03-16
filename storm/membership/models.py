from django.db import models
from django.utils.translation import ugettext_lazy as _, pgettext_lazy

from cities.models import Country, City


class Contact(models.Model):
    UNKNOWN, MALE, FEMALE = None, True, False
    GENDER_CHOICES = (
        (MALE, _('Male')),
        (FEMALE, _('Female')),
    )

    first_name = models.CharField(_('first name'), max_length=255)
    last_name = models.CharField(_('last name'), max_length=255)

    # Personal data
    birthday = models.DateField(_('birthday'), null=True, blank=True)
    nationality = models.ForeignKey(
        Country, models.SET_NULL,
        verbose_name=_('nationality'),
        null=True, blank=True,
        related_name='+',
    )
    gender = models.NullBooleanField(_('gender'), choices=GENDER_CHOICES)

    # Address
    address = models.TextField(_('address'), blank=True)
    zip_code = models.CharField(_('ZIP code'), max_length=16, blank=True)
    city = models.ForeignKey(
        City, models.SET_NULL,
        verbose_name=_('city'),
        null=True, blank=True,
        related_name='+',
    )

#    phone
#    mobile
#    email

    class Meta:
        ordering = ('last_name', 'first_name')

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def __unicode__(self):
        return self.get_full_name()


class MembershipType(models.Model):
    name = models.CharField(
        pgettext_lazy('membership type', 'label'),
        max_length=255,
    )

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class MembershipPeriod(models.Model):
    name = models.CharField(
        pgettext_lazy('membership period', 'label'),
        max_length=255,
    )
    start = models.DateField(_('start'))
    end = models.DateField(_('end'))

    class Meta:
        ordering = ('start', 'end', 'name')

    def __unicode__(self):
        return self.name


class PeriodType(models.Model):
    period = models.ForeignKey(
        MembershipPeriod,
        related_name='membership_types',
    )
    type = models.ForeignKey(
        MembershipType,
        related_name='membership_periods',
    )
    price = models.DecimalField(decimal_places=2, max_digits=7)

    class Meta:
        unique_together = (
            ('period', 'type'),
        )

    def __unicode__(self):
        return u'{} \u2013 {}'.format(self.period, self.type)


class Membership(models.Model):
    contact = models.ForeignKey(Contact)
    membership = models.ForeignKey(PeriodType, related_name='memberships')

    start = models.DateField(null=True, blank=True)
    end = models.DateField(null=True, blank=True)
