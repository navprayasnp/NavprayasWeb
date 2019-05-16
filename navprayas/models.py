from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime

# (datavbase, show onn page)

# NAME	MOTHER'S NAME 	FATHER'S NAME 	CLASS	SCHOOL/COACHING	BOARD	Q.P.L(H/E)	D.O.B	GENDER	ADDRESS	LANDMARK	PO+PS	DISTRICT	PIN	CONTACT
GENDER = (
    ('','select'),
    ('Female','Female'),
    ('Male','Male'),
)
# question paper language
QPL = (
    ('','select'),
    ('English','English'),
    ('Hindi','Hindi'),
)
CLASS = (
        ('', 'select'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
    )

BOARD = (
    ('','select'),
    ('BSEB','BSEB'),
    ('CBSE','CBSE'),
)

# G1(Upto 13 Years)
# G2(From 14 to 17 Years)
# G3(Above 17 Years)

# chess category

C_CATEGORY = (
    ('','select'),
    ('G1','Upto 13 yrs'),
    ('G2','From 14 to 17 yrs'),
    ('G3','Above 17 yrs'),
)
# FHS category


F_CATEGORY = (
    ('',''),
    ('Junior','V/VI/VII'),
    ('Senior','VIII/IX/X'),
)
R_CATEGORY = (
    ('','select'),
    ('Junior','Below 13 years'),
    ('Senior','Above or equal to 13 yrs'),
)

S_CATEGORY = (
    ('','select'),
    ('Junior','Upto 13 yrs'),
    ('Senior','Above 13 yrs'),
)

P_CATEGORY = (
    ('','select'),
    ('Junior','VII/VIII'),
    ('Senior','IX/X'),
)
# ------------------------------------------------------------------------------------------------
class Profile (models.Model):
    user            = models.OneToOneField(User,verbose_name="User", on_delete=models.CASCADE)
    city            = models.CharField(verbose_name="City", max_length=50, blank=True, null=True)
    mother_name     = models.CharField(verbose_name="Mother Name",max_length=50, blank=True, null=True)
    father_name     = models.CharField(verbose_name="Father Name",max_length=50, blank=True, null=True)
    class_study     = models.PositiveIntegerField(verbose_name="Class Study",default=5, null=True, validators=[MinValueValidator(4), MaxValueValidator(10)])
    post_office     = models.CharField(verbose_name="Post Office", max_length=50, blank=True, null=True)
    gender          = models.CharField(verbose_name="Gender", default = 'Male', max_length=50, blank=True, null=False,choices = GENDER)
    addess          = models.CharField(verbose_name="Address", max_length=50, blank=True, null=True)
    landmark        = models.CharField(verbose_name="Landmark", max_length=50, blank=True, null=True)
    birth_date      = models.DateField(("Date of birth"),null = False,blank = False, default=datetime.date.today)
    ditrict         = models.CharField(verbose_name="District",max_length=50, blank=True, null=True)
    pin             = models.PositiveIntegerField(verbose_name="Pin",validators=[MinValueValidator(100000), MaxValueValidator(999999)], blank=True, null=True)
    Home_number     = models.CharField(verbose_name="Home Number",max_length=10, blank=True, null=True)
    contact         = models.PositiveIntegerField(verbose_name="Contact",validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)] , blank=False,null = True)
    
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
    qpl             = models.CharField(max_length = 9, choices = QPL,blank = False, null = False,verbose_name = 'Paper langauge')
    father_name     = models.CharField(verbose_name="Father Name",max_length=50, blank=False, null=True)
    mother_name     = models.CharField(verbose_name="Mother Name",max_length=50, blank=False, null=True)
    st_class        = models.CharField(verbose_name="Std Class",choices=CLASS, max_length=2, blank=False,null = False )
    board           = models.CharField(verbose_name="Board",max_length = 6,choices = BOARD,blank=False)
    school          = models.CharField(verbose_name="School",max_length=50, blank=True, null=True)
    post_office     = models.CharField(verbose_name="Post Office",max_length=50, blank=True, null=True)
    birth_date      = models.DateField(("Date of birth"), default=datetime.date.today)
    gender          = models.CharField(verbose_name="Gender",max_length=50, blank=False, null=True,choices = GENDER)
    landmark        = models.CharField(verbose_name="Landmark",max_length=50, blank=True, null=True)
    addess          = models.CharField(verbose_name="Address",max_length=50, blank=True, null=True)
    ditrict         = models.CharField(verbose_name="District",max_length=50, blank=True, null=True)
    city            = models.CharField(verbose_name="City",max_length=50, blank=True, null=True)
    pin             = models.PositiveIntegerField(verbose_name="Pin",validators=[MinValueValidator(100000), MaxValueValidator(999999)], blank=True, null=True)
    Home_number     = models.CharField(verbose_name="Home Number",max_length=10, blank=True, null=True)
    payment         = models.BooleanField(default = False)
    order_id        = models.CharField(max_length = 20,blank = True,null = True)
    txn_date        = models.DateTimeField(null = True,blank = True  )

