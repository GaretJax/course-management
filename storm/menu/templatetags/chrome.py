from django import template
from django.core.urlresolvers import reverse

from classytags.core import Options
from classytags.helpers import InclusionTag
from classytags.arguments import (
    Argument,
    Flag,
    MultiKeywordArgument,
    MultiValueArgument,
)


register = template.Library()


@register.tag
class CellButtonRenderer(InclusionTag):
    template = 'includes/elements/cell_button.html'
    name = 'cell_button'

    options = Options(
        Argument('text'),
        MultiKeywordArgument('options', required=False),
        'url',
        Argument('url_name'),
        MultiKeywordArgument('url_kwargs', required=False),
    )

    def get_context(self, context, text, options, url_name, url_kwargs):
        icon = options.get('icon')
        return {
            'text': text,
            'show_text': not icon or options.get('show_text'),
            'icon': icon,
            'modal': options.get('modal'),
            'url': reverse(url_name, kwargs=url_kwargs),
        }
