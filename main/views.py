from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView as BaseLoginView, PasswordResetView as BasePasswordResetView,
    PasswordResetConfirmView as BasePasswordResetConfirmView
)
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.files.base import ContentFile
from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (
    CreateView, DeleteView, FormView, ListView, TemplateView, UpdateView, View
)

from honeypot.decorators import check_honeypot
from registration import signals
from registration.backends.hmac.views import ActivationView, RegistrationView
from tablib import Dataset

from .forms import (
    UserActivationForm, UserAuthenticationForm, UserRegistrationForm,
    PasswordResetForm, SetPasswordForm, AnswerFormSet, AnswerFormSetHelper,
    AnswerChoiceFormset, UserGeoKeyForm, EmailGeoKeyForm, MobileGeoKeyForm
)
from .models import UserGeoKey, UserProfile


User = get_user_model()

# #############################
#  Authentication views      #
##############################


class LoginView(SuccessMessageMixin, BaseLoginView):
    '''
    Handles user sign in. On successful signing in a user is redirect to
    his/her homepage
    '''

    form_class = UserAuthenticationForm

    def get(self, request, *args, **kwargs):
        # Redirect users already logged in to their homepage
        if request.user.is_authenticated():
            if 'next' in request.GET:
                return redirect(request.GET['next'])
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super(LoginView, self).get(request, *args, **kwargs)

    def get_success_message(self, cleaned_data):
        name = self.request.user.last_name or self.request.user.username
        return "Welcome {}.".format(name)


class PasswordResetView(BasePasswordResetView):
    '''
    Handle password resets for users who have forgotten their passwords.
    On correctly answering two of the three questions they answered when
    signing up send them an email with a one time link to reset their password.
    '''

    form_class = PasswordResetForm
    email_template_name = 'registration/password_reset_email.txt'

    def get_context_data(self, **kwargs):
        context = super(PasswordResetView, self).get_context_data(**kwargs)
        return context

    @method_decorator(check_honeypot)
    def post(self, request, *args, **kwargs):
        form = PasswordResetForm(request.POST)
        if not form.is_valid():
            context = {
                'form': self.get_form(),
            }
            return render(request, self.template_name, context)

        email = form.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
        except (User.DoesNotExist):
            return render(request, self.template_name, {'form': self.get_form()})
        return self.form_valid(form)


class PasswordResetConfirmView(BasePasswordResetConfirmView):

    '''
    Allows user to change their password after requesting a password reset.
    '''

    form_class = SetPasswordForm


class UserRegistrationView(RegistrationView):
    '''
    Initial step for user registration. User gives their email and a one time
    account activation link is sent to this mail address.
    An inactive account is also created for the user.
    '''

    email_body_template = 'registration/activation_email.txt'
    email_subject_template = 'registration/activation_email_subject.txt'
    form_class = UserRegistrationForm

    @method_decorator(check_honeypot)
    def dispatch(self, request, *args, **kwargs):
        return super(UserRegistrationView, self).dispatch(request, *args, **kwargs)

    def create_inactive_user(self, form):
        """
        Create an inactive user using the email provided and send an email to that address.
        """
        email = form.cleaned_data['email']
        new_user = User.objects.create(username=email, email=email, is_active=False)

        self.send_activation_email(new_user)
        return new_user


class WelcomePageView(TemplateView):

    template_name = 'main/planetxy.html'


