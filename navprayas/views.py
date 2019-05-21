from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login   #as it clashes with other login term
from .functions import *


from .forms import * #all the components from .form
import json
from django.views.decorators.csrf import csrf_exempt
from navprayas import checksum as Checksum
from django.contrib import messages
from django.core.mail import send_mail
#from django.contrib.auth.models import User

    



from secret import *
import string
import random
TRN_DIGITS = 9
def OID(size=TRN_DIGITS, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

MERCHANT_KEY = Secret.PAYMENT_MERCHANT_KEY
CHESS_FEE   = '15'
MTSE_FEE    = '25'
FHS_FEE     = '10'
PR_FEE      = '40'
# _FEE

# Create your views here.
def index(request):
    return render(request, 'navprayas/home_links/index.html', {})

def about(request):
    return render(request, 'navprayas/home_links/about.html', {})

def pay(request):
    return render(request, 'navprayas/paytm/pay.html', {})

def events(request):
    return render(request, 'navprayas/home_links/events.html', {})

def notifications(request):
    return render(request, 'navprayas/home_links/notifications.html', {})

def team(request):
    return render(request, 'navprayas/home_links/team.html', {})



def pay(user_id,price,form):
    oid = 'O19'+OID()
    form.order_id = oid
    form.save() 
    

    param_dict = {
            'MID': Secret.PAYMENT_MERCHANT_ID,
            'ORDER_ID': oid,
            'TXN_AMOUNT': price,
            'CUST_ID': str(user_id),
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'DEFAULT',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL':'http://www.navprayas.in/handlerequest/',
            'INDUSTRY_TYPE_ID' : 'Retail',
            'CHANNEL_ID' : 'WEB',

            }
    param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
    return param_dict

def status(user):
    status_dict ={}
    # rangotsav1 = rangotsav.objects.filter(rangotsav_user_id = user.id ).first()
    # if rangotsav1 is not None   :
    #     status_dict['RANGOTSAV'] = '<span class="text-success">SUCCESSFUL</span>'
    # else :
    #     status_dict['RANGOTSAV'] = "<a href = '/rangotsav_register/'><b> Click Here </b></a> to register"
    # fhs1 = FHS.objects.filter(FHS_user_id = user.id ).first()
    # if fhs1 is not None   :
    #     if fhs1.payment :
    #         status_dict['FREE HAND SKETCHING'] ='<span class="text-success">SUCCESSFUL </span> '+str(fhs1.order_id)
    #     else :
    #         status_dict['FREE HAND SKETCHING'] = "<a href = '/FHS_register/'> <b>Click Here</b> </a> to pay"
    # else :
    #     status_dict['FREE HAND SKETCHING'] = "<a href = '/FHS_register/'><b>Click Here </b></a> to register"
    pr1 = PR.objects.filter(PR_user_id = user.id ).first()
    if pr1 is not None   :
        if pr1.payment :
            status_dict['PUZZLE RACE'] = '<span class="text-success">SUCCESSFUL </span> ' +str(pr1.order_id) 
        else :
            status_dict['PUZZLE RACE'] = "<a href = '/PR_register/'> <b>Click Here </b></a> to pay"
    else :
        status_dict['PUZZLE RACE'] = "<a href = '/PR_register/'> <b>Click Here </b></a> to register"
    mtse1 = MTSE.objects.filter(MTSE_user_id = user.id ).first()
    if mtse1 is not None   :
        if mtse1.payment :
            status_dict['MTSE'] ='<span class="text-success">SUCCESSFUL</span> '+ str(mtse1.order_id)
        else :
            status_dict['MTSE'] = "<a href = '/MTSE_register/'> <b>Click Here </b></a> to pay"
    else :
        status_dict['MTSE'] = "<a href = '/MTSE_register/'> <b>Click Here </b></a> to register"
    chess1 = chess.objects.filter(chess_user_id = user.id ).first()
    if chess1 is not None   :
        if chess1.payment :
            status_dict['CHESS'] = '<span class="text-success">SUCCESSFUL </span> '+str(chess1.order_id)
        else :
            status_dict['CHESS'] = "<a href = '/chess_register/'> <b>Click Here </b></a> to pay"
    else :
        status_dict['CHESS'] = "<a href = '/chess_register/'> <b>Click Here </b></a> to register"
    # spr1 = SPR.objects.filter(SPR_user_id = user.id ).first()
    # if spr1 is not None   :
    #     status_dict['POEM & STORY WRITIING'] = '<span class="text-success">SUCCESSFUL</span>'
    # else :
    #     status_dict['POEM & STORY WRITIING'] = "<a href = '/SPR_register/'> <b>Click Here </b></a> to register"
    return status_dict
    




# *************************
# signup form
# *************************
@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    np_email = Secret.USERID_FOR_EMAIL
    if request.method == 'POST':
        form = request.POST
        print(form)
        response_dict = {}
        for i in form.keys():
            response_dict[i] = form[i]
            if i == 'CHECKSUMHASH':
                checksum = form[i]

        verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
        if verify:
            if response_dict['RESPCODE'] == '01':
                print('order successful')
                oid = response_dict['ORDERID']
                txndate = response_dict['TXNDATE']
                mtse = MTSE.objects.filter(order_id = oid).first()
                if mtse is not None:
                    mtse.payment = True
                    mtse.txn_date = txndate
                    mtse.save()
                    email = mtse.MTSE_user.email
                    sub = "Confirmation for your registration"
                    mgs = "You  have succesfullly registered for MTSE.\n Your application ID is " + str(oid) + ".\n\n\n\n\n\n\n\n" + "NAVPRAYAS OFFICE\n 1st floor Durga Asthan Market \nManpur Patwatoli Gaya,PIN-823003\nBihar, India"
                    send_mail(sub, mgs, np_email, [email])

                pr = PR.objects.filter(order_id = oid).first()
                if pr is not None:
                    pr.payment = True
                    pr.txn_date = txndate
                    pr.save()
                    email=pr.PR_user.email
                    sub = "Confirmation for your registration"
                    mgs = "You  have succesfullly registered for PUZZLE RACE.\n Your application ID is " + str(oid) + ".\n\n\n\n\n\n\n\n" + "NAVPRAYAS OFFICE\n 1st floor Durga Asthan Market \nManpur Patwatoli Gaya,PIN-823003\nBihar, India"
                    send_mail(sub, mgs, np_email, [email])

                # fhs = FHS.objects.filter(order_id = oid).first()
                # if fhs is not None:
                #     fhs.payment = True
                #     fhs.txn_date = txndate
                #     fhs.save()
                #     email=fhs.FHS_user.email
                #     print(oid)
                #     sub="Confirmation for your registration"
                #     mgs="You  have succesfullly registered for FREE HAND SKETCHING  .\n Your application ID is " + str(oid) + ".\n\n\n\n\n\n\n\n" + "NAVPRAYAS OFFICE\n 1st floor Durga Asthan Market \nManpur Patwatoli Gaya,PIN-823003\nBihar, India"
                #     send_mail(sub, mgs, np_email, [email])

                ches = chess.objects.filter(order_id = oid).first()
                if ches is not None:    # please donot rectify ches
                    ches.payment = True
                    ches.txn_date = txndate
                    ches.save()
                    email=ches.chess_user.email
                    sub = "Confirmation for your registration"
                    mgs = "You  have succesfullly registered for CHESS.\n Your application ID is " + str(oid) + ".\n\n\n\n\n\n\n\n" + "NAVPRAYAS OFFICE\n 1st floor Durga Asthan Market \nManpur Patwatoli Gaya,PIN-823003\nBihar, India"
                    send_mail(sub, mgs, np_email, [email])



            else:
                print('order was not successful because' + response_dict['RESPMSG'])
        return render(request, 'navprayas/paytm/status.html', {'response': response_dict})
    return redirect('index')











def profile(request):
    if not request.user.is_authenticated :
        messages.info(request,'Please login first to proceed')
        return redirect('login')
    statuses=status(request.user)
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST,instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            return redirect('profile')

    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'p_form': p_form,
        'status': statuses,
    }

    return render(request, 'navprayas/users/profile.html', context)






