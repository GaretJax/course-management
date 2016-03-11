import datetime

from django.shortcuts import get_object_or_404
from django.views.generic import RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.edit import ProcessFormView, FormMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.functional import cached_property
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.contrib.auth.decorators import login_required

import storm.menu as m
from storm.menu.views import UrlMixin

from . import models, forms, utils


course_menu = m.Menu('Course menu')


@method_decorator(login_required, name='dispatch')
class Index(UrlMixin, RedirectView):
    pattern_name = 'education:courses'


@method_decorator(login_required, name='dispatch')
class ListLocations(UrlMixin, ListView):
    model = models.Location


@method_decorator(login_required, name='dispatch')
class AddLocation(UrlMixin, CreateView):
    model = models.Location
    success_url = reverse_lazy('education:locations')
    fields = [
        'name',
    ]


@method_decorator(login_required, name='dispatch')
class EditLocation(UrlMixin, UpdateView):
    model = models.Location
    success_url = reverse_lazy('education:locations')
    fields = [
        'name',
    ]


@method_decorator(login_required, name='dispatch')
class DeleteLocation(UrlMixin, DeleteView):
    model = models.Location
    success_url = reverse_lazy('education:locations')


@method_decorator(login_required, name='dispatch')
class ListCourses(UrlMixin, ListView):
    model = models.Course


@method_decorator(login_required, name='dispatch')
class AddCourse(UrlMixin, CreateView):
    model = models.Course
    success_url = reverse_lazy('education:courses')
    fields = [
        'identifier',
        'name',
        'start',
        'end',
        'location',
    ]


class CourseObjectMixin(UrlMixin):
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


@course_menu.item('Overview', 'education:courses:overview')
@method_decorator(login_required, name='dispatch')
class CourseOverview(CourseObjectMixin, DetailView):
    template_name = 'education/course_overview.html'
    model = models.Course

    def get_object(self):
        return self.course


@course_menu.item('Participants management', 'education:courses:participants')
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
        return reverse('education:courses:participants', kwargs={
            'course_pk': self.course.pk,
        })


@method_decorator(login_required, name='dispatch')
class RemoveParticipant(CourseObjectMixin, DeleteView):
    model = models.Registration
    pk_url_kwarg = 'registration_pk'

    def get_success_url(self):
        return reverse('education:courses:participants', kwargs={
            'course_pk': self.course.pk,
        })


@course_menu.item('Sessions planning', 'education:courses:sessions')
@method_decorator(login_required, name='dispatch')
class SessionsPlanning(CourseObjectMixin, ListView):
    def get_queryset(self):
        return self.course.sessions


@method_decorator(login_required, name='dispatch')
class AddSession(CourseObjectMixin, CreateView):
    model = models.Session
    form_class = forms.SessionPlanningForm

    def get_success_url(self):
        return reverse('education:courses:sessions', kwargs={
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

    def get_queryset(self):
        qs = super(EditSession, self).get_queryset()
        return qs.filter(course=self.course)

    def get_success_url(self):
        return reverse('education:courses:sessions', kwargs={
            'course_pk': self.course.pk,
        })


@method_decorator(login_required, name='dispatch')
class DeleteSession(CourseObjectMixin, DeleteView):
    model = models.Session
    pk_url_kwarg = 'session_pk'

    def get_queryset(self):
        qs = super(DeleteSession, self).get_queryset()
        return qs.filter(course=self.course)

    def get_success_url(self):
        return reverse('education:courses:sessions', kwargs={
            'course_pk': self.course.pk,
        })


@course_menu.item('Attendance monitoring', 'education:courses:attendance')
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

    def get_page_for_date(self, queryset, page_size, timestamp=None):
        if timestamp is None:
            timestamp = timezone.now() - datetime.timedelta(days=3)

        objects_before_count = queryset.filter(start__lte=timestamp).count()
        return objects_before_count // page_size + 1

    def paginate_queryset(self, queryset, page_size):
        page_kwarg = self.page_kwarg
        self.kwargs[page_kwarg] = (
            self.kwargs.get(page_kwarg) or
            self.request.GET.get(page_kwarg) or
            self.get_page_for_date(queryset, page_size)
        )
        return super(AttendanceMonitoring, self).paginate_queryset(
            queryset, page_size)

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
            reverse('education:courses:attendance', kwargs={
                'course_pk': self.course.pk,
            }),
        )

    def form_invalid(self, form):
        return self.get(self.request, *self.args, **self.kwargs)

    def form_valid(self, form):
        form.save(self.request.user)
        return super(AttendanceMonitoring, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class EditCourse(UrlMixin, UpdateView):
    model = models.Course
    pk_url_kwarg = 'course_pk'
    success_url = reverse_lazy('education:courses')
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
    success_url = reverse_lazy('education:courses')
