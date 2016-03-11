from django.apps import apps
from django.utils.lru_cache import lru_cache

import storm.menu as m


@lru_cache()
def get_main_menu():
    main_menu = m.Menu('Main menu')
    for app in apps.get_app_configs():
        if hasattr(app, 'main_menu_item'):
            main_menu.add(app.main_menu_item)
    return main_menu


def main_menu(request):
    return {
        'main_menu': get_main_menu(),
    }


def sidebar_menu(request):
    sidebar_menu = m.Menu('Sidebar menu')
    resolver_match = request.resolver_match
    app_name = resolver_match.namespace or resolver_match.url_name
    app_name = app_name.split(':', 1)[0]
    if app_name:
        try:
            app = apps.get_app_config(app_name)
        except LookupError:
            pass
        else:
            sidebar_menu.add_all(getattr(app, 'sidebar_menu_items', []))
    return {
        'sidebar_menu': sidebar_menu
    }
