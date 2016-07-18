from django.conf.urls import url

from .views import *

app_name = "footy"
urlpatterns = [
    url(r'^$', ShowGamesView.as_view(), name="show_games"),
    url(r'^new_match/$', CreateEventView.as_view(), name="new_match"),
    url(r'^joined_match/(?P<pk>[0-9]+)/$', JoinMatchView.as_view(), name="join_match"),
    url(r'^my_matches/$', UserMatchesView.as_view(), name="my_matches"),
    url(r'^match/(?P<pk>[0-9]+)/$', ShowEventView.as_view(), name="match"),
    url(r'^profile/(?P<pk>[0-9]+)/$', ProfileView.as_view(), name="profile"),
    url(r'^profile/$', MyProfileView.as_view(), name="my_profile"),
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^signup/$', CreateUserView.as_view(), name="signup"),
]