from django.apps import AppConfig

import storm.menu as m


class ContactConfig(AppConfig):
    name = 'storm.membership'
    verbose_name = 'Members management'
    main_menu_item = m.Item('Members', 'membership')
    sidebar_menu_items = [
        m.Item('Contacts', 'membership:contacts'),
        m.Item('Membership periods', 'membership:periods'),
        m.GroupedItems('Configuration', [
            m.Item('Membership types', 'membership:types'),
        ]),
    ]
