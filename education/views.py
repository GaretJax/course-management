from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.edit import ProcessFormView, FormMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.functional import cached_property
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

import menu as m

from . import models, forms, utils


sidebar_menu = m.Menu('Sidebar menu')
sidebar_menu.add_all([
    m.Item('Locations', 'education:location'),
    m.Item('Courses', 'education:course'),
])

main_menu = m.Menu('Main menu')
main_menu.add_all([
    # m.Item('Customers', 'education:index'),
    m.Item('Courses', 'education:course'),
    # m.Item('Collaborators', 'education:index'),
])


course_menu = m.Menu('Course menu')


@login_required
def index(request):
    return render(request, 'education/index.html', {
        'main_menu': main_menu,
    })


class UrlMixin(object):
    @classmethod
    def as_url(cls, name, segment=None, children=None):
        if segment is None:
            segment = name
        from education.urls import View, ViewGroup
        if children:
            return ViewGroup(name, segment, cls, children)
        else:
            return View(name, segment, cls)


class MenuMixin(UrlMixin):
    def get_context_data(self, **kwargs):
        context = super(MenuMixin, self).get_context_data(**kwargs)
        context.update({
            'main_menu': main_menu,
            'sidebar_menu': sidebar_menu,
        })
        return context


@method_decorator(login_required, name='dispatch')
class ListLocations(MenuMixin, ListView):
    model = models.Location


@method_decorator(login_required, name='dispatch')
class AddLocation(MenuMixin, CreateView):
    model = models.Location
    success_url = reverse_lazy('education:location')
    fields = [
        'name',
    ]


@method_decorator(login_required, name='dispatch')
class EditLocation(MenuMixin, UpdateView):
    model = models.Location
    success_url = reverse_lazy('education:location')
    fields = [
        'name',
    ]


@method_decorator(login_required, name='dispatch')
class DeleteLocation(MenuMixin, DeleteView):
    model = models.Location
    success_url = reverse_lazy('education:location')


@method_decorator(login_required, name='dispatch')
class ListCourses(MenuMixin, ListView):
    model = models.Course


@method_decorator(login_required, name='dispatch')
class AddCourse(MenuMixin, CreateView):
    model = models.Course
    success_url = reverse_lazy('education:course')
    fields = [
        'identifier',
        'name',
        'start',
        'end',
        'location',
    ]


class CourseObjectMixin(MenuMixin):
    def get_course(self):
        return get_object_or_404(models.Course, pk=self.kwargs['course_pk'])

    @cached_property
    def course(self):
        return self.get_course()

    def get_context_data(self, **kwargs):
        context = super(CourseObjectMixin, self).get_context_data(**kwargs)
        context.update({
            'course': self.course,
            'course_menu': course_menu,
        })
        return context


@course_menu.item('Overview', 'education:course:overview')
@method_decorator(login_required, name='dispatch')
class CourseOverview(CourseObjectMixin, DetailView):
    template_name = 'education/course_overview.html'
    model = models.Course

    def get_object(self):
        return self.course


@course_menu.item('Participants management', 'education:course:participants')
@method_decorator(login_required, name='dispatch')
class ParticipantsManagement(CourseObjectMixin, ListView):
    def get_queryset(self):
        return self.course.registrations


@method_decorator(login_required, name='dispatch')
class AddParticipant(CourseObjectMixin, CreateView):
    model = models.Registration
    form_class = forms.AddParticipantForm

    def get_form_kwargs(self):
        kwargs = super(AddParticipant, self).get_form_kwargs()
        kwargs.update({
            'course': self.course,
        })
        return kwargs

    def get_success_url(self):
        return reverse('education:course:participants', kwargs={
            'course_pk': self.course.pk,
        })


@method_decorator(login_required, name='dispatch')
class RemoveParticipant(CourseObjectMixin, DeleteView):
    model = models.Registration
    pk_url_kwarg = 'registration_pk'

    def get_success_url(self):
        return reverse('education:course:participants', kwargs={
            'course_pk': self.course.pk,
        })


@course_menu.item('Sessions planning', 'education:course:sessions')
@method_decorator(login_required, name='dispatch')
class SessionsPlanning(CourseObjectMixin, ListView):
    def get_queryset(self):
        return self.course.sessions


@method_decorator(login_required, name='dispatch')
class AddSession(CourseObjectMixin, CreateView):
    model = models.Session
    form_class = forms.SessionPlanningForm

    def get_success_url(self):
        return reverse('education:course:sessions', kwargs={
            'course_pk': self.course.pk,
        })

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        form.instance.course = self.course
        return super(AddSession, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class EditSession(CourseObjectMixin, UpdateView):
    model = models.Session
    pk_url_kwarg = 'session_pk'
    form_class = forms.SessionPlanningForm

    def get_success_url(self):
        return reverse('education:course:sessions', kwargs={
            'course_pk': self.course.pk,
        })


@method_decorator(login_required, name='dispatch')
class DeleteSession(CourseObjectMixin, DeleteView):
    model = models.Session
    pk_url_kwarg = 'session_pk'

    def get_success_url(self):
        return reverse('education:course:sessions', kwargs={
            'course_pk': self.course.pk,
        })


@course_menu.item('Attendance monitoring', 'education:course:attendance')
@method_decorator(login_required, name='dispatch')
class AttendanceMonitoring(CourseObjectMixin, FormMixin,
                           ProcessFormView, ListView):
    template_name = 'education/course_attendance.html'
    model = models.Session
    paginate_by = 5
    paginate_by_choices = [3, 5, 8, 10, 15]
    form_class = forms.AttendanceForm

    def get_form_kwargs(self):
        kwargs = super(AttendanceMonitoring, self).get_form_kwargs()
        kwargs.update({
            'course': self.course,
        })
        return kwargs

    def get(self, *args, **kwargs):
        return super(ProcessFormView, self).get(*args, **kwargs)

    def get_queryset(self):
        return self.course.sessions.all()

    def get_paginate_by(self, queryset=None):
        paginate_by_form = forms.PaginateByForm(
            choices=self.paginate_by_choices,
            data=self.request.GET,
            initial={'paginate_by': self.paginate_by},
        )
        if paginate_by_form.is_valid():
            return int(paginate_by_form.cleaned_data['paginate_by'])
        else:
            return self.paginate_by

    def get_context_data(self, **kwargs):
        context = super(AttendanceMonitoring, self).get_context_data(**kwargs)
        context.update({
            'paginate_by_form': forms.PaginateByForm(
                self.paginate_by_choices,
                initial={'paginate_by': self.get_paginate_by()},
            ),
            'participant_list': self.course.registrations.all(),
            'coach_list': self.course.coaches.all(),
        })
        return context

    def get_success_url(self):
        return utils.preserve_request_params(
            self.request,
            reverse('education:course:attendance', kwargs={
                'course_pk': self.course.pk,
            }),
        )

    def form_invalid(self, form):
        return self.get(self.request, *self.args, **self.kwargs)

    def form_valid(self, form):
        form.save(self.request.user)
        return super(AttendanceMonitoring, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class EditCourse(MenuMixin, UpdateView):
    model = models.Course
    pk_url_kwarg = 'course_pk'
    success_url = reverse_lazy('education:course')
    fields = [
        'name',
        'start',
        'end',
        'location',
        'active',
        'confirmed',
    ]


@method_decorator(login_required, name='dispatch')
class DeleteCourse(CourseObjectMixin, DeleteView):
    success_url = reverse_lazy('education:course')
