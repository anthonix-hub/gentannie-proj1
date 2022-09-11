from os import name
from django.contrib.auth import views as auth_views
from django.urls import path,include
# from .views import signupview, update_view
from . import views
from gentannieReferal.views import *

urlpatterns = [
    path('countdown', views.countdown, name='countdown'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('transaction_history_page', views.transact_history, name='transact_history'),
    path('notification_page', views.notification, name='notification'),
    path('profile_page', views.account_detail_profile, name='account_detail_profile'),
    path('referal_views', views.Referal_views, name='Referal_views'),
    # path('<user_id>/update_view', update_view),

    # ******** deposits urls *********
    path('deposit_page', views.deposit_page, name='deposit_page'),
    path('smart_pack', views.smart_pack, name='smart_pack'),
    path('super_pack', views.super_pack, name='super_pack'),
    path('supreme_pack', views.supreme_pack, name='supreme_pack'),
    # ******** / .deposits urls *********

    path('user_withdrawal', views.user_withdrawal_page, name='user_withdrawal_page'),
    path('smart_withdrawal_smart_page', views.smart_withdrawal, name='smart_withdrawal'),
    path('SuperSmart_withdrawal_SuperSmart_page', views.SuperSmart_withdrawal, name='SuperSmart_withdrawal_SuperSmart_page'),
    path('supreme_withdrawal_supreme_page', views.supreme_withdrawal_page, name='supreme_withdrawal_page'),

    # ********** payment confirmation_page ************
    path('comfirm_smart_payment', views.comfirm_smart_payment_page, name='comfirm_smart_payment_page'),
    path('comfirm_super_payment', views.comfirm_super_payment_page, name='comfirm_super_payment_page'),
    path('comfirm_supreme_payment', views.comfirm_supreme_payment_page, name='comfirm_supreme_payment_page'),
    # ********** / .payment confirmation_page ************

    path('', include('django.contrib.auth.urls')),
    path('signup', signup_view, name='signup_view'),
    path('logoutUser/', views.logoutUser, name='logoutUser'),
    
    path('statistics', views.statistics, name='statistics'),
    path('marketing_stat', views.marketing_stats, name='marketing_stats'),
    path('user_statistics', views.user_stats, name="user_stats")

    # path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),
    # name='password_change_done'),

    # path('password_change/', auth_views.PasswordChangeView.as_view(),
    # name='password_change'),

    # path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
    # name='password_reset_done'),

    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),

    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
    # name='password_reset_complete'),
]
