# from .models import *
# from django.http import HttpResponse, JsonResponse
# from django.shortcuts import render, redirect



# def profile_update_required(function):
#     def wrapper(request, *args, **kwargs):
#         user=request.user
#         if user.is_authenticated:
#             techrep = Techrep.objects.filter(user=user).first()
#             if techrep.is_verified:
#                 return function(request, *args, **kwargs)
#             else:
#                 return HttpResponse("Not verified yet")           
#         else:
#             return redirect("/techrep/login")
#     return wrapper