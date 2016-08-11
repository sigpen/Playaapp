from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point, GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.utils.encoding import escape_uri_path
from django.views.generic import ListView, CreateView, FormView, DetailView, UpdateView, DeleteView
from django.views.generic.base import View
from footy.forms import UserForm, LoginForm, EventForm, LocationForm
from footy.models import Event, UserProfile, Location
from . import models


# Validating user's username and password
class LoginView(FormView):
    form_class = LoginForm
    template_name = "login.html"
    page_title = "Login"

    # Checks if user is already logged in
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('footy:show_matches')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

        if user is not None and user.is_active:
            login(self.request, user)
            if self.request.GET.get('from'):
                return redirect(
                    self.request.GET['from'])  # SECURITY: check path
            return redirect('footy:show_matches')

        # Returns an error if authentication failed
        form.add_error(None, "Invalid user name or password")
        return self.form_invalid(form)


# User Logout
class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('footy:login'))


# Checks if user is already logged in, and redirects the former page
class LoggedInMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            url = reverse("footy:login") + "?from=" + escape_uri_path(request.path)
            return redirect(url)
        return super().dispatch(request, *args, **kwargs)


# Presenting close matches via list
class ShowMatchesView(LoggedInMixin, ListView):
    model = Event
    template_name = "index.html"
    page_title = "Games"

    def get_object(self):
        user = self.request.user.profile
        ev = Event.objects.get(pk=self.kwargs['pk'])
        ev.users.add(user)

    # GET latitude and longitude parameters and return filtered by distance results
    def get_queryset(self):
        if (self.request.GET):
            lat = self.request.GET['lat']
            lng = self.request.GET['lng']
        else:
            lat = 32.0777
            lng = 34.7805
        origin = GEOSGeometry('POINT({} {})'.format(lng, lat), srid=4326)
        qs = Event.objects.filter(location__point__distance_lte=(origin, D(km=100))) \
            .annotate(distance=Distance('location__point', origin)).order_by('distance')
        return qs


# Sign up view
class CreateUserView(CreateView):
    model = User
    form_class = UserForm
    template_name = "signup.html"
    page_title = "Sign Up"

    success_url = reverse_lazy('footy:show_matches')

    # Creates User & UserProfile objects and logging in
    def form_valid(self, form):
        resp = super().form_valid(form)
        models.UserProfile.objects.create(
            user=form.instance,
            phone_number=form.cleaned_data['phone_number']
        )
        if form.is_valid():
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password'],
                                    )
            login(self.request, new_user)
        return resp


# Creates a new match form
class CreateEventView(LoggedInMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = "new_match.html"
    page_title = "Create A New Match"

    success_url = reverse_lazy('footy:show_matches')


# Presents nearby matches using a map
class NearByMatchesView(LoggedInMixin, ListView):
    model = Event
    template_name = "nearby_matches.html"
    page_title = "Nearby Games"

    def get_queryset(self):
        if (self.request.GET):
            lat = self.request.GET['lat']
            lng = self.request.GET['lng']
        else:
            lat = 32.0777
            lng = 34.7805
        origin = GEOSGeometry('POINT({} {})'.format(lng, lat), srid=4326)
        qs = Event.objects.filter(location__point__distance_lte=(origin, D(km=100))) \
            .annotate(distance=Distance('location__point', origin)).order_by('distance')
        return qs


# Presents current user profile data
class MyProfileView(LoggedInMixin, DetailView):
    model = UserProfile
    template_name = "profile.html"
    page_title = "Profile"

    def get_object(self, queryset=None):
        return self.request.user.profile


# Presents any user profile using it's pk as a parameter
class ProfileView(LoggedInMixin, DetailView):
    model = UserProfile
    template_name = "profile.html"
    page_title = "Profile"

    def get_object(self, queryset=None):
        return get_object_or_404(UserProfile, pk=self.kwargs.get('pk'))


# Current user's matches
class UserMatchesView(LoggedInMixin, ListView):
    model = Event
    template_name = "mymatches.html"
    page_title = "My Matches"

    def get_queryset(self):
        return Event.objects.filter(users=self.request.user.profile)


# TODO: redirect to index after joining a match
# Adds current user to a match and presents nearby matches
class JoinMatchView(LoggedInMixin, UpdateView):
    model = Event
    template_name = "match.html"
    page_title = "Thanks for joining!"

    fields = ['users']

    # Get current user's object and add to the match's player list
    def get_object(self, queryset=None):
        user = self.request.user.profile
        ev = Event.objects.get(pk=self.kwargs['pk'])
        ev.users.add(user)
        return ev


# TODO: redirect to index after joining a match
# Deletes current user from a match and presents nearby matches
class LeaveMatchView(LoggedInMixin, DeleteView):
    model = Event
    template_name = "match.html"

    fields = ['users']

    # Get current user's object and remove from the Match's player list
    def get_object(self, queryset=None):
        user = self.request.user.profile
        ev = Event.objects.get(pk=self.kwargs['pk'])
        ev.users.remove(user)
        return ev


class AddLocationView(LoggedInMixin, CreateView):
    model = Location
    template_name = "add_location.html"
    page_title = "New Location"

    form_class = LocationForm
    success_url = reverse_lazy('footy:new_match')
