from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import *
from .models import *


# *************
# User Signup Form
# *************
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ( 'first_name', 'last_name', 'email', 'password1', 'password2',)


# *************
# Profile Signup Form
# *************
class SignUpFormProfile(ModelForm):
    class Meta:
        model = Profile
        fields = ( 'birth_date', 'gender', )


#    user upadate form and profile update form 
# 
#  

class UserUpdateForm(ModelForm):
    email = EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = [
            'city',
            'mother_name',
            'class_study',
            'school',
            'board',
            'post_office',
            'gender',
            'addess',
            'landmark',
            'birth_date',
            'ditrict',
            'pin',
        ]



















# *************
# Free hand sketching Form
# *************
class FHS_form(ModelForm):
    class Meta:
        model = FHS
        fields = ('category',)

# *************
# Rangotsav Form
# *************
class rangotsav_form(ModelForm):
    class Meta:
        model = rangotsav
        fields = ('category',)

# *************
# Puzzle Race Form
# *************
class PR_form(ModelForm):
    class Meta:
        model = PR
        fields = ('category','candidate_2','address_2','contact_2','candidate_3','address_3','contact_3', )

# *************
# MTSE Form
# *************
class MTSE_form(ModelForm):
    class Meta:
        model = MTSE
        fields = ('st_class',)

# *************
# Story and Poem Writing Form
# *************
class SPR_form(ModelForm):
    class Meta:
        model = SPR
        fields = ('category','candidate_2','address_2','contact_2','candidate_3','address_3','contact_3', )
# *************
# Chess Competition Form
# *************
class chess_form(ModelForm):
    class Meta:
        model = chess
        fields = ('category',)


    


   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
    # class ArticleForm(ModelForm):
    # headline = MyFormField(
    #     max_length=200,
    #     required=False,
    #     help_text='Use puns liberally',
    # )

    # class Meta:
    #     model = Article
    #     fields = ['headline', 'content']