from storm.menu.views import Group
from . import views


urlpatterns = views.Index.as_url('membership', '', [
    views.ListContacts.as_url('contacts', 'contacts', [
        views.AddContact.as_url('add'),
        Group(None, '(?P<pk>\d+)', [
            views.EditContact.as_url('edit'),
            views.DeleteContact.as_url('delete'),
        ]),
    ]),
    views.ListMembershipType.as_url('types', 'types', [
        views.AddMembershipType.as_url('add'),
        Group(None, '(?P<pk>\d+)', [
            views.EditMembershipType.as_url('edit'),
            views.DeleteMembershipType.as_url('delete'),
        ]),
    ]),
    views.ListMembershipPeriod.as_url('periods', 'periods', [
        views.AddMembershipPeriod.as_url('add'),
        Group(None, '(?P<period_pk>\d+)', [
            views.MembershipPeriodOverview.as_url('overview'),
            views.MembershipPeriodStructure.as_url('structure', children=[
                views.AddTypeToPeriod.as_url('add'),
                Group(None, '(?P<type_pk>\d+)', [
                    views.EditPeriodType.as_url('edit'),
                    views.DeletePeriodType.as_url('delete'),
                ]),
            ]),
            views.EditMembershipPeriod.as_url('edit'),
            views.DeleteMembershipPeriod.as_url('delete'),
        ]),
    ]),
]).get_urls()
