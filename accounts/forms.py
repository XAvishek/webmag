from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile


class EmailValidation(forms.EmailField):
    def validate(self, value):
        try:
            User.objects.get(email=value)
            raise forms.ValidationError("Email already exists.")
        except User.MultipleObjectsReturned:
            raise forms.ValidationError("email already exists")
        except User.DoesNotExist:
            pass


class UserSignUpForm(UserCreationForm):
    email = EmailValidation(required=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name')


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['dob', 'address', 'image']


class EmailSignupForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'type': "email",
        'name': "newsletter",
        'id': "email",
        'placeholder': "Enter your email"
    }), label='')

    class Meta:
        model = User
        fields = ['email']
