from six.moves import urllib

import yurl

from django import template

from classytags.core import Tag, Options
from classytags.arguments import Argument, MultiKeywordArgument
from classytags.arguments import MultiValueArgument


register = template.Library()


@register.tag
class AlterUrl(Tag):
    name = 'alter_url'

    options = Options(
        Argument('url', required=False),
        'params',
        MultiKeywordArgument('params', required=False),
        'remove',
        MultiValueArgument('remove', required=False),
    )

    def render_tag(self, context, url, params, remove):
        if url is None:
            url = context['request'].get_full_path()

        url = yurl.URL(url)

        query = urllib.parse.parse_qs(url.query)
        for k in remove:
            query.pop(k, None)
        for k, v in params.items():
            query[k] = [v]
        query = urllib.parse.urlencode(query, doseq=True)

        return str(url.replace(query=query))
