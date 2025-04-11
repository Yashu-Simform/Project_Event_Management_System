from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Button, HTML
from django.urls import reverse
from .emsmodels import *

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(render_value=True))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.form_action = reverse('user_registration')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']


class UserLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(render_value=True))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('login', 'Login', css_id='loginbtn'))
        # self.helper.form_action = reverse('token_obtain_pair')

    class Meta:
        model = User
        fields = ['username', 'password']

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
    invite_to = forms.EmailField(label="Email: ", required=True, widget=forms.EmailInput())
    events = forms.ChoiceField(choices=[('hi', 'Hi'), ('hello', 'Hello')], required=True, label = 'Select Event: ')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.attrs = {'id': 'inviteform'}
        self.helper.layout = Layout(
            Div(    
                'invite_to',
                'events',
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
        fields = ['invite_to']