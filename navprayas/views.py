from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login   #as it clashes with other login term
from .forms import * #all the components from .form
import json
from django.views.decorators.csrf import csrf_exempt
from navprayas import checksum as Checksum

MERCHANT_KEY = 'WVQB3eC57Bdu3&N_'
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

@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'navprayas/paytm/status.html', {'response': response_dict})

def payment(request):
    if request.method=="POST":
        # Request paytm to transfer the amount to your account after payment by user
        param_dict = {

                'MID': 'iArBym81738942720672',
                'ORDER_ID': '2',
                'TXN_AMOUNT': '30',
                'CUST_ID': 'kena421@gmail.com',
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/handlerequest/',

        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'navprayas/paytm/paytm.html', {'param_dict': param_dict})

    return render(request, 'navprayas/paytm/pay.html')

# *************************
# signup form
# *************************


def register(request):
    if request.method == 'POST':
        gender = request.POST.get("gender")
        birth_date = request.POST.get("birth_date")
        form = SignUpForm(request.POST)
        form2 = SignUpFormProfile(request.POST)
        if form.is_valid() and form2.is_valid:
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
        p_form = ProfileUpdateForm(request.POST,
                                #    request.FILES,
                                   instance=request.user.profile)
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


# def Mail(request):
#     if request.method== 'POST':
#         to = request.POST["to"]
#         subject = request.POST["subject"]
#         body = request.POST["body"]
#         mail(to,subject,body)
        

#     return render(request, 'navprayas/mail.html', {})












# /////////////////////////
# Exam_forms
# /////////////////////////


# *************************
# MTSE
# *************************
@login_required
def MTSE_register(request):
    MTSE_filled = MTSE.objects.filter(MTSE_user=request.user).first() #if returns none then u can fill form
    if MTSE_filled is None:
        if request.method == 'POST':
            form = MTSE_form(request.POST)
            if form.is_valid():
                MTSE_filled = form.save(commit=False)
                MTSE_filled.MTSE_user=request.user
                MTSE_filled.save()
                return redirect('index')
        else:
            form = MTSE_form()           

    else:
        return render(request, 'navprayas/home_links/submitted.html', {})
    return render(request, 'navprayas/exam_forms/MTSE_register.html', {'form': form})





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
                return redirect('index')
        else:
            form = FHS_form()           

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
                
                return redirect('index')
        else:
            form = PR_form()
           

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
                
                return redirect('index')
        else:
            form = chess_form()
            

    else:
        return render(request, 'navprayas/home_links/submitted.html', {})
    return render(request, 'navprayas/exam_forms/chess_register.html', {'form': form})



