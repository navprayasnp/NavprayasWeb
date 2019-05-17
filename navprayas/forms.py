from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *
from django.utils.translation import gettext, gettext_lazy as _


# *************
# User Signup Form
# *************
class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
        # help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        strip=False,
        # help_text=_("Enter the same password as before, for verification."),
    )
    class Meta:
        model = User
        fields = ( 'first_name', 'last_name', 'email', 'password1', 'password2',)


# *************
# Profile Signup Form
# *************
class SignUpFormProfile(forms.ModelForm):
    birth_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'placeholder': 'yyyy-mm-dd'}),
        )
    class Meta:
        model = Profile
        fields = ( 'birth_date', 'gender', )


#    user upadate form and profile update form 
# 
#  

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'mother_name',
            'father_name',
            'class_study',
            'post_office',
            'birth_date',
            'gender',
            'Home_number',
            'landmark',
            'addess',
            'contact',
            'pin',
            'ditrict',
            'city',
        ]

# *************
# Free hand sketching Form
# *************
class FHS_form(forms.ModelForm):
    class Meta:
        model = FHS
        fields = (
            'Full_name',
            'category',
            'contact',
            'addess',
        )

# *************
# Rangotsav Form
# *************
class rangotsav_form(forms.ModelForm):
    class Meta:
        model = rangotsav
        fields = (
            'category',
            'Full_name1',
            'contact_1',
            'addess1',
            'Full_name2',
            'address_2',
            'contact_2',
            'Full_name3',
            'address_3',
            'contact_3',
        )

# *************
# Puzzle Race Form
# *************
class PR_form(forms.ModelForm):
    class Meta:
        model = PR
        fields = (
            'category',
            'Full_name1',
            'class1',
            'contact_1',
            'addess1',
            'Full_name2',
            'class2',
            'address_2',
            'contact_2',
            'Full_name3',
            'class3',
            'address_3',
            'contact_3',
         )

# *************
# MTSE Form
# *************
class MTSE_form(forms.ModelForm):
    class Meta:
        model = MTSE
        fields = (
            'qpl',
            'father_name',
            'mother_name',
            'st_class',
            'board',
            'school',
            'post_office',
            'birth_date',
            'gender',
            'landmark',
            'addess',
            'ditrict',
            'city',
            'pin',
            'Home_number',
        )

# *************
# Story and Poem Writing Form
# *************
class SPR_form(forms.ModelForm):
    class Meta:
        model = SPR
        fields = (
            'Full_name',
            'category',
            'contact',
            'addess',
         )
# *************
# Chess Competition Form
# *************
class chess_form(forms.ModelForm):
    class Meta:
        model = chess
        fields = (
            'Full_name',
            'category',
            'contact',
            'addess',
        )


    


   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
    # class ArticleForm(forms.ModelForm):
    # headline = MyFormField(
    #     max_length=200,
    #     required=False,
    #     help_text='Use puns liberally',
    # )

    # class Meta:
    #     model = Article
    #     fields = ['headline', 'content']
