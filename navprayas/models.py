from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime
    
# NAME	MOTHER'S NAME 	FATHER'S NAME 	CLASS	SCHOOL/COACHING	BOARD	Q.P.L(H/E)	D.O.B	GENDER	ADDRESS	LANDMARK	PO+PS	DISTRICT	PIN	CONTACT
GENDER = (
    ('Female','Female'),
    ('','Male'),
)
# question paper language
QPL = (
    ('','English'),
    ('Hindi','Hindi'),
)
CLASS = (
        ('', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
    )

BOARD = (
    ('','BSEB'),
    ('CBSE','CBSE'),
)

# G1(Upto 13 Years)
# G2(From 14 to 17 Years)
# G3(Above 17 Years)

# chess category

C_CATEGORY = (
    ('','Upto 13 yrs'),
    ('G2','From 14 to 17 yrs'),
    ('G3','Above 17 yrs'),
)
# FHS category


F_CATEGORY = (
    ('','V/VI/VII'),
    ('SENIOR','VIII/IX/X'),
)
R_CATEGORY = (
    ('','JUNIOR'),
    ('SENIOR','Above or equal to 13 yrs'),
)

S_CATEGORY = (
    ('','Upto 13 yrs'),
    ('SENIOR','Above 13 yrs'),
)

P_CATEGORY = (
    ('','VII/VIII'),
    ('SENIOR','IX/X'),
)
# ------------------------------------------------------------------------------------------------
class Profile (models.Model):
    user            = models.OneToOneField(User,verbose_name="user", on_delete=models.CASCADE)
    city            = models.CharField(max_length=50, blank=True, null=True)
    mother_name     = models.CharField(max_length=50, blank=True, null=True)
    father_name     = models.CharField(max_length=50, blank=True, null=True)
    class_study     = models.PositiveIntegerField(default=5, null=True, validators=[MinValueValidator(4), MaxValueValidator(10)])
    post_office     = models.CharField(max_length=50, blank=True, null=True)
    gender          = models.CharField(default = 'Male', max_length=50, blank=True, null=False,choices = GENDER)
    addess          = models.CharField(max_length=50, blank=True, null=True)
    landmark        = models.CharField(max_length=50, blank=True, null=True)
    birth_date      = models.DateField(("Date of birth"),null = False, default=datetime.date.today)
    ditrict         = models.CharField(max_length=50, blank=True, null=True)
    post_office     = models.PositiveIntegerField(validators=[MinValueValidator(100000), MaxValueValidator(999999)], blank=True, null=True)
    Home_number     = models.CharField(max_length=10, blank=True, null=True)
    contact         = models.PositiveIntegerField(validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)] , blank=False,null = True)

    def __str__(self):
        return f'{self.user.first_name}'

#   --------------------------------------------------------------------------------------------------------------  # 


def create_profile(sender, **kwargs):
    if(kwargs["created"]):
        user_profile = Profile.objects.create(user = kwargs["instance"])


post_save.connect(create_profile,sender=User)



#   --------------------------------------------------------------------------------------------------------------  # 


class MTSE (models.Model):
    MTSE_user       = models.OneToOneField(User, on_delete = models.CASCADE)
    qpl             = models.CharField(max_length = 9, choices = QPL,blank = False,null = False,verbose_name = 'Paper langauge')
    father_name     = models.CharField(max_length=50, blank=True, null=True)
    mother_name     = models.CharField(max_length=50, blank=True, null=True)
    st_class        = models.CharField(choices=CLASS, max_length=2, blank=False,null = False ) 
    board           = models.CharField(max_length = 6,choices = BOARD)
    class_study     = models.PositiveIntegerField(default=4, null=True, validators=[MinValueValidator(4), MaxValueValidator(10)])
    school          = models.CharField(max_length=50, blank=True, null=True)
    post_office     = models.CharField(max_length=50, blank=True, null=True)
    birth_date      = models.DateField(("Date of birth"), default=datetime.date.today)
    gender          = models.CharField(max_length=50, blank=True, null=True,choices = GENDER)
    landmark        = models.CharField(max_length=50, blank=True, null=True)
    addess          = models.CharField(max_length=50, blank=True, null=True)
    ditrict         = models.CharField(max_length=50, blank=True, null=True)
    city            = models.CharField(max_length=50, blank=True, null=True)
    pin             = models.PositiveIntegerField(validators=[MinValueValidator(1000000), MaxValueValidator(999999)], blank=True, null=True)
    Home_number     = models.CharField(max_length=10, blank=True, null=True)
    
