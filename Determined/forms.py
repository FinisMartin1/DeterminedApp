from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from django import forms
from users.models import User


class UserLoginForm(AuthenticationForm):
    """Modifies authenication form to support email and custom styling

    Args:
        AuthenticationForm: extends default AuthenticationForm
    """
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.EmailField(widget=forms.TextInput(
            attrs={'class': 'form-control form-control-user',
                'placeholder': 'Enter Email Address...', 'id': 'exampleInputEmail'}),
        label="")
    password = forms.CharField(widget=forms.PasswordInput(
            attrs={'class': 'form-control form-control-user','placeholder': 'Password',
                'id': 'exampleInputPassword',
            }),
        label="")

class UserCreation(UserCreationForm):
    """Modifies user creation form to support names, multi-passwords, access level, and email

    Args:
        UserCreationForm: extends default UserCreationForm
    """
    def __init__(self, *args, **kwargs):
        super(UserCreation, self).__init__(*args, **kwargs)
    first_name = forms.CharField(max_length=32)
    last_name=forms.CharField(max_length=32)
    email=forms.EmailField(max_length=64)
    password1=forms.CharField()
    password2=forms.CharField()
    accessLevel=forms.ChoiceField(
        choices=[("Instructor", "Instructor"), 
                ("Administrator","Administrator")], 
        widget=forms.RadioSelect)
        

    class Meta: 
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2', 'accessLevel']
    
    def save(self, commit=True):
        email = self.cleaned_data['email']
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        access_level = self.cleaned_data['accessLevel']
        password = self.cleaned_data.get("password2")
        if commit:
            user = User.objects.create_user(email, first_name, last_name, access_level, password)
        return user
