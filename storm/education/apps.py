from django.apps import AppConfig

import storm.menu as m


class EducationConfig(AppConfig):
    name = 'storm.education'
    verbose_name = 'Education'
    main_menu_item = m.Item('Courses', 'education')
    sidebar_menu_items = [
        m.Item('Courses', 'education:courses'),
        m.Item('Locations', 'education:locations'),
    ]
