from django.template.loader import render_to_string
from django.core.urlresolvers import reverse


class Menu(object):
    def __init__(self, label, template='menu/menu.html'):
        self.label = label
        self.template = template
        self._items = []

    def add(self, item):
        self._items.append(item)

    def add_all(self, items):
        self._items.extend(items)

    def add_grouped(self, label, items):
        self._items.append(GroupedItems(label, items))

    def item(self, *args, **kwargs):
        def register_item(view):
            return self.add_view(view, *args, **kwargs)
        return register_item

    def add_view(self, view, *args, **kwargs):
        self.add(Item(*args, **kwargs))
        return view

    def __iter__(self):
        for item in self._items:
            yield item

    def render(self, request):
        return render_to_string(self.template, request=request, context={
            'menu': self,
        })


class RawItem(object):
    def __init__(self, label, url, template='menu/item.html'):
        self.label = label
        self.template = template
        self._url = url

    def get_url(self, request, **kwargs):
        if callable(self._url):
            return self._url()
        else:
            return self._url

    def is_active(self, request):
        return False

    def render(self, request, **kwargs):
        return render_to_string(self.template, request=request, context={
            'item': self,
            'url': self.get_url(request, **kwargs),
            'is_active': self.is_active(request),
            'is_parent': self.is_parent(request),
        })

    def __repr__(self):
        return 'Item({!r})'.format(self._url)


class Item(RawItem):
    def get_url(self, request, **kwargs):
        return reverse(self._url, kwargs=kwargs.get('kwargs', {}))

    def is_parent(self, request):
        item_chunks = self._url.split(':')
        current_chunks = request.resolver_match.view_name.split(':')
        return current_chunks[:len(item_chunks)] == item_chunks

    def is_active(self, request):
        return request.resolver_match.view_name == self._url


class GroupedItems(object):
    def __init__(self, label, items=None, template='menu/group.html'):
        self.label = label
        self.template = template
        self._items = items if items else []

    def add(self, item):
        self._items.append(item)

    def __iter__(self):
        for item in self._items:
            yield item

    def render(self, request):
        return render_to_string(self.template, request=request, context={
            'items': self,
        })
