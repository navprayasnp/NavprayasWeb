from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login   #as it clashes with other login term
from .forms import * #all the components from .form
import json
from django.views.decorators.csrf import csrf_exempt
from navprayas import checksum as Checksum
from django.contrib import messages 

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



# *************************
# signup form
# *************************
@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
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
                pr = PR.objects.filter(order_id = oid).first()
                if pr is not None:
                    pr.payment = True
                    pr.txn_date = txndate
                    pr.save()
                fhs = FHS.objects.filter(order_id = oid).first()
                if fhs is not None:
                    fhs.payment = True
                    fhs.txn_date = txndate
                    fhs.save()
                ches = chess.objects.filter(order_id = oid).first()
                if ches is not None:    # please donot rectify ches
                    ches.payment = True
                    ches.txn_date = txndate
                    ches.save()
                



            else:
                print('order was not successful because' + response_dict['RESPMSG'])
        return render(request, 'navprayas/paytm/status.html', {'response': response_dict})
    return redirect('index')


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
            'CALLBACK_URL':'http://127.0.0.1:8000/handlerequest/',
            'INDUSTRY_TYPE_ID' : 'Retail',
            'CHANNEL_ID' : 'WEB',

            }
    param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
    return param_dict




@login_required
def chess_register(request):

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
            form = chess_form()
            
    elif chess_filled.payment is False:
        param_dict = pay(request.user.id,CHESS_FEE,chess_filled)
        return render(request, 'navprayas/paytm/paytm.html', {'param_dict': param_dict})
    else:
        return render(request, 'navprayas/home_links/submitted.html', {})
    return render(request, 'navprayas/exam_forms/chess_register.html', {'form': form})









def register(request):
    if request.method == 'POST':
        gender = request.POST.get("gender")
        birth_date = request.POST.get("birth_date")
        form = SignUpForm(request.POST)
        form2 = SignUpFormProfile(request.POST)
        if form.is_valid() and form2.is_valid():
            email = form.cleaned_data['email']
            if User.objects.filter(email = email).exists():
                messages.warning(request, 'username already exists')
                form = SignUpForm(request.POST)
                context = {
                'form' : form,
                'form2' : form2,
                }
                return render(request, 'navprayas/users/signup.html',context)
            user = form.save(commit = False)
            user.username = user.email  #username and email is same so we are not using username
            user.save()
            a = Profile.objects.filter(user = user).first()
            a.gender = gender
            a.birth_date = birth_date
            a.save()
            return redirect('index')
    else:
        form = SignUpForm()
        form2 = SignUpFormProfile()
    context = {
        'form' : form,
        'form2' : form2,
    }    
    return render(request, 'navprayas/users/signup.html',context)



@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'navprayas/users/profile.html', context)














# /////////////////////////
# Exam_forms
# /////////////////////////


# *************************
# MTSE
# *************************
@login_required
def MTSE_register(request):
    MTSE_filled = MTSE.objects.filter(MTSE_user=request.user).first() #if returns none then u can fill form
    form = MTSE_form()
    if MTSE_filled is None:
        if request.method == 'POST':
            form = MTSE_form(request.POST)
            if form.is_valid():
                MTSE_filled = form.save(commit=False)
                MTSE_filled.MTSE_user=request.user
                MTSE_filled.save()
                param_dict = pay(request.user.id,MTSE_FEE,MTSE_filled)
                return render(request, 'navprayas/paytm/paytm.html', {'param_dict': param_dict})
        else:
            form = MTSE_form()           
    elif MTSE_filled.payment is False:
        print('**********************')
        form = MTSE_form() 
        print(form.board)
        print('***************')
             
        return render(request, 'navprayas/home_links/proceed.html', {'form': form})

    else:
        return render(request, 'navprayas/home_links/submitted.html', {})
    return render(request, 'navprayas/exam_forms/MTSE_register.html', {'form': form})

@login_required
def already_applied(request):
    pass
    # MTSE_filled = MTSE.objects.filter(MTSE_user=request.user).first() #if returns none then u can fill form
    # if MTSE_filled is None:
    #     if request.method == 'POST':
    #         form = MTSE_form(request.POST)
    #         if form.is_valid():
    #             MTSE_filled = form.save(commit=False)
    #             MTSE_filled.MTSE_user=request.user
    #             MTSE_filled.save()
    #             param_dict = pay(request.user.id,MTSE_FEE,MTSE_filled)
    #             return render(request, 'navprayas/paytm/paytm.html', {'param_dict': param_dict})
    # elif MTSE_filled.payment is False:
    #     param_dict = pay(request.user.id,MTSE_FEE,MTSE_filled)
    #     print(param_dict)
    #     return render(request, 'navprayas/paytm/paytm.html', {'param_dict': param_dict})

    # else:
    #     return render(request, 'navprayas/home_links/submitted.html', {})
    # if request.method == 'GET':
    #     form = MTSE_form()
    # return render(request, 'navprayas/exam_forms/MTSE_register.html', {'form': form})





# *************************
# FHS
# *************************
@login_required
def FHS_register(request):
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
            form = FHS_form() 
# if payment is not done but form is filled               
    elif FHS_filled.payment is False:
        param_dict = pay(request.user.id,FHS_FEE,FHS_filled)
        return render(request, 'navprayas/paytm/paytm.html', {'param_dict': param_dict})
    else:
        return render(request, 'navprayas/home_links/submitted.html', {})
    return render(request, 'navprayas/exam_forms/FHS_register.html', {'form': form})




# *************************
# rangotsav
# *************************
@login_required
def rangotsav_register(request):
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
@login_required
def PR_register(request):

    PR_filled = PR.objects.filter(PR_user=request.user).first() #if returns none then u can fill form
    if PR_filled is None:
        if request.method == 'POST':
            form = PR_form(request.POST)
            if form.is_valid():
                PR_filled = form.save(commit=False)
                PR_filled.PR_user=request.user
                PR_filled.save()
                param_dict = pay(request.user.id,PR_FEE,PR_filled)
                print("*************************************************")
                return render(request, 'navprayas/paytm/paytm.html', {'param_dict': param_dict})

        else:
            print("################################")
            form = PR_form()
           

    elif PR_filled.payment is False:
        param_dict = pay(request.user.id,PR_FEE,PR_filled)
        return render(request, 'navprayas/paytm/paytm.html', {'param_dict': param_dict})
    else:
        return render(request, 'navprayas/home_links/submitted.html', {})
    return render(request, 'navprayas/exam_forms/PR_register.html', {'form': form})

# *************************
# SPR
# *************************
@login_required
def SPR_register(request):

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


# def payment(request):
#     if request.method=="POST":
#         # Request paytm to transfer the amount to your account after payment by user
#         param_dict = {

#                 'MID': 'iArBym81738942720672',
#                 'ORDER_ID': '2',
#                 'TXN_AMOUNT': '30',
#                 'CUST_ID': 'kena421@gmail.com',
#                 'INDUSTRY_TYPE_ID': 'Retail',
#                 'WEBSITE': 'WEBSTAGING',
#                 'CHANNEL_ID': 'WEB',
#                 'CALLBACK_URL':'http://127.0.0.1:8000/handlerequest/',

#         }
#         param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
#         return render(request, 'navprayas/paytm/paytm.html', {'param_dict': param_dict})

#     return render(request, 'navprayas/paytm/pay.html')

