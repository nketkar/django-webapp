from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm, UserCreationForm,
    PasswordResetForm as BasePasswordResetForm,
    SetPasswordForm as BaseSetPasswordForm
)
from django.core.exceptions import NON_FIELD_ERRORS
from django.core.mail import EmailMultiAlternatives
from django.forms import inlineformset_factory, formset_factory, BaseFormSet, BaseInlineFormSet
from django.template import loader

from crispy_forms.bootstrap import AppendedText, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Div, HTML

from .models import Answer, Question, UserGeoKey

User = get_user_model()


class UserAuthenticationForm(AuthenticationForm):
    '''
    Form used in the sign in page.
    '''

    def __init__(self, *args, **kwargs):
        super(UserAuthenticationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('username', css_class='form-control-lg', wrapper_class='row'),
            Field('password', css_class='form-control-lg', wrapper_class='row'),
        )


class UserRegistrationForm(forms.Form):
    '''
    Form used in the user registration page.
    '''

    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.helper.form_method = 'post'
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('email', css_class='form-control-lg', wrapper_class='row'),
            Submit('save', 'Register me', css_class='btn-lg offset-lg-4'),
        )
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        """
        Validate that the supplied email address is unique for the site.
        """
        message = "This email address is already in use. Please supply a different email address."

        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(message)
        return self.cleaned_data['email']


class UserActivationForm(UserCreationForm):
    '''
    Used in the activation view to capture a new user's details.
    '''

    company = forms.CharField(label='Company(if applicable)', max_length=100, required=False)

    def __init__(self, *args, **kwargs):
        super(UserActivationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = ''
        self.fields['password2'].label = 'Confirm password'
        self.fields['username'].help_text = 'You will use it when sigining into the account'
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('username', wrapper_class='row'),
            Field('password1', wrapper_class='row'),
            Field('password2', wrapper_class='row'),
        )
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'


class PasswordResetForm(BasePasswordResetForm):

    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        #self.fields['email'].widget = forms.HiddenInput()


class SetPasswordForm(BaseSetPasswordForm):

    def __init__(self, *args, **kwargs):
        super(SetPasswordForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['new_password1'].help_text = ''
        self.helper.add_input(Submit('submit', 'Change my password'))


class AnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ('question', 'answer')

        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "Sorry, that is a common answer. Please give another answer or select another question."
            }
        }


class AnswerFormSetMixin:

    def clean(self):
        """Don't allow a user to answer the same question twice."""
        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on its own
            return
        questions = []
        for form in self.forms:
            question = form.cleaned_data['question']
            if question in questions:
                raise forms.ValidationError("Repeating the same question is not allowed.")
            questions.append(question)


class AnswerChoiceForm(forms.Form):

    question = forms.ModelChoiceField(Question.objects.all())
    answer = forms.CharField(max_length=255)


class BaseAnswerFormSet(AnswerFormSetMixin, BaseInlineFormSet):

    '''
        Base formset which displays forms each with a questions select
        dropdown and answer
    '''


# Used in the activation view to capture the three secret questions and answers.
AnswerFormSet = inlineformset_factory(
    User,
    Answer,
    AnswerForm,
    min_num=3,
    extra=0,
    validate_min=True,
    can_delete=False,
    formset=BaseAnswerFormSet
)


class BaseAnswerChoiceFormSet(AnswerFormSetMixin, BaseFormSet):

    '''
        Used to displays two question/answer forms on the password reset view
    '''

    def clean(self):
        super(BaseAnswerChoiceFormSet, self).clean()

        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on its own
            return

        error = '''
            Sorry, a matching user account was not found. Please double
            check your answers and try again.
        '''
        users = []
        if not len(self.forms) == 2:
            raise forms.ValidationError(error)

        for form in self.forms:
            question = form.cleaned_data['question']
            answer = form.cleaned_data['answer']
            try:
                answer_obj = Answer.objects.get(
                    answer__exact=answer, question=question
                )
                user = User.objects.get(answers=answer_obj)
                users.append(user)
            except (Answer.DoesNotExist, User.DoesNotExist):
                raise forms.ValidationError(error)

        if users[0] == users[1]:
            self.user_email = users[0].email
        else:
            raise forms.ValidationError(error)


