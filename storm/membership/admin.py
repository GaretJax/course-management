from django.contrib import admin

from . import models


class ContactAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Contact, ContactAdmin)


class MembershipTypeAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.MembershipType, MembershipTypeAdmin)


class MembershipPeriodAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.MembershipPeriod, MembershipPeriodAdmin)


class MembershipAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Membership, MembershipAdmin)