class UserActivationView(SuccessMessageMixin, UpdateView, ActivationView):
    '''
    Handles account activation. Captures the details of a user and set their
    account to active if all details provided are okay.
    '''

    form_class = UserActivationForm
    model = User
    template_name = 'registration/activation_form.html'
    success_message = "."
    initial = {'username': ''}

    def get(self, *args, **kwargs):
        activated_user = self.activate(*args, **kwargs)
        if not activated_user:
            return redirect('activation_failure')

        self.object = activated_user
        signals.user_activated.send(
            sender=self.__class__,
            user=activated_user,
            request=self.request
        )
        return super(UserActivationView, self).get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserActivationView, self).get_context_data(**kwargs)
        context['formset'] = AnswerFormSet
        context['helper'] = AnswerFormSetHelper
        return context

    def save_form(self, form):
        user = self.get_object()
        user.set_password(form.cleaned_data["password1"])
        user.username = form.cleaned_data["username"]
        user.save()

        UserProfile.objects.create(user=user)

    def post(self, request, *args, **kwargs):
        instance = self.get_object()

        form = UserActivationForm(request.POST)
        if form.is_valid():
            self.save_form(form)
            message = '''
                Thank you for registering with the GeoKey system.
                Please click on the sign-in link to use the GeoKey system.
            '''
            messages.success(self.request, message)
            return redirect('usergeokey')
        else:
            context = {
                'form': form,
                'helper': AnswerFormSetHelper,
            }
            return render(request, self.template_name, context)

    def get_object(self):
        username = self.validate_key(self.kwargs.get('activation_key'))
        return get_object_or_404(User, username=username)


class UserActivationFailureView(TemplateView):
    '''
    Users are redirected here if their activation process failed, eg the activation
    link had expired or had already been used.
    '''

    template_name = 'registration/activation_failure.html'


# #############################
#  Geokey views              #
##############################

