from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, User
# from accounts.models import User
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=120)
    password = forms.CharField(max_length=120)
    remember_me = forms.BooleanField(required=False)


class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        for field_name in ['username', 'password', 'bio', 'profile_image']:
            self.fields[field_name].help_text = None
    # first_name = forms.CharField(max_length=90)
    # last_name = forms.CharField(max_length=90)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        for field_name in ['username', 'password1', 'password2']:
            self.fields[field_name].help_text = None


class EditProfileForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        for field_name in ['username', 'password']:
            self.fields[field_name].help_text = None

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')


class PasswordResetForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=20, widget=forms.PasswordInput())
    new_password1 = forms.CharField(label='New password', max_length=20, widget=forms.PasswordInput())
    new_password2 = forms.CharField(label='Confirm new password', max_length=20, widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        for field_name in ['old_password', 'new_password1', 'new_password2', ]:
            self.fields[field_name].help_text = None

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2',)