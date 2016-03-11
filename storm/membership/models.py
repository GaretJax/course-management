from django.db import models


class Contact(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

#    birthday = models.DateField(null=True, blank=True)
#    gender
#    nationality

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


class MembershipType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class MembershipPeriod(models.Model):
    name = models.CharField(max_length=255)
    start = models.DateField()
    end = models.DateField()

    class Meta:
        ordering = ('start', 'end', 'name')

    def __unicode__(self):
        return self.name


class PeriodType(models.Model):
    period = models.ForeignKey(MembershipPeriod, related_name='membership_types')
    type = models.ForeignKey(MembershipType)
    price = models.DecimalField(decimal_places=2, max_digits=7)

    class Meta:
        unique_together = (
            ('period', 'type'),
        )

    def __unicode__(self):
        return u'{} \u2013 {}'.format(self.period, self.type)


class Membership(models.Model):
    contact = models.ForeignKey(Contact)
    membership = models.ForeignKey(PeriodType)

    start = models.DateField(null=True, blank=True)
    end = models.DateField(null=True, blank=True)