class UserGeoKeyMixin(LoginRequiredMixin, SuccessMessageMixin):

    model = UserGeoKey
    form_class = UserGeoKeyForm
    success_url = reverse_lazy('usergeokey')

    def form_valid(self, form):
        if not self.request.user.is_anonymous:
            form.instance.user = self.request.user
        form.save()

        return super(UserGeoKeyMixin, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below first.")
        return super(UserGeoKeyMixin, self).form_invalid(form)


class UserGeoKeyCreateView(UserGeoKeyMixin, CreateView):
    '''
    Displays an interactive map and allows users to search and save locations
    based on an geokey, lat/long values or address.
    '''

    success_message = "The location has been saved successfully."

    def get(self, request, *args, **kwargs):
        geokey_count = UserGeoKey.objects.filter(user=self.request.user).count()
        if geokey_count > settings.MAX_GEOKEYS_FOR_FREE_ACCOUNT:
            return redirect('subscription_notification')
        return super(UserGeoKeyCreateView, self).get(request, *args, **kwargs)

    def get_initial(self):
        initial = {}
        geokey = self.request.GET.get('geokey')
        if geokey:
            initial['geokey'] = geokey
        return initial


class UserGeoKeyUpdateView(UserGeoKeyMixin, UpdateView):
    '''Allow users to update their saved geokeys'''

    success_message = "The location has been updated successfully."


class UserGeoKeyDeleteView(LoginRequiredMixin, DeleteView):
    '''Allow user to delete a given geokey'''

    model = UserGeoKey
    success_url = reverse_lazy('usergeokeys')


class UserGeoKeyListView(LoginRequiredMixin, ListView):
    '''
    Display the last twenty 25 searches of the user currently logged in.
    A user cannot view another person's saved searches.
    '''

    context_object_name = 'geokeys'
    paginate_by = 25
    paginate_orphans = 3

    def get_queryset(self):
        return UserGeoKey.objects.filter(user=self.request.user)


class UserGeoKeyBulkDeleteView(LoginRequiredMixin, TemplateView):

    template_name = 'main/usergeokey_confirm_delete_all.html'
    success_url = 'usergeokeys'

    def post(self, request, *args, **kwargs):
        UserGeoKey.objects.filter(user=self.request.user).delete()
        return redirect('usergeokeys')


# #############################
#  Utility views              #
##############################

class EmailGeoKeyFormView(LoginRequiredMixin, FormView):

    form_class = EmailGeoKeyForm
    template_name = 'main/email_geokey_form.html'
    success_url = reverse_lazy('usergeokeys')

    def get_email_context(self):
        scheme = 'http' if settings.DEBUG else 'https'
        geokey = self.kwargs.get('geokey', '')
        share_current = self.request.GET.get('share')
        if share_current:
            geokey = self.request.GET.get('geokey', '')
        return {
            'scheme': scheme,
            'user': self.request.user,
            'site': get_current_site(self.request),
            'geokey': geokey,
            'share_current': share_current
        }

    def form_valid(self, form):
        form.send_email(self.get_email_context())
        messages.success(self.request, "The geokey has been emailed successfully.")
        return super(EmailGeoKeyFormView, self).form_valid(form)


class SubscriptionNotificationView(LoginRequiredMixin, TemplateView):

    template_name = 'main/subscription_notification.html'


class UserGeoKeyListMapView(LoginRequiredMixin, ListView):
    '''Display a user saved positions in a map.'''

    template_name = 'main/search_list_map.html'
    context_object_name = 'user_searches'
    paginate_by = 25
    paginate_orphans = 3

    def get_context_data(self):
        ctx = super(UserGeoKeyListMapView, self).get_context_data()
        ctx['map_api_key'] = settings.GEOPOSITION_GOOGLE_MAPS_API_KEY
        return ctx

    def get_queryset(self):
        user_searches = []
        queryset = UserGeoKey.objects.filter(user=self.request.user)
        for row in queryset:
            data = {
                'address': row.address,
                'geokey': row.geokey,
                'created': row.created,
                'lat': row.position.latitude,
                'lon': row.position.longitude
            }
            user_searches.append(data)
        return user_searches


class DownloadMixin(LoginRequiredMixin, View):

    http_method_names = [u'get']

    def get_dataset(self):
        queryset = UserGeoKey.objects.filter(user=self.request.user)

        headers = ['GeoKey', 'Address', 'Latitude', 'Longitude', 'Date saved', "Nickname"]
        dataset = Dataset(headers=headers)

        # Body
        for data in queryset.only('geokey', 'address', 'position', 'created', 'nickname').iterator():
            lat = '{0:.5f}'.format(data.position.latitude)
            lon = '{0:.5f}'.format(data.position.longitude)

            dataset.append([data.geokey, data.address, lat, lon, data.created.date(), data.nickname])

        return dataset

    def get(self, request, *args, **kwargs):
        dataset = self.get_dataset()

        if self.data_type == 'csv':
            content_file = ContentFile(dataset.csv)
            suffix = 'csv'
        else:
            content_file = ContentFile(dataset.xlsx)
            suffix = 'xlsx'

        response = FileResponse(content_file)
        response['Content-Disposition'] = 'attachment; filename="{}-saved-locations.{}"'.format(request.user.username, suffix)
        return response


class GeoKeyCSVView(DownloadMixin):
    '''Users download their saved locations in csv format'''

    data_type = 'csv'


class GeoKeyExcelView(DownloadMixin):
    '''Alow users to download their saved locations in excel format'''

    data_type = 'excel'


class ShareView(View):
    template_name = 'main/share_geokey.html'

    def get(self, request, *args, **kwargs):
        geokey = self.request.GET.get('geokey', '')
        ctx = {
            'geo_key': geokey,
            'open_link': '{}/share/?geokey={}'.format(settings.NATIVE_APP_REDIRECT_URL, geokey)
        }
        return render(request, self.template_name, ctx)


# #############################
#  Mobile views
##############################

class MobileGeoKeyView(SuccessMessageMixin, FormView):

    form_class = MobileGeoKeyForm
    template_name = 'main/mobile_geokey_form.html'
    success_url = reverse_lazy('welcome')
    success_message = 'The co-ordinates have been generated'

    def get_initial(self):
        initial = {}
        geokey = self.request.GET.get('geokey')
        if geokey:
            initial['geokey'] = geokey
        return initial

    def get_context_data(self):
        ctx = super(MobileGeoKeyView, self).get_context_data()
        ctx['map_api_key'] = settings.GEOPOSITION_GOOGLE_MAPS_API_KEY
        return ctx

    def form_valid(self, form):
        return super(MobileGeoKeyView, self).form_valid(form)
