from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime
    
# NAME	MOTHER'S NAME 	FATHER'S NAME 	CLASS	SCHOOL/COACHING	BOARD	Q.P.L(H/E)	D.O.B	GENDER	ADDRESS	LANDMARK	PO+PS	DISTRICT	PIN	CONTACT
GENDER = (
    ('female','female'),
    ('male','male'),
)
class Profile (models.Model):
    user            = models.OneToOneField(User, verbose_name="user", on_delete=models.CASCADE)
    city            = models.CharField(max_length=50, blank=True, null=True)
    mother_name     = models.CharField(max_length=50, blank=True, null=True)
    class_study     = models.PositiveIntegerField(default=4, null=True, validators=[MinValueValidator(4), MaxValueValidator(10)])
    school          = models.CharField(max_length=50, blank=True, null=True)
    board           = models.CharField(max_length=50, blank=True, null=True)
    post_office     = models.CharField(max_length=50, blank=True, null=True)
    gender          = models.CharField(max_length=50, blank=True, null=True,choices = GENDER)
    addess          = models.CharField(max_length=50, blank=True, null=True)
    landmark        = models.CharField(max_length=50, blank=True, null=True)
    birth_date       = models.DateField(("Date of birth"), default=datetime.date.today)
    ditrict         = models.CharField(max_length=50, blank=True, null=True)
    pin             = models.PositiveIntegerField(max_length=6, blank=True, null=True)
    

    def __str__(self):
        return f'{self.user.first_name} Profile'


def create_profile(sender, **kwargs):
    if(kwargs["created"]):
        user_profile = Profile.objects.create(user = kwargs["instance"])


post_save.connect(create_profile,sender=User)



    


class MTSE (models.Model):
    MTSE_user = models.OneToOneField(User, on_delete = models.CASCADE)
    student_class = (
        ('1', '5'),
        ('1', '6'),
        ('1', '7'),
        ('1', '8'),
        ('1', '9'),
        ('1', '10'),
    )
    st_class = models.CharField(choices=student_class, max_length=2, blank=False, ) 
    father_name = models.CharField(max_length=100 , blank=False)
        
    
class PR (models.Model):
    PR_user = models.OneToOneField(User, on_delete = models.CASCADE)
    division = (
        ('junior', 'junior(7&8)'),
        ('senior', 'senior(9&10)'),
    )
    category = models.CharField(choices=division, max_length=12, blank=False) 
    candidate_2 = models.CharField(max_length=100 , blank=False)
    address_2 = models.CharField(max_length=100 , blank=False)
    contact_2 = models.CharField(max_length=12 , blank=False)
    candidate_3 = models.CharField(max_length=100 , blank=False)
    address_3 = models.CharField(max_length=100 , blank=False)
    contact_3 = models.CharField(max_length=12 , blank=False)


# Story and Poem Writing
class SPR (models.Model):
    SPR_user = models.OneToOneField(User, on_delete = models.CASCADE,)
    division = (
        ('junior', 'junior(7&8)'),
        ('senior', 'senior(9&10)'),
    )
    category = models.CharField(choices=division, max_length=12, blank=False) 
    candidate_2 = models.CharField(max_length=100 , blank=False)
    address_2 = models.CharField(max_length=100 , blank=False)
    contact_2 = models.PositiveIntegerField(validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)] , blank=False)
    candidate_3 = models.CharField(max_length=100 , blank=False)
    address_3 = models.CharField(max_length=100 , blank=False)
    contact_3 = models.PositiveIntegerField(validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)] , blank=False)
    

class rangotsav (models.Model):
    rangotsav_user = models.OneToOneField(User, on_delete = models.CASCADE,)
    division = (
        ('junior', 'junior(7&8)'),
        ('senior', 'senior(9&10)'),
    )
    category = models.CharField(choices=division, max_length=12, blank=False) 


class chess (models.Model):
    chess_user = models.OneToOneField(User, on_delete = models.CASCADE,)
    division = (
        ('junior', 'junior(7&8)'),
        ('senior', 'senior(9&10)'),
    )
    category = models.CharField(choices=division, max_length=12, blank=False) 
    
class FHS (models.Model):
    FHS_user = models.OneToOneField(User, on_delete = models.CASCADE,)
    division = (
        ('junior', 'junior(7&8)'),
        ('senior', 'senior(9&10)'),
    )
    category = models.CharField(choices=division, max_length=12, blank=False) 
    
