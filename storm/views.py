import os
import json

from django.http import HttpResponse, HttpResponseRedirect


class AjaxMixin(object):
    def _add_suffix(self, path, suffix):
        base, ext = os.path.splitext(path)
        return ''.join([base, suffix, ext])

    def get_template_names(self, **kwargs):
        template_names = super(AjaxMixin, self).get_template_names()
        if self.request.is_ajax():
            template_names = [
                self._add_suffix(t, '_ajax') for t in template_names
            ]
        return template_names

    def dispatch(self, request, *args, **kwargs):
        response = super(AjaxMixin, self).dispatch(
            request, *args, **kwargs)
        if request.is_ajax():
            payload = {
                'status_code': response.status_code,
            }
            if isinstance(response, HttpResponseRedirect):
                payload['location'] = response.url
            else:
                payload['content'] = response.rendered_content
            return HttpResponse(
                json.dumps(payload),
                content_type='application/json',
            )
        return response
