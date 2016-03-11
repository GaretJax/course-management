from storm.menu.views import Group
from . import views


urlpatterns = views.Index.as_url('education', '', [
    views.ListLocations.as_url('locations', 'locations', [
        views.AddLocation.as_url('add'),
        Group(None, '(?P<pk>\d+)', [
            views.EditLocation.as_url('edit'),
            views.DeleteLocation.as_url('delete'),
        ]),
    ]),
    views.ListCourses.as_url('courses', 'courses', [
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
