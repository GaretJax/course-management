from django.conf.urls import url, include
from django.core.urlresolvers import RegexURLPattern
from django.views.generic.base import View as BaseView

from education import views


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


urlpatterns = Group(None, '', [
    url(r'^$', views.index, name='index'),
    views.ListLocations.as_url('location', 'locations', [
        views.AddLocation.as_url('add'),
        Group(None, '(?P<pk>\d+)', [
            views.EditLocation.as_url('edit'),
            views.DeleteLocation.as_url('delete'),
        ]),
    ]),
    views.ListCourses.as_url('course', 'courses', [
        views.AddCourse.as_url('add'),
        Group(None, '(?P<course_pk>\d+)', [
            views.CourseOverview.as_url('overview'),
            views.ParticipantsManagement.as_url('participants', children=[
                views.AddParticipant.as_url('add'),
                Group(None, '(?P<registration_pk>\d+)', [
                    views.RemoveParticipant.as_url('remove'),
                ]),
            ]),
            views.SessionsPlanning.as_url('sessions', children=[
                views.AddSession.as_url('add'),
                Group(None, '(?P<session_pk>\d+)', [
                    views.EditSession.as_url('edit'),
                    views.DeleteSession.as_url('delete'),
                ]),
            ]),
            views.AttendanceMonitoring.as_url('attendance'),
            views.EditCourse.as_url('edit'),
            views.DeleteCourse.as_url('delete'),
        ]),
    ]),
]).get_urls()