class PR (models.Model):
    PR_user     = models.OneToOneField(User, on_delete = models.CASCADE)
    category    = models.CharField(verbose_name="Category",choices=P_CATEGORY, max_length=12, blank=False)
    Full_name1  = models.CharField(verbose_name="Full Name",max_length=50, blank=False, null=True)
    class1      = models.PositiveIntegerField(verbose_name="Class",default=4, null=True, validators=[MinValueValidator(4), MaxValueValidator(10)])
    contact_1   = models.PositiveIntegerField(verbose_name="Contact",validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)], blank=False)
    addess1     = models.CharField(verbose_name="Address",max_length=50, blank=False, null=True)
    Full_name2  = models.CharField(verbose_name="Full Name",max_length=50, blank=False, null=True)
    class2      = models.PositiveIntegerField(verbose_name="Class",default=4, null=True, validators=[MinValueValidator(4), MaxValueValidator(10)])
    address_2   = models.CharField(verbose_name="Address",max_length=100 , blank=False)
    contact_2   = models.PositiveIntegerField(verbose_name='Contact', validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)] , blank=False, null=True)
    Full_name3  = models.CharField(verbose_name="Full Name",max_length=50, blank=True, null=True)
    class3      = models.PositiveIntegerField(verbose_name="Class",default=4, null=True, blank=True , validators=[MinValueValidator(4), MaxValueValidator(10)])
    address_3   = models.CharField(verbose_name="Address",max_length=100 , blank=True)
    contact_3   = models.PositiveIntegerField(verbose_name="Contact",validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)] , blank=True)
    payment         = models.BooleanField(default = False)
    order_id        = models.CharField(max_length = 20,blank = True,null = True)
    txn_date        = models.DateTimeField(null = True,blank = True  )


# Story and Poem Writing
class SPR (models.Model):
    SPR_user    = models.OneToOneField(User, on_delete     = models.CASCADE,)
    Full_name   = models.CharField(verbose_name="Full Name",max_length=50, blank=False, null=True)
    category    = models.CharField(verbose_name="Category",choices=S_CATEGORY, max_length=12, blank=False)
    contact     = models.PositiveIntegerField(verbose_name="Contact",validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)] , blank=False)
    addess      = models.CharField(verbose_name="Address",max_length=50, blank=False, null=True)
    payment     = models.BooleanField(default = True)
    order_id        = models.CharField(max_length = 20,blank = True,null = True)
    txn_date        = models.DateTimeField(null = True,blank = True  )


class rangotsav (models.Model):
    rangotsav_user  = models.OneToOneField(User, on_delete = models.CASCADE,)
    category    = models.CharField(verbose_name="Category",choices=R_CATEGORY, max_length=12, blank=False)
    Full_name1  = models.CharField(verbose_name="Full Name",max_length=50, blank=False, null=True)
    contact_1   = models.PositiveIntegerField(verbose_name="Contact",validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)] , blank=False)
    addess1     = models.CharField(verbose_name="Address",max_length=50, blank=False, null=True)
    Full_name2  = models.CharField(verbose_name="Full Name",max_length=50, blank=False, null=True)
    address_2   = models.CharField(verbose_name="Address",max_length=100 , blank=False)
    contact_2   = models.PositiveIntegerField(verbose_name="Contact",validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)] , blank=False, null=True)
    Full_name3  = models.CharField(verbose_name="Full Name",max_length=50, blank=True, null=True)
    address_3   = models.CharField(verbose_name="Address",max_length=100 , blank=True)
    contact_3   = models.PositiveIntegerField(verbose_name="Contact",validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)] , blank=True,null=True)
    payment     = models.BooleanField(default = True)
    order_id        = models.CharField(max_length = 20,blank = True,null = True)
    txn_date        = models.DateTimeField(null = True,blank = True  )


class chess (models.Model):
    chess_user = models.OneToOneField(User, on_delete = models.CASCADE,)
    Full_name   = models.CharField(max_length=50, blank=False, null=True)
    category = models.CharField(verbose_name="Contact",choices=C_CATEGORY, max_length=12, blank=False)
    contact     = models.PositiveIntegerField(verbose_name="Contact",validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)] , blank=False)
    addess     = models.CharField(verbose_name="Address",max_length=50, blank=False, null=True)
    txn_date        = models.DateTimeField(null = True,blank = True  )
    payment         = models.BooleanField(default = False)
    order_id        = models.CharField(max_length = 20,blank = True,null = True)


class FHS (models.Model):
    FHS_user    = models.OneToOneField(User, on_delete = models.CASCADE,)
    Full_name   = models.CharField(max_length=50, blank=False, null=True)
    category    = models.CharField(verbose_name="Category",choices=F_CATEGORY ,max_length=12, blank=False)
    contact     = models.PositiveIntegerField(verbose_name="Contact",validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)] , blank=False)
    addess     = models.CharField(verbose_name="Address",max_length=50, blank=False, null=True)
    payment         = models.BooleanField(default = False)
    txn_date        = models.DateTimeField(null = True,blank = True  )
    order_id        = models.CharField(max_length = 20,blank = True,null = True)

