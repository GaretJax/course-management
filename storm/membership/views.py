from django.shortcuts import get_object_or_404
from django.views.generic import RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.functional import cached_property
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy

import storm.menu as m
from storm.views import AjaxMixin
from storm.menu.views import UrlMixin

from . import models, forms


period_menu = m.Menu('Period menu')


@method_decorator(login_required, name='dispatch')
class Index(UrlMixin, RedirectView):
    pattern_name = 'membership:contacts'


@method_decorator(login_required, name='dispatch')
class ListContacts(UrlMixin, ListView):
    model = models.Contact


@method_decorator(login_required, name='dispatch')
class AddContact(UrlMixin, CreateView):
    model = models.Contact
    success_url = reverse_lazy('membership:contacts')
    fields = [
        'first_name',
        'last_name',
    ]


@method_decorator(login_required, name='dispatch')
class EditContact(UrlMixin, UpdateView):
    model = models.Contact
    success_url = reverse_lazy('membership:contacts')
    fields = [
        'first_name',
        'last_name',
    ]


@method_decorator(login_required, name='dispatch')
class DeleteContact(UrlMixin, DeleteView):
    model = models.Contact
    success_url = reverse_lazy('membership:contacts')


@method_decorator(login_required, name='dispatch')
class ListMembershipType(UrlMixin, ListView):
    model = models.MembershipType


@method_decorator(login_required, name='dispatch')
class AddMembershipType(UrlMixin, AjaxMixin, CreateView):
    model = models.MembershipType
    success_url = reverse_lazy('membership:types')
    fields = [
        'name',
    ]


@method_decorator(login_required, name='dispatch')
class EditMembershipType(UrlMixin, AjaxMixin, UpdateView):
    model = models.MembershipType
    success_url = reverse_lazy('membership:types')
    fields = [
        'name',
    ]


@method_decorator(login_required, name='dispatch')
class DeleteMembershipType(UrlMixin, AjaxMixin, DeleteView):
    model = models.MembershipType
    success_url = reverse_lazy('membership:types')


@method_decorator(login_required, name='dispatch')
class ListMembershipPeriod(UrlMixin, ListView):
    model = models.MembershipPeriod


@method_decorator(login_required, name='dispatch')
class AddMembershipPeriod(UrlMixin, AjaxMixin, CreateView):
    model = models.MembershipPeriod
    success_url = reverse_lazy('membership:periods')
    fields = [
        'name',
        'start',
        'end',
    ]


class MembershipPeriodObjectMixin(UrlMixin):
    def get_period(self):
        return get_object_or_404(
            models.MembershipPeriod,
            pk=self.kwargs['period_pk'],
        )

    @cached_property
    def period(self):
        return self.get_period()

    def get_context_data(self, **kwargs):
        context = super(MembershipPeriodObjectMixin, self).get_context_data(
            **kwargs)
        context.update({
            'period': self.period,
            'submenu': period_menu,
        })
        return context


@period_menu.item('Overview', 'membership:periods:overview')
@method_decorator(login_required, name='dispatch')
class MembershipPeriodOverview(MembershipPeriodObjectMixin, DetailView):
    template_name = 'membership/membershipperiod_overview.html'

    def get_object(self):
        return self.period


@period_menu.item('Structure', 'membership:periods:structure')
@method_decorator(login_required, name='dispatch')
class MembershipPeriodStructure(MembershipPeriodObjectMixin, ListView):
    template_name = 'membership/membershipperiod_structure.html'

    def get_queryset(self):
        return self.period.membership_types


@period_menu.item('Members', 'membership:periods:members')
@method_decorator(login_required, name='dispatch')
class MembershipPeriodMembers(MembershipPeriodObjectMixin, ListView):
    template_name = 'membership/membershipperiod_members.html'

    def get_queryset(self):
        return models.Membership.objects.filter(membership__period=self.period)


@method_decorator(login_required, name='dispatch')
class AddTypeToPeriod(MembershipPeriodObjectMixin, AjaxMixin, CreateView):
    model = models.PeriodType
    form_class = forms.AddTypeToPeriodForm

    def get_success_url(self):
        return reverse('membership:periods:structure', kwargs={
            'period_pk': self.period.pk,
        })

    def get_form_kwargs(self):
        kwargs = super(AddTypeToPeriod, self).get_form_kwargs()
        kwargs.update({
            'period': self.period,
        })
        return kwargs


@method_decorator(login_required, name='dispatch')
class EditPeriodType(MembershipPeriodObjectMixin, AjaxMixin, UpdateView):
    model = models.PeriodType
    pk_url_kwarg = 'type_pk'
    fields = [
        'price',
    ]

    def get_queryset(self):
        qs = super(EditPeriodType, self).get_queryset()
        return qs.filter(period=self.period)

    def get_success_url(self):
        return reverse('membership:periods:structure', kwargs={
            'period_pk': self.period.pk,
        })


@method_decorator(login_required, name='dispatch')
class DeletePeriodType(MembershipPeriodObjectMixin, AjaxMixin, DeleteView):
    model = models.PeriodType
    pk_url_kwarg = 'type_pk'
    template_name = 'confirm_delete.html'

    def get_queryset(self):
        qs = super(DeletePeriodType, self).get_queryset()
        return qs.filter(period=self.period)

    def get_success_url(self):
        return reverse('membership:periods:structure', kwargs={
            'period_pk': self.period.pk,
        })


@method_decorator(login_required, name='dispatch')
class EditMembershipPeriod(UrlMixin, AjaxMixin, UpdateView):
    model = models.MembershipPeriod
    success_url = reverse_lazy('membership:periods')
    pk_url_kwarg = 'period_pk'
    fields = [
        'name',
        'start',
        'end',
    ]


@method_decorator(login_required, name='dispatch')
class DeleteMembershipPeriod(UrlMixin, AjaxMixin, DeleteView):
    model = models.MembershipPeriod
    pk_url_kwarg = 'period_pk'
    success_url = reverse_lazy('membership:periods')
    template_name = 'confirm_delete.html'
