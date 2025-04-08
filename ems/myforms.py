from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
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