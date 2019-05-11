from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    # *****************************
    # urls for home_links
    # *****************************

    path('index/', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('events/', views.events, name='events'),
    path('notifications/', views.notifications, name='notifications'),
    path('team/', views.team, name='contact'),
    path('', views.index, name='index'),

    # *****************************
    # urls for registering to exams
    # *****************************
	path('signup/', views.register, name='signup'),
    path('profile/', views.profile, name='profile'),  #not created the profile
    path('login/', auth_views.LoginView.as_view(template_name ='navprayas/users/login.html'), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(template_name= 'navprayas/users/logout.html'), name='logout'),


    # *****************************
    # urls for Forget Password
    # *****************************

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name= 'navprayas/users/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name= 'navprayas/users/password_reset_done.html'), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name= 'navprayas/users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name= 'navprayas/users/password_reset_complete.html'), name='password_reset_complete'),

    #path('password_reset/', auth_views.password_reset, name='password_reset'),
    #path('password_reset/done/', auth_views.password_reset_done, name='password_reset_done'),
    #path('reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
    #    auth_views.password_reset_confirm, name='password_reset_confirm'),
    #path('reset/done/', auth_views.password_reset_complete, name='password_reset_complete'),

    #path('', include('django.contrib.auth.urls')),

    # *****************************
    # urls for registering to exams
    # *****************************

    path('MTSE_register/', views.MTSE_register, name='MTSE_register'),
    path('PR_register/', views.PR_register, name='PR_register'),
    path('SPR_register/', views.SPR_register, name='SPR_register'),
    path('rangotsav_register/', views.rangotsav_register, name='rangotsav_register'),
    path('FHS_register/', views.FHS_register, name='FHS_register'),
    path('chess_register/', views.chess_register, name='chess_register'),
    # path('mail/', views.Mail, name='mail'),
    path("payment/", views.payment, name="payment"),
    path("handlerequest/", views.handlerequest, name="handlerequest"),
    # path("pay/", views.pay, name="pay"),

]
