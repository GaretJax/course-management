from django import template

from classytags.core import Tag, Options
from classytags.arguments import Argument, MultiKeywordArgument


register = template.Library()


@register.tag
class MenuRenderer(Tag):
    name = 'menu'

    options = Options(
        Argument('menu'),
    )

    def render_tag(self, context, menu):
        return menu.render(context['request'])


@register.tag
class MenuItemsRenderer(Tag):
    name = 'children'

    options = Options(
        Argument('menu'),
        'with',
        MultiKeywordArgument('kwargs', required=False),
    )

    def render_tag(self, context, menu, kwargs):
        return '\n'.join(
            item.render(context['request'], kwargs=kwargs)
            for item in menu
        )
