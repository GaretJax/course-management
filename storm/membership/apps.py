from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

import storm.menu as m


class ContactConfig(AppConfig):
    name = 'storm.membership'
    verbose_name = _('Members management')
    main_menu_item = m.Item(_('Members management'), 'membership')
    sidebar_menu_items = [
        m.Item(_('Contacts'), 'membership:contacts'),
        m.Item(_('Membership periods'), 'membership:periods'),
        m.GroupedItems(_('Configuration'), [
            m.Item(_('Membership structure'), 'membership:types'),
        ]),
    ]