AnswerChoiceFormset = formset_factory(
    AnswerChoiceForm,
    min_num=2,
    validate_min=True,
    max_num=2,
    formset=BaseAnswerChoiceFormSet
)


class AnswerFormSetHelper(FormHelper):

    def __init__(self, *args, **kwargs):
        super(AnswerFormSetHelper, self).__init__(*args, **kwargs)
        self.form_method = 'post'
        self.form_tag = False
        self.wrapper_class = 'row'
        self.label_class = 'col-lg-3'
        self.field_class = 'col-lg-9'
        self.html5_required = True
        self.layout = Layout(
            Field('question', wrapper_class='row'),
            Field('answer', wrapper_class='row'),
        )


class UserGeoKeyForm(forms.ModelForm):
    '''
    Form used to capture a location's info
    '''
    search_address = forms.CharField(
        label='Address',
        required=False,
        help_text='Enter an address and press enter',
    )

    class Meta:
        model = UserGeoKey
        fields = ('address', 'geokey', 'search_address', 'position', 'nickname')

        help_texts = {
            'position': 'Drag the marker to change locations',
            'geokey': 'Enter a GeoKey and press enter',
        }

        labels = {
            'position': ''
        }

        widgets = {
            'address': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super(UserGeoKeyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'geokey-form'
        self.helper.layout = Layout(
            HTML('<div class="geokey-ajax-errors"></div>'),
            Div(
                Div('geokey', css_class='col-md-6'),
                Div('search_address', css_class='col-md-6'),
                css_class='row',
            ),
            'address', 'position',
            Div(
                Div('nickname', css_class='col-md-6'),
                css_class='row'
            ),
            StrictButton('Save position', type='submit', css_class='btn-primary btn-lg mb-5')
        )

    def clean_address(self):
        address = self.cleaned_data['address']
        # Until we configure mysql to handle unicode characters gracefully,
        # this will serve for the moment
        try:
            address.decode('ascii')
            return address
        except UnicodeEncodeError:
            return ''

    def clean_position(self):
        lat, lng = self.cleaned_data['position']
        is_valid_lat = lat >= -90 and lat <= 90
        is_valid_lng = lng >= -180 and lng <= 180

        if not is_valid_lat or not is_valid_lng:
            msg = '''
                The latitude value must be between -90 and 90 and longitude
                value must be between -180 and 180.
                '''
            raise forms.ValidationError(msg)
        return self.cleaned_data['position']


class EmailGeoKeyForm(forms.Form):

    email = forms.EmailField(
        help_text="Please enter the recipient's email address and hit send"
    )
    txt_template = 'main/partials/email_geokey.txt',
    html_template = 'main/partials/email_geokey_html.html',

    def __init__(self, *args, **kwargs):
        super(EmailGeoKeyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div('email', css_class='col-md-6'),
                css_class='row',
            ),
            StrictButton('Send', type='submit', css_class='btn-primary')
        )

    def send_email(self, email_context):
        to = self.cleaned_data['email']
        subject = 'Try out the PlanetXY Geokey service!'

        subject = '{} {}'.format(settings.EMAIL_SUBJECT_PREFIX, subject)
        # force subject to one line to avoid header injection issues
        subject = ''.join(subject.splitlines())

        txt_message = loader.render_to_string(self.txt_template, email_context)
        html_message = loader.render_to_string(self.html_template, email_context)

        msg = EmailMultiAlternatives(subject, txt_message, settings.DEFAULT_FROM_EMAIL, [to])
        msg.attach_alternative(html_message, "text/html")
        msg.send()


class MobileGeoKeyForm(forms.Form):

    geokey = forms.CharField(label="Destination GeoKey")
    current_geokey = forms.CharField(
        label="Current GeoKey",
        required=False,
        help_text='To share this GeoKey, click on the arrow.'
    )

    def __init__(self, *args, **kwargs):
        super(MobileGeoKeyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'mobile-geokey-form'
        self.helper.form_method = 'GET'
        self.helper.layout = Layout(
            AppendedText('current_geokey', '<i id="share-geokey" class="fa fa-share"></i>'),
            'geokey',
            StrictButton('Show position on map', type='submit', css_class='btn-primary my-2')
        )
