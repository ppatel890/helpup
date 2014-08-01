from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from helpup.models import Project, Donation


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')



# class CreateProjectForm(forms.Form):
#     title = forms.CharField(max_length=150)
#     description = forms.CharField()
#     location = forms.CharField(max_length=6)
#     picture = forms.ImageField()
#
#     class Meta:
#         model = Project
#         fields = ('title', 'description', 'location', 'picture')
#



class AddPicture(ModelForm):
    class Meta:
        model=Project
        fields = ['picture', 'title', 'description', 'date_created','location', 'student', 'donor', 'lat', 'lng']


class DonateForm(ModelForm):
    class Meta:
        model = Donation







