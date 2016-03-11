from django.conf.urls import url, include
from django.core.urlresolvers import RegexURLPattern
from django.views.generic.base import View as BaseView


def ensure_view(view):
    if isinstance(view, type) and issubclass(view, BaseView):
        return view.as_view()
    else:
        return view


class View(object):
    def __init__(self, name, segment, view, children=None):
        self.name = name
        self.segment = segment
        self.view = ensure_view(view)
        self.children = children or []

    def get_urls(self):
        self_regex = r'^{}/$'.format(self.segment) if self.segment else r'^$'
        return [
            url(self_regex, self.view, name=self.name),
        ]


class Group(object):
    def __init__(self, name, segment, children):
        self.name = name
        self.segment = segment
        self.children = children

    def get_urls(self):
        child_regex = r'^{}/'.format(self.segment) if self.segment else '^'
        child_urls = []
        for child in self.children:
            if isinstance(child, RegexURLPattern):
                child_urls.append(child)
            else:
                child_urls.extend(child.get_urls())

        return [
            url(child_regex, include(child_urls, namespace=self.name))
        ]


class ViewGroup(Group):
    def __init__(self, name, segment, view, children):
        self.name = name
        self.segment = segment
        self.view = ensure_view(view)
        self.children = children

    def get_urls(self):
        child_regex = r'^{}/'.format(self.segment) if self.segment else '^'
        child_urls = []
        for child in self.children:
            child_urls.extend(child.get_urls())

        if self.name:
            return [
                url(child_regex + '$', self.view, name=self.name),
                url(child_regex, include(child_urls, namespace=self.name))
            ]


class UrlMixin(object):
    @classmethod
    def as_url(cls, name, segment=None, children=None):
        if segment is None:
            segment = name
        if children:
            return ViewGroup(name, segment, cls, children)
        else:
            return View(name, segment, cls)
