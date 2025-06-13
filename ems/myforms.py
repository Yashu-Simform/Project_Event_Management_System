from django import forms
# from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Button, HTML
from django.urls import reverse
from src.apps.authentication.models import EmsUser
from src.apps.events.models import Event
from src.apps.invitations.models import Invite
from core.validators import user_model_validations

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(render_value=True), validators=[user_model_validations.validate_password])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        login_page_url = reverse('user_login_page')
        self.helper = FormHelper(self)
        self.helper.attrs = {'id': 'registrationForm'}
        self.helper.form_action = reverse('user_registration')
        self.helper.layout = Layout( 
            'email',
            'first_name',
            'last_name',
            'password',
            HTML(f'<p>Already have an account ? <a style="color: blue;" href="{login_page_url}">SignIn</a></p>'),
            Submit('submit', 'Register'),
        )

    class Meta:
        model = EmsUser
        fields = ['email', 'first_name', 'last_name', 'password']


class UserLoginForm(forms.ModelForm):
    email = forms.EmailField(max_length=255, widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput(render_value=True))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        registration_page_url = reverse('user_registration_page')   
        self.helper = FormHelper(self)
        self.helper.attrs = {'id': 'loginForm'}
        self.helper.form_action = reverse('user_login')
        self.helper.layout = Layout( 
            'email',
            'password',
            HTML(f'<p>Create new account ? <a style="color: blue;" href="{registration_page_url}">SignUp</a></p>'),
            Submit('login', 'Login', css_id='loginbtn'),
        )

    class Meta:
        model = EmsUser
        fields = ['email', 'password']

# Event Form
class EventForm(forms.ModelForm):

    # event_time = forms.DateTimeField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('create', 'Create Event', css_id='createbtn'))
        self.helper.attrs = {'id': 'eventform'}
        self.helper.form_action = reverse('create_event')

    class Meta:
        model = Event
        fields = ['title', 'description', 'event_type', 'venue', 'event_time']

        widgets = {
            'event_time': forms.TextInput(attrs={'type':'datetime-local'}),
        }

class EventUpdateForm(forms.ModelForm):
    title = forms.CharField(initial='Hello' ,widget=forms.TextInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.attrs = {'id': 'eventupdateform'}
        self.helper.add_input(Submit('update', 'Update Event', css_id='updatebtn'))

    class Meta:
        model = Event
        fields = ['title', 'description', 'event_type', 'venue', 'event_time']

        widgets = {
            'title': forms.TextInput(),
            'description': forms.TextInput(),
            'venue': forms.TextInput(),
            'event_time': forms.TextInput(attrs={'type':'datetime-local'})
        }


# Invitation
class InviteSentForm(forms.ModelForm):
    receiver_email = forms.EmailField(label="Email: ", required=True, widget=forms.EmailInput())
    event_id = forms.ChoiceField(choices=[('hi', 'Hi'), ('hello', 'Hello')], required=True, label = 'Select Event: ')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.attrs = {'id': 'inviteform'}
        self.helper.layout = Layout(
            Div(    
                'receiver_email',
                'event_id',
                css_class='modal-body'
            ),
            Div(
                HTML('<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>'),
                Submit(name='sendinvite', value='sendInvite', css_id='sendInviteBtn'),
                css_class="modal-footer"
            )
        )
    
    class Meta:
        model = Invite
        fields = ['sent_to']