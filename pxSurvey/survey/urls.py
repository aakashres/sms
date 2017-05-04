from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),

    url(r'^accounts/login/$', AdminLogInView.as_view(), name='adminLogIn'),
    url(r'^accounts/logout/$', AdminLogOutView.as_view(), name='adminLogOut'),


    url(r'^staff/list/$', StaffListView.as_view(), name='staffList'),
    url(r'^form/list/$', FormEntryListView.as_view(), name='formList'),
    url(r'^staff/create/$',
        StaffCreateView.as_view(), name='staffCreate'),
    url(r'^staff/(?P<pk>\d+)/email-change/$',
        StaffEmailChangeView.as_view(), name='staffEmailChange'),
    url(r'^staff/(?P<pk>\d+)/toggle-group/$',
        StaffToggleGroupView.as_view(), name='staffToggleGroup')
]