def register(request):
    if request.method == 'POST':
        gender = request.POST.get("gender")
        birth_date = request.POST.get("birth_date")
        form = SignUpForm(request.POST)
        form2 = SignUpFormProfile(request.POST)
        if form.is_valid() and form2.is_valid():
            email       = form.cleaned_data['email']

            #check if username already exits
            if User.objects.filter(email = email).exists():
                messages.warning(request, 'Email already exists !!!')
                form = SignUpForm(request.POST)
                context = {
                'form' : form,
                'form2' : form2,
                }
                return render(request, 'navprayas/users/signup.html',context)
            #create user
            password1   = form.cleaned_data['password1']
            password2   = form.cleaned_data['password2']
            
            # check if passwords are same
            if not (password1 == password2):
                messages.warning(request, 'Passwords do not match !!!')
                form = SignUpForm(request.POST)
                context = {
                'form' : form,
                'form2' : form2,
                }
                return render(request, 'navprayas/users/signup.html',context)
            #finally creating user with same email and username
            user = User.objects.create_user(email,email,password1)
            user.first_name = form.cleaned_data['first_name']   
            user.last_name = form.cleaned_data['last_name']

            user.save()
            a = Profile.objects.filter(user = user).first()
            a.gender = gender
            a.birth_date = birth_date
            a.save()
            sub = "Successful signup"
            mgs = "Your account has been created successfully."
            send_mail(sub, mgs, email, [email])
            messages.success(request, 'Your account is created successfully | SignIn Now !!!')
            return redirect('login')
        else:
            messages.warning(request, 'Please Enter Valid Details')
            form = SignUpForm(request.POST)
            context = {
            'form' : form,
            'form2' : form2,
            }
            return render(request, 'navprayas/users/signup.html',context)
        
    else:
        form = SignUpForm()
        form2 = SignUpFormProfile()
    context = {
        'form' : form,
        'form2' : form2,
    }    
    return render(request, 'navprayas/users/signup.html',context)


















# /////////////////////////
# Exam_forms
# /////////////////////////


# *************************
# MTSE
# *************************

def MTSE_register(request):
    if not request.user.is_authenticated :
        messages.info(request,'Please login first to proceed')
        return redirect('login')
    MTSE_filled = MTSE.objects.filter(MTSE_user=request.user).first() #if returns none then u can fill form
    if MTSE_filled is None: #if form is filled
        if request.method == 'POST':
            form = MTSE_form(request.POST)
            if form.is_valid():
                MTSE_filled = form.save(commit=False)
                MTSE_filled.MTSE_user=request.user
                MTSE_filled.save()
                #form filled
                #proceed for paymment
                param_dict = pay(request.user.id,MTSE_FEE,MTSE_filled)
                return render(request, 'navprayas/paytm/paytm.html', {'param_dict': param_dict})
            else:
                messages.warning(request, 'Please enter valid details')
                form = MTSE_form(request.POST)
                return render(request, 'navprayas/exam_forms/MTSE_register.html', {'form': form})
        else:
            form = MTSE_form()
            return render(request, 'navprayas/exam_forms/MTSE_register.html', {'form': form})           
    elif MTSE_filled.payment is False:
        if request.method == 'POST' :
            form = MTSE_form(request.POST,instance=request.user.mtse)

            if form.is_valid() :
                MTSE_filled = form.save()
                param_dict = pay(request.user.id,MTSE_FEE,MTSE_filled)
                return render(request, 'navprayas/paytm/paytm.html', {'param_dict': param_dict})
            else:
                messages.warning(request, 'Please enter valid details')
                form = MTSE_form(instance=request.user.mtse)
                return render(request, 'navprayas/exam_forms/MTSE_register.html', {'form': form})
        else:
            form = MTSE_form(instance=request.user.mtse)
            return render(request, 'navprayas/exam_forms/MTSE_register.html', {'form': form})
    else :
        return render(request, 'navprayas/home_links/submitted.html', {})





# *************************
# FHS
# *************************


def FHS_register(request):
    return redirect('index')
    if not request.user.is_authenticated :
            messages.info(request,'Please login first to proceed')
            return redirect('login')    
    FHS_filled = FHS.objects.filter(FHS_user=request.user).first() #if returns none then u can fill form

    if FHS_filled is None:
        if request.method == 'POST':
            form = FHS_form(request.POST)
            if form.is_valid():
                FHS_filled = form.save(commit=False)
                FHS_filled.FHS_user=request.user
                FHS_filled.save()
                param_dict = pay(request.user.id,FHS_FEE,FHS_filled)
                return render(request, 'navprayas/paytm/paytm.html', {'param_dict': param_dict})
            else:
                messages.warning(request, 'Please enter valid details')
                form = FHS_form(request.POST)
                return render(request, 'navprayas/exam_forms/FHS_register.html', {'form': form})

        else:
            form = FHS_form() 
            return render(request, 'navprayas/exam_forms/FHS_register.html', {'form': form})           

# if payment is not done but form is filled               
    elif FHS_filled.payment is False:
        if request.method == 'POST' :
            form = FHS_form(request.POST,instance=request.user.fhs)
            if form.is_valid() :
                FHS_filled=form.save()
                param_dict = pay(request.user.id,FHS_FEE,FHS_filled)
                return render(request, 'navprayas/paytm/paytm.html', {'param_dict': param_dict})
            else:
                messages.warning(request, 'Please enter valid details')
                form = FHS_form(instance=request.user.fhs)
                return render(request, 'navprayas/exam_forms/FHS_register.html', {'form': form})
        else:
            form = FHS_form(instance=request.user.fhs)
            return render(request, 'navprayas/exam_forms/FHS_register.html', {'form': form})
    else:
        return render(request, 'navprayas/home_links/submitted.html', {})



def chess_register(request):
    if not request.user.is_authenticated :
        messages.info(request,'Please login first to proceed')
        return redirect('login')
    chess_filled = chess.objects.filter(chess_user=request.user).first() #if returns none then u can fill form

    if chess_filled is None:
        if request.method == 'POST':
            form = chess_form(request.POST)
            if form.is_valid():
                chess_filled = form.save(commit=False)
                chess_filled.chess_user=request.user
                chess_filled.save()
                param_dict = pay(request.user.id,CHESS_FEE,chess_filled)
                return render(request, 'navprayas/paytm/paytm.html', {'param_dict': param_dict})
            else:
                messages.warning(request, 'Please enter valid details')
                form = chess_form(request.POST)
                return render(request, 'navprayas/exam_forms/chess_register.html', {'form': form})
        else:
            form = chess_form() 
            return render(request, 'navprayas/exam_forms/chess_register.html', {'form': form})           

# if payment is not done but form is filled               
    elif chess_filled.payment is False:
        if request.method == 'POST' :
            form = chess_form(request.POST,instance=request.user.chess)
            if form.is_valid() :
                chess_filled=form.save()
                param_dict = pay(request.user.id,CHESS_FEE,chess_filled)
                return render(request, 'navprayas/paytm/paytm.html', {'param_dict': param_dict})
            else:
                messages.warning(request, 'Please enter valid details')
                form = chess_form(instance = request.user.chess)
                return render(request, 'navprayas/exam_forms/chess_register.html', {'form': form})
        else:
            form = chess_form(instance=request.user.chess)
            return render(request, 'navprayas/exam_forms/chess_register.html', {'form': form})
    else:
        return render(request, 'navprayas/home_links/submitted.html', {})


def PR_register(request):
    if not request.user.is_authenticated :
        messages.info(request,'Please login first to proceed')
        return redirect('login')
    PR_filled = PR.objects.filter(PR_user=request.user).first() #if returns none then u can fill form

    if PR_filled is None:
        if request.method == 'POST':
            form = PR_form(request.POST)
            if form.is_valid():
                PR_filled = form.save(commit=False)
                PR_filled.PR_user=request.user
                PR_filled.save()
                param_dict = pay(request.user.id,PR_FEE,PR_filled)
                return render(request, 'navprayas/paytm/paytm.html', {'param_dict': param_dict})
            else:
                messages.warning(request, 'Please enter valid details')
                form = PR_form(request.POST)
                return render(request, 'navprayas/exam_forms/PR_register.html', {'form': form})
        else:
            form = PR_form() 
            return render(request, 'navprayas/exam_forms/PR_register.html', {'form': form})           

# if payment is not done but form is filled               
    elif PR_filled.payment is False:
        if request.method == 'POST' :
            form = PR_form(request.POST,instance=request.user.pr)
            if form.is_valid() :
                PR_filled=form.save()
                param_dict = pay(request.user.id,PR_FEE,PR_filled)
                return render(request, 'navprayas/paytm/paytm.html', {'param_dict': param_dict})
            else:
                messages.warning(request, 'Please enter valid details')
                form = PR_form(instance=request.user.pr)
                return render(request, 'navprayas/exam_forms/PR_register.html', {'form': form})

        else:
            form = PR_form(instance=request.user.pr)
            return render(request, 'navprayas/exam_forms/PR_register.html', {'form': form})
    else:
        return render(request, 'navprayas/home_links/submitted.html', {})
# *************************
# rangotsav
# *************************
def rangotsav_register(request):
    return redirect('index')
    if not request.user.is_authenticated :
        messages.info(request,'Please login first to proceed')
        return redirect('login')
    rangotsav_filled = rangotsav.objects.filter(rangotsav_user=request.user).first() #if returns none then u can fill form
    if rangotsav_filled is None:
        if request.method == 'POST':
            form = rangotsav_form(request.POST)
            if form.is_valid():
                rangotsav_filled = form.save(commit=False)
                rangotsav_filled.rangotsav_user=request.user
                rangotsav_filled.save()
                return redirect('index')
        else:
            form = rangotsav_form()
    else:
        return render(request, 'navprayas/home_links/submitted.html', {})
    return render(request, 'navprayas/exam_forms/rangotsav_register.html', {'form': form})

# *************************
# PR
# *************************

# *************************
# SPR
# *************************
def SPR_register(request):
    return redirect('index')
    if not request.user.is_authenticated :
        messages.info(request,'Please login first to proceed')
        return redirect('login')
    SPR_filled = SPR.objects.filter(SPR_user=request.user).first() #if returns none then u can fill form

    if SPR_filled is None:
        if request.method == 'POST':
            form = SPR_form(request.POST)
            if form.is_valid():
                SPR_filled = form.save(commit=False)
                SPR_filled.SPR_user=request.user
                SPR_filled.save()
                
                return redirect('index')
        else:
            form = SPR_form()
            

    else:
        return render(request, 'navprayas/home_links/submitted.html', {})
    return render(request, 'navprayas/exam_forms/SPR_register.html', {'form': form})

# *************************
# chess
# *************************



        
        