class PR (models.Model):
    PR_user     = models.OneToOneField(User, on_delete = models.CASCADE)
    category    = models.CharField(choices=P_CATEGORY, max_length=12, blank=False) 
    Full_name1  = models.CharField(max_length=50, blank=True, null=True)
    class1      = models.PositiveIntegerField(default=4, null=True, validators=[MinValueValidator(4), MaxValueValidator(10)])
    contact_1   = models.PositiveIntegerField(validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)] , blank=False)
    addess1     = models.CharField(max_length=50, blank=True, null=True)
    Full_name2  = models.CharField(max_length=50, blank=True, null=True)
    class2      = models.PositiveIntegerField(default=4, null=True, validators=[MinValueValidator(4), MaxValueValidator(10)])
    address_2   = models.CharField(max_length=100 , blank=False)
    contact_3   = models.PositiveIntegerField(validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)] , blank=False)
    Full_name3  = models.CharField(max_length=50, blank=True, null=True)
    class3      = models.PositiveIntegerField(default=4, null=True, validators=[MinValueValidator(4), MaxValueValidator(10)])
    address_3   = models.CharField(max_length=100 , blank=False)
    contact_3   = models.PositiveIntegerField(validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)] , blank=False)


# Story and Poem Writing
class SPR (models.Model):
    SPR_user    = models.OneToOneField(User, on_delete     = models.CASCADE,)
    Full_name   = models.CharField(max_length=50, blank=True, null=True)
    category    = models.CharField(choices=S_CATEGORY, max_length=12, blank=False) 
    contact     = models.PositiveIntegerField(validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)] , blank=False)
    addess     = models.CharField(max_length=50, blank=True, null=True)


class rangotsav (models.Model):
    rangotsav_user  = models.OneToOneField(User, on_delete = models.CASCADE,)
    category    = models.CharField(choices=R_CATEGORY, max_length=12, blank=False) 
    Full_name1  = models.CharField(max_length=50, blank=True, null=True)
    contact_1   = models.PositiveIntegerField(validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)] , blank=False)
    addess1     = models.CharField(max_length=50, blank=True, null=True)
    Full_name2  = models.CharField(max_length=50, blank=True, null=True)
    address_2   = models.CharField(max_length=100 , blank=False)
    contact_2   = models.PositiveIntegerField(validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)] , blank=False)
    Full_name3  = models.CharField(max_length=50, blank=True, null=True)
    address_3   = models.CharField(max_length=100 , blank=False)
    contact_3   = models.PositiveIntegerField(validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)] , blank=False)



class chess (models.Model):
    chess_user = models.OneToOneField(User, on_delete = models.CASCADE,)
    Full_name   = models.CharField(max_length=50, blank=True, null=True)
    category = models.CharField(choices=C_CATEGORY, max_length=12, blank=False) 
    contact     = models.PositiveIntegerField(validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)] , blank=False)
    addess     = models.CharField(max_length=50, blank=True, null=True)
    
class FHS (models.Model):
    FHS_user    = models.OneToOneField(User, on_delete = models.CASCADE,)
    Full_name   = models.CharField(max_length=50, blank=True, null=True)
    category    = models.CharField(choices=F_CATEGORY ,max_length=12, blank=False) 
    contact     = models.PositiveIntegerField(validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)] , blank=False)
    addess     = models.CharField(max_length=50, blank=True, null=True)

