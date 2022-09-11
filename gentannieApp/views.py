# django.contrib.admin.options import FORMFIELD_FOR_DBFIELD_DEFAULTS
from django.core.files.base import File
from django.db import reset_queries
from django.db.models.expressions import F
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView,UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from django.core.mail import message, send_mail
from django.contrib import messages
from .models import *
from django.contrib.auth.forms import UserCreationForm
from gentannieReferal.models import user_referal
from gentannieReferal.form import referForm

from gent_marketering.models import *

from .form import *
from datetime import date, datetime, timedelta,date,timezone
from time import sleep,thread_time, time
import time
import threading

from django.db.models import Sum,Avg


smart_pack_details = smart.objects.all()
super_pack_details = smart.objects.all()
supreme_pack_details = smart.objects.all()

def countdown(request):
    return render(request,'gentannieReferal/countdown_lauch.html',None)        

def Referal_withdrawal_alert(get_user):
    EMAIL_HOST_USER = 'anthonix1759@gmail.com'
    subject =  'withdrawal of referral bonus is being requested by %s'%get_user
    message = 'Admin someone just made a request to withdraw referral bonus'
    # recepient = ['informaniac665@gmail.com']
    try:
        send_mail(subject,
            message, 'support@gentannie.com', ['support@gentannie.com'], fail_silently=False)
    except:
        print('MAIL not sent')

def dashboard(request):
    recom_profiles = user_referal.objects.get(user=request.user)
    my_recs = recom_profiles.get_recommended_profiles()

    recom_len =  len(my_recs)
    recomms_rewards = recom_len*1000

    # *******************  referral bonus request ******************
    if request.method=='POST':
        referal_req_form = referForm(request.POST)
        if referal_req_form.is_valid():
            request_mark = user_referal.objects.all().filter(numbers_refered__gte=3).filter(user=request.user)
            request_mark.update(request_bonus=True, requested_bonus=recomms_rewards,total_withdrawed_bonus=F('total_withdrawed_bonus')+recomms_rewards)
            # request_mark.update(request_bonus=True, requested_bonus=10000,total_withdrawed_bonus=F('total_withdrawed_bonus')+10000)

            request_marked = user_referal.objects.all().filter(recommended_by = request.user)
            request_marked.update(recommended_by= None)

            # ****** mailing Admin ****
            get_user = request.user
            Referal_withdrawal_alert(get_user)
            # / .****** mailing Admin *****
        return redirect('dashboard')
    else:
        referal_req_form = referForm()

    # ******************* / .referral bonus request ****************

    user_item_prog = users_investment_progress(user=request.user)
    user_progress_feed = users_investment_progress.objects.all().filter(user=request.user)
    
    users_data = users_investment_progress(user=request.user)
    
    smart_data = smart.objects.all().filter(username=request.user)
    super_data = SuperSmart.objects.all().filter(username=request.user)
    supreme_data = supreme.objects.all().filter(username=request.user)

    # ********** Referal Section ***********
    recom_profiles = user_referal.objects.get(user=request.user)
    my_recs = recom_profiles.get_recommended_profiles()

    recom_len =  len(my_recs)
    recomms_rewards = recom_len * 1000

    # referal_no_check = user_referal.objects.all().filter(user=request.user).filter(numbers_refered__gte=10).exists()
    referal_no_check = user_referal.objects.all().filter(user=request.user).filter(numbers_refered=10).exists()
    referal_no = user_referal.objects.all().filter(user=request.user)
    referal_no.update(numbers_refered=recom_len, Referal_bonus=recomms_rewards)

    Num_refered = user_referal.objects.all().filter(user=request.user)

    # ********** / .Referal Section ***********
    user_referal_profile = user_referal.objects.filter(user=request.user)
    pic = users_details.objects.all().filter(username=request.user)
    smart_progress_feed = users_investment_progress.objects.all().filter(user=request.user).filter(package='smart')
    super_progress_feed = users_investment_progress.objects.all().filter(user=request.user).filter(package='SuperSmart')
    supreme_progress_feed = users_investment_progress.objects.all().filter(user=request.user).filter(package='supreme')

    context = {
        'users_data':users_data,
        'user_progress_feed':user_progress_feed,
        'recomms_rewards':recomms_rewards,
        'user_referal_profile':user_referal_profile,
        'recom_len':recom_len,
        'smart_data':smart_data,
        'super_data':super_data,
        'supreme_data':supreme_data,
        'pic':pic,
        'smart_progress_feed':smart_progress_feed,
        'super_progress_feed':super_progress_feed,
        'supreme_progress_feed':supreme_progress_feed,
        'referal_no_check':referal_no_check,
        'referal_req_form':referal_req_form,
        'Num_refered':Num_refered,
        
    }
    return render(request, 'gentannieReferal/dash/dash_index.html', context)

def Referal_views(request,  *args, **kwargs):
    code = str(kwargs.get('ref_code'))
    try:
        profiles = user_referal.objects.get(code=code)
        request.session['ref_profile'] = profiles.id
        print('id', profiles.id)
    except:
        pass
    session = request.session.get_expiry_age()
    context = {
        'session':session
    }
    # return render(request, 'gentannieReferal/dash/referal_view.html', context)
    return render(request, 'gentannieApp/dash/Referal_page.html', context)

def my_recomms_views(request):
    recom_profiles = user_referal.objects.get(user=request.user)
    my_recs = recom_profiles.get_recommended_profiles()

    recom_len =  len(my_recs)
    recomms_rewards = recom_len*1000

    user_referal_profile = user_referal.objects.filter(user=request.user)

    context = {
        'recomms_rewards':recomms_rewards,
        'my_recs':my_recs,
        'user_referal_profile':user_referal_profile,
        'recom_len':recom_len,
    }
    return render (request, 'gentannieReferal/index2.html', context)

# ******** investment plans deposit Views *********
def deposit_page(request):
    user_smart_details = users_investment_progress.objects.all().filter(user=request.user).filter(package='smart')
    user_super_details = users_investment_progress.objects.all().filter(user=request.user).filter(package='SuperSmart')
    user_supreme_details = users_investment_progress.objects.all().filter(user=request.user).filter(package='supreme')

    smart_pack_check = smart.objects.all().filter(username=request.user)
    smart_pack_close = smart_pack_check.values().exists()

    super_pack_check = SuperSmart.objects.all().filter(username=request.user)
    super_pack_close = super_pack_check.values().exists()

    supreme_pack_check = supreme.objects.all().filter(username=request.user)
    supreme_pack_close = supreme_pack_check.values().exists()

    context={
        "user_smart_details":user_smart_details, 
        'smart_pack_check':smart_pack_check,
        'super_pack_check':super_pack_check,
        'supreme_pack_check':supreme_pack_check,
        'smart_pack_close':smart_pack_close,
        'super_pack_close':super_pack_close,
        'supreme_pack_close':supreme_pack_close
        
    }
    return render(request, 'gentannieApp/dash/dash_deposit.html',context)

def smart_pack(request):
    user_pack = smart(username=request.user)
    if request.method == 'POST':
        packform = smart_form(request.POST, request.FILES, instance=user_pack)
        if packform.is_valid():
            users_investment_progress.objects.filter(user=request.user)

            users_investment_progress.objects.filter(user=request.user)
            users_data = users_investment_progress(user=request.user)

            acc_plan = user_pack.plan_name
            acc_type = user_pack.account_type
            uploaded_proof = user_pack.payment_proof
            acc_plan = user_pack.plan_name
            pack = user_pack.plan

            if pack ==  'smart':
                span = '9 months'
            elif pack ==  'SuperSmart':
                span = '9 months'
            elif pack ==  'supreme':
                span = '9 months'

            if acc_plan ==  basic:
                amount_deposit = 20000
            elif acc_plan == standard:
                amount_deposit = 40000
            elif acc_plan == premium:
                amount_deposit = 60000
            elif acc_plan ==  bronze:
                amount_deposit = 80000
            elif acc_plan == super_bronze:
                amount_deposit = 100000
            elif acc_plan == silver:
                amount_deposit = 120000
            elif acc_plan == super_silver:
                amount_deposit = 140000
            elif acc_plan == Gold:
                amount_deposit = 200000

            # ******** Acc type Logics *******
            if acc_type == unlocked:
                interest = int(amount_deposit) * 0.35
                time_stamp = timedelta(days = 30)
            elif acc_type == locked:
                interest = int(amount_deposit) * 1.2
                time_stamp = timedelta(days = 30 * 3 ) 

            future_time = datetime.now() + time_stamp
            smart.objects.update_or_create(username=request.user, amount_deposited=amount_deposit, account_type=acc_type, ROI=interest, plan_name=pack, plan=acc_plan, payment_proof=uploaded_proof, )
            users_investment_progress.objects.all().filter(user=request.user).update_or_create(user=request.user, amount_deposited = amount_deposit, account_type=acc_type, ROI=interest, proof=uploaded_proof, plan=acc_plan, package=pack, life_span=span )

            deposit = str(amount_deposit)
            get_user = request.user
            deposit_sending(str(deposit), get_user)# sending Admin email for deposit alert

            return redirect('dashboard')
    else:
        packform = smart_form()
    context = {
        'packform':packform,
    }   
    return render(request, 'gentannieApp/dash/make_smart_deposit.html', context)

def super_pack(request):
    user_pack = SuperSmart(username=request.user)
    if request.method == 'POST':
        packform = super_form(request.POST, request.FILES, instance=user_pack)
        if packform.is_valid():
            users_investment_progress.objects.filter(user=request.user)

            acc_plan = user_pack.plan_name
            acc_type = user_pack.account_type
            uploaded_proof = user_pack.payment_proof
            pack = user_pack.plan

            span = '9 months'
            if pack ==  'SuperSmart':
                span = '9 months'
            elif pack ==  'supreme':
                span = '9 months'

            if acc_plan ==  basic:
                amount_deposit = 20000
            elif acc_plan == standard:
                amount_deposit = 40000
            elif acc_plan == premium:
                amount_deposit = 60000
            elif acc_plan ==  bronze:
                amount_deposit = 80000
            elif acc_plan == super_bronze:
                amount_deposit = 100000
            elif acc_plan == silver:
                amount_deposit = 120000
            elif acc_plan == super_silver:
                amount_deposit = 140000
            elif acc_plan == Gold:
                amount_deposit = 200000
            elif acc_plan ==  diamond:
                amount_deposit = 400000
            elif acc_plan == Ruby:
                amount_deposit = 600000
            elif acc_plan == peal:
                amount_deposit = 700000
            elif acc_plan ==  emerald:
                amount_deposit = 800000
            elif acc_plan == Jasper:
                amount_deposit = 900000

            # ******** Acc type Logics *******
            if acc_type == unlocked:
                interest = amount_deposit * 0.25
                time_stamp = timedelta(days = 30 )
            elif acc_type == locked:
                interest = int(amount_deposit) * 0.8
                time_stamp = timedelta(days = 30 * 3)

            future_time = datetime.now() + time_stamp
            SuperSmart.objects.update_or_create(username=request.user, amount_deposited=amount_deposit, account_type=acc_type, ROI=interest, plan_name=pack, plan=acc_plan, payment_proof=uploaded_proof, )
            users_investment_progress.objects.all().filter(user=request.user).update_or_create(user=request.user, amount_deposited = amount_deposit, account_type=acc_type, ROI=interest, proof=uploaded_proof, plan=acc_plan, package=pack, life_span=span)

            deposit = str(amount_deposit)
            get_user = request.user
            deposit_sending(deposit, get_user)# sending Admin email for deposit alert

            return redirect('dashboard')
    else:
        packform = super_form()

    context = {
        'packform':packform,
    }   
    # return render(request, 'gentannieApp/dash/dash_make_deposit.html', context)
    return render(request, 'gentannieApp/dash/make_super_deposit.html', context)

def supreme_pack(request):
    user_pack = supreme(username=request.user)
    
    if request.method == 'POST':
        supremepackform = supreme_form(request.POST, request.FILES, instance=user_pack)
        if supremepackform.is_valid():
            users_investment_progress.objects.filter(user=request.user)

            acc_plan = user_pack.plan_name
            pack = user_pack.plan
            uploaded_proof = user_pack.payment_proof

            if pack ==  'supreme':
                span = '9 months'
            else:
                span = '9 months'
            if acc_plan ==  Whale:
                amount_deposit = 1000000
            else:
                amount_deposit = 2000000

            interest = amount_deposit * 0.15
            future_time = datetime.now() + timedelta(days = 30)

            supreme.objects.update_or_create(username=request.user, amount_deposited=amount_deposit, ROI=interest, plan_name=pack, plan=acc_plan, payment_proof=uploaded_proof, )
            users_investment_progress.objects.all().filter(user=request.user).update_or_create(user=request.user, amount_deposited = amount_deposit, ROI=interest, proof=uploaded_proof, plan=acc_plan, package=pack, life_span=span )

            deposit = str(amount_deposit)
            get_user = request.user
            deposit_sending(deposit, get_user)# sending Admin email for deposit alert

            # user_profile = supremepackform.save()
            # user_profile.save()
            return redirect('dashboard')
    else:
        supremepackform = supreme_form()

    context = {
        'supremepackform':supremepackform,
    }   
    
    return render(request, 'gentannieApp/dash/make_supreme_deposit.html', context)
    # return render(request, 'gentannieReferal/dash/dash_profile.html', context)


# ************ withdrawal request **************
def user_withdrawal_page(request):
    user_progress_feed = users_investment_progress.objects.all().filter(user=request.user)

    smart_data = smart.objects.all().filter(username=request.user)
    super_data = SuperSmart.objects.all().filter(username=request.user)
    supreme_data = supreme.objects.all().filter(username=request.user)

    context = {
        'user_progress_feed':user_progress_feed,
        'smart_data':smart_data,
        'super_data':super_data,
        'supreme_data':supreme_data
        }
    return render(request,'gentannieApp/dash/withdrawal_page.html',context)

def smart_withdrawal(request):
    smart_opt = smart(username=request.user)
    if request.method == 'POST':
        smart_withdraw_form = smart_withdrawalForm(request.POST, instance=smart_opt)
        if smart_withdraw_form.is_valid:
            messages.success(request, 'Withdrawal request has been submitted!! wait for your account to be credited before you click on comfirm payment button ')
            req_user_option = smart.objects.filter(username=request.user)
            req_user_option.update(request=True)

            smart_pull_request = users_investment_progress.objects.filter(user=request.user).filter(package='smart')
            smart_pull_request.update(withdraw_request=True)

            get_user = request.user
            mail_sending(get_user)#sends Admin alert for user withdrawal request 

            return redirect('dashboard')
    else:
        smart_withdraw_form = smart_withdrawalForm()

    # smart_ROI = users_investment_progress(user=request.user)

    user_progress_update = users_investment_progress.objects.filter(user=request.user).filter(package='smart')
    current_date = datetime.now()
    today = date.isoformat(current_date)

    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='smart').filter(Due_date__lte=datetime.isoformat(current_date)).values().exists()
    context = {
        'smart_withdraw_form':smart_withdraw_form,
        'user_progress_update':user_progress_update,
        'today':today,
        'date_check':date_check,

    }
    return render(request, 'gentannieApp/dash/smart_withdrawal_page.html',context)

def SuperSmart_withdrawal(request):
    super_opt = SuperSmart(username=request.user)
    if request.method == 'POST':
        super_withdraw_form = super_withdrawalForm(request.POST, instance=super_opt)
        if super_withdraw_form.is_valid:
            req_user_option = SuperSmart.objects.filter(username=request.user)
            req_user_option.update(request=True)

            super_pull_request = users_investment_progress.objects.filter(user=request.user).filter(package='SuperSmart')
            super_pull_request.update(withdraw_request=True)

            get_user = request.user
            mail_sending(get_user)#Alerts Admin for withdrawal request

            return redirect('dashboard')
    else:
        super_withdraw_form = super_withdrawalForm()
    user_progress_update = users_investment_progress.objects.filter(user=request.user).filter(package='SuperSmart')

    current_date = datetime.now()
    today = date.isoformat(current_date)
    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='SuperSmart').filter(Due_date__lte=datetime.isoformat(current_date)).values().exists()
    context = {
        'super_withdraw_form':super_withdraw_form,
        'user_progress_update':user_progress_update,
        'today':today,
        'date_check':date_check
    }
    return render(request, 'gentannieApp/dash/super_withdrawal_page.html',context)

def supreme_withdrawal_page(request):
    supreme_opt = supreme(username=request.user)
    if request.method == 'POST':
        supreme_withdraw_form = supreme_withdrawalForm(request.POST, instance=supreme_opt)
        if supreme_withdraw_form.is_valid:
            req_user_option = supreme.objects.filter(username=request.user)
            req_user_option.update(request=True)

            supreme_pull_request = users_investment_progress.objects.filter(user=request.user).filter(package='supreme')
            supreme_pull_request.update(withdraw_request=True)

            get_user = request.user
            mail_sending(get_user)#Alerts Admin for withdrawal request

            return redirect('dashboard')
    else:
        supreme_withdraw_form = supreme_withdrawalForm()
    user_progress_update = users_investment_progress.objects.filter(user=request.user).filter(package='supreme')
    current_date = datetime.now()
    today = date.isoformat(current_date)
    date_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='supreme').filter(Due_date__lte=datetime.isoformat(current_date)).values().exists()
    context = {
        'supreme_withdraw_form':supreme_withdraw_form,
        'user_progress_update':user_progress_update,
        'today':today,
        'date_check':date_check
    }
    return render(request, 'gentannieApp/dash/supreme_withdrawal_page.html',context)
# **************** / .withdrawal request *****************

def notification(request):
    notice = notify_user.objects.all().filter(username=request.user)
    notice2 = notify_all_user.objects.all()

    context={
        'notice':notice,
        'notice2':notice2
    }
    return render(request,'gentannieApp/dash/dash_notification.html', context)

def account_detail_profile(request):
    user_prof = users_details(username=request.user)
    if request.method == 'POST':
        profile_form = users_detailsForm(request.POST, request.FILES, instance=user_prof)
        if profile_form.is_valid():
            # profile_form.cl
            user_details = profile_form.save(commit=False)
            user_details.save()
 
        return redirect('dashboard')
    else:
        profile_form = users_detailsForm()

    details = users_details.objects.all().filter(username=request.user)
    profile_check = users_details.objects.all().filter(username=request.user).values()
    profile_list = users_details.objects.all().values_list

    print(profile_list)
    rendered_form = ''
    button_diabler = ''
    Display_btn = ''
    if profile_check.exists():
        button_diabler = 'hidden'
        Display_btn = 'Profile updated'
        print('am present sir')
    else:
        rendered_form = users_detailsForm()
        Display_btn = 'submit'
        print('not in list')

    profile_context={
        'rendered_form':rendered_form,
        'details':details,
        'button_diabler':button_diabler,
        'Display_btn':Display_btn
    }
    return render(request,'gentannieApp/dash/dash_profile.html',profile_context)

def mail_check():
    dateDue = users_investment_progress.objects.all()
    # due_date = dateDue.get()
    due_date = date.today
    filtered_date = users_investment_progress.objects.filter(Due_date = str(due_date))

# if filtered_date:
    print (filtered_date.user )
# ******** / .investment plans Views *********

def logoutUser(request):
    logout(request)
    messages.info(request, "You have logged Out!!!")
    return redirect("login")

def deposit_sending(deposit, get_user):
    EMAIL_HOST_USER = 'anthonix1759@gmail.com'
    subject =  'Deposit made, plan has been paid for by %s'%get_user
    message = 'Admin someone just made a deposit and needs comfirmation'
    # recepient = ['informaniac665@gmail.com']
    try:
        send_mail(subject,
            message, 'support@gentannie.com', ['support@gentannie.com'], fail_silently=False)
    except:
        print('MAIL not sent')

def mail_sending(get_user):
    EMAIL_HOST_USER = 'anthonix1759@gmail.com'
    subject =  'Withdrawal is being requested for by %s'%get_user
    message = 'Admin someone just made a request for withdrawal '
    # recepient = ['informaniac665@gmail.com']
    try:
        send_mail(subject,
            # message, 'informaniac665@gmail.com', ['anthonix1759@gmail.com'], fail_silently=False)
            message, 'informaniac665@gmail.com', ['support@gentannie.com'], fail_silently=False)
    except:
        print('MAIL not sent')

def scheduled_withdrawal():
    filtered_data = users_investment_progress.objects.all().filter(deposit_status=comfirmed, hault=False, account_type=locked)
    super_filtered_data = users_investment_progress.objects.all().filter(deposit_status=comfirmed, hault=False, account_type=unlocked)
    supreme_filtered_data = users_investment_progress.objects.all().filter(deposit_status=comfirmed, hault=False, account_type='NONE')
    
    # filtered_data = users_investment_progress.objects.all().filter(deposit_status=comfirmed).filter(hault=False).filter(account_type=locked)
    # super_filtered_data = users_investment_progress.objects.all().filter(deposit_status=comfirmed).filter(hault=False).filter(account_type=unlocked)
    # supreme_filtered_data = users_investment_progress.objects.all().filter(deposit_status=comfirmed).filter(hault=False).filter(account_type='NONE')

    filtered_data.update(Due_date=datetime.now()+ timedelta(days= (30*3)),hault=True )
    super_filtered_data.update(Due_date=datetime.now()+ timedelta(days=30),hault=True)
    supreme_filtered_data.update(Due_date=datetime.now()+ timedelta(days=30),hault=True)

    # current_date = datetime.now()
    current_date = date.today()
    payment_filters = users_investment_progress.objects.all().filter(deposit_status=comfirmed).filter(Due_date__lte=date.isoformat(current_date))

    payment_filters.update(payment_status=payment_declined)

def life_span_cheker():
    smart_pay_out_checker = smart.objects.all().filter(payment_count=9)
    super_pay_out_checker = SuperSmart.objects.all().filter(payment_count=9)
    supreme_pay_out_checker = supreme.objects.all().filter(payment_count=9)
    pay_out_checker = users_investment_progress.objects.all().filter(count=9)

    smart_pay_out_checker.all().delete()
    super_pay_out_checker.all().delete()
    supreme_pay_out_checker.all().delete()
    pay_out_checker.all().delete()

def transact_history(request):
    user_history = users_investment_progress.objects.all().filter(user=request.user)
    # withdrawal_amount_count = user_history.filter()
    # print(withdrawal_amount_count.values())
    context={
        'user_history':user_history
    }
    return render(request, 'gentannieApp/dash/dash_trans_history.html', context)

# ************* payment comfirmations  ********************
def comfirm_smart_payment_page(request):
    if request.method=='POST':
        comfirmed_form = smart_pay_comfirmForm(request.POST)
        if comfirmed_form.is_valid():

            # ********** keeping count of users life span **********
            smart_count_locked = users_investment_progress.objects.all().filter(user=request.user).filter(package='smart').filter(account_type=locked)
            smart_count_life_span_locked = smart.objects.all().filter(username=request.user).filter(account_type=locked)

            smart_count_locked.update(count=F('count')+3)
            smart_count_life_span_locked.update(payment_count=F('payment_count')+3)

            smart_count_unlockd = users_investment_progress.objects.all().filter(user=request.user).filter(package='smart').filter(account_type=unlocked)
            smart_count_life_span_unlocked = smart.objects.all().filter(username=request.user).filter(account_type=unlocked)

            smart_count_unlockd.update(count=F('count')+1)
            smart_count_life_span_unlocked.update(payment_count=F('payment_count')+1)
            # ********** / .keeping count of users life span **********

            #*************** withdrawal History ******************
            withdrawal_history = withdrawal_tabel.objects.all().filter(username=request.user)
            withdrawal_history.update()
            #*************** / .withdrawal History ******************

            smart_comfirm_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='smart').filter(withdraw_request=True )
            smart_comfirm_check.update(hault=False,withdraw_request=False)

        return redirect('dashboard')
    else:
        comfirmed_form = smart_pay_comfirmForm()

    smart_progress_feed = users_investment_progress.objects.all().filter(user=request.user).filter(package='smart')
    context = {
        'comfirmed_form':comfirmed_form,
        "smart_progress_feed":smart_progress_feed
    }
    return render(request,'gentannieApp/dash/smart_pay_comfirm.html', context)

def comfirm_super_payment_page(request):
    if request.method=='POST':
        comfirmed_form = super_pay_comfirmForm(request.POST)
        if comfirmed_form.is_valid():

            # ********** keeping count of users life span **********
            super_count_locked = users_investment_progress.objects.all().filter(user=request.user).filter(package='SuperSmart').filter(account_type=locked)
            super_count_life_span_locked = SuperSmart.objects.all().filter(username=request.user).filter(account_type=locked)

            super_count_locked.update(count=F('count')+3)
            super_count_life_span_locked.update(payment_count=F('payment_count')+3)

            super_count_unlocked = users_investment_progress.objects.all().filter(user=request.user).filter(package='SuperSmart').filter(account_type=unlocked)
            super_count_life_span_unlocked = SuperSmart.objects.all().filter(username=request.user).filter(account_type=unlocked)

            super_count_unlocked.update(count=F('count')+1)
            super_count_life_span_unlocked.update(payment_count=F('payment_count')+1)
            # ********** / .keeping count of users life span **********

            super_comfirm_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='SuperSmart').filter(withdraw_request=True )
            super_comfirm_check.update(hault=False,withdraw_request=False)

        return redirect('dashboard')
    else:
        comfirmed_form = super_pay_comfirmForm()

    super_progress_feed = users_investment_progress.objects.all().filter(user=request.user).filter(package='SuperSmart')
    context = {
        'comfirmed_form':comfirmed_form,
        'super_progress_feed':super_progress_feed
    }
    return render(request,'gentannieApp/dash/super_pay_comfirm.html', context)

def comfirm_supreme_payment_page(request):
    if request.method=='POST':
        comfirmed_form = supreme_pay_comfirmForm(request.POST)
        if comfirmed_form.is_valid():

            # ********* keeping count of users life span *************
            supreme_count = users_investment_progress.objects.all().filter(user=request.user).filter(package='supreme')
            supreme_count.update(count=F('count')+1)

            supreme_count_life_span = supreme.objects.all().filter(username=request.user)
            supreme_count_life_span.update(payment_count=F('payment_count')+1)
            # ********* / .keeping count of users life span *************

            supreme_comfirm_check = users_investment_progress.objects.all().filter(user=request.user).filter(package='supreme').filter(withdraw_request=True )
            supreme_comfirm_check.update(hault=False,withdraw_request=False)

        return redirect('dashboard')
    else:
        comfirmed_form = supreme_pay_comfirmForm()
    
    supreme_progress_feed = users_investment_progress.objects.all().filter(user=request.user).filter(package='supreme')
    context = {
        'comfirmed_form':comfirmed_form,
        "supreme_progress_feed":supreme_progress_feed
    }
    return render(request,'gentannieA.pp/dash/supreme_pay_comfirm.html', context)
# ************ / .payment comfirmations ***************

def referal_scheduler():
    referal_bonus_reset = user_referal.objects.all().filter(payment_status='Payment_made')
    referal_bonus_reset.update(Referal_bonus=F('Referal_bonus')-10000, numbers_refered=F('numbers_refered')-10, payment_status='NONE', request_bonus=False, requested_bonus=0)


def statistics(request):
    investment_prog_details = users_investment_progress.objects.all()

    users_detail = users_details.objects.all().order_by('-username')
     
    smart_plan_stats = smart.objects.all()
    super_plan_stats = SuperSmart.objects.all()
    supreme_plan_stats = supreme.objects.all()

    summed_smart = 0
    summed_super = 0
    summed_supreme = 0

    for smart_x in smart_plan_stats.iterator():
        gotted_val = smart_x.amount_deposited
        summed_smart = int(gotted_val) + summed_smart
        
    unlocked_types = investment_prog_details.filter(account_type='unlocked').count()
    locked_types = investment_prog_details.filter(account_type='locked').count()

    tot_locked = investment_prog_details.filter(account_type='locked').values_list('amount_deposited')
    total_locked_amount = 0

    for locked_sum in tot_locked:
        conv_list = list(locked_sum)
        for gotten_sum in conv_list:
            gotten_sm_int = int(gotten_sum)
            total_locked_amount = gotten_sm_int + total_locked_amount
            
    tot_unlocked = investment_prog_details.filter(account_type='unlocked').values_list('amount_deposited')
    total_unlocked_amount = 0
    for unlocked_sum in tot_unlocked:
        conv_list = list(unlocked_sum)
        for gotten_sum in conv_list:
            gotten_sum_int = int(gotten_sum)
            total_unlocked_amount = gotten_sum_int + total_unlocked_amount

    amount_details = investment_prog_details.values_list('amount_deposited')
    total_amount_deposited = 0
    for total_amount in amount_details:
        amount_listed = list(total_amount)
        for gotten_sum in amount_listed:
            gotten_sum_int = int(gotten_sum)
            total_amount_deposited = gotten_sum_int + total_amount_deposited

    # count of smart_plan packages
    basic_count = smart_plan_stats.filter(plan='basic').values_list('plan').count()
    standard_count = smart_plan_stats.filter(plan='standard').values_list('plan').count()
    premium_count = smart_plan_stats.filter(plan='premium').values_list('plan').count()
    bronze_count = smart_plan_stats.filter(plan='bronze').values_list('plan').count()
    super_bronze_count = smart_plan_stats.filter(plan='super_bronze').values_list('plan').count()
    silver_count = smart_plan_stats.filter(plan='silver').values_list('plan').count()
    super_silver_count = smart_plan_stats.filter(plan='super_silver').values_list('plan').count()
    Gold_count = smart_plan_stats.filter(plan='Gold').values_list('plan').count()

    # count of super_plan packages
    basic_super_count = super_plan_stats.filter(plan='basic').values_list('plan').count()
    standard_super_count = super_plan_stats.filter(plan='standard').values_list('plan').count()
    premium_super_count = super_plan_stats.filter(plan='premium').values_list('plan').count()
    bronze_super_count = super_plan_stats.filter(plan='bronze').values_list('plan').count()
    super_bronze_super_count = super_plan_stats.filter(plan='super_bronze').values_list('plan').count()
    silver_super_count = super_plan_stats.filter(plan='silver').values_list('plan').count()
    super_silver_super_count = super_plan_stats.filter(plan='super_silver').values_list('plan').count()
    Gold_super_count = super_plan_stats.filter(plan='Gold').values_list('plan').count()
    diamond_super_count = super_plan_stats.filter(plan='diamond').values_list('plan').count()
    Ruby_super_count = super_plan_stats.filter(plan='Ruby').values_list('plan').count()
    pearl_super_count = super_plan_stats.filter(plan='pearl').values_list('plan').count()
    emerald_super_count = super_plan_stats.filter(plan='emerald').values_list('plan').count()
    Jasper_super_count = super_plan_stats.filter(plan='Jasper').values_list('plan').count()

    # count of supreme_plan packages
    Whale_count = super_plan_stats.filter(plan='Whale').values_list('plan').count()
    Patriot_count = super_plan_stats.filter(plan='Patriot').values_list('plan').count()

    for super_x in super_plan_stats.iterator():
        gotted_val = super_x.amount_deposited
        summed_super = int(gotted_val) + summed_super

    for supreme_x in supreme_plan_stats.iterator():
        gotted_val = supreme_x.amount_deposited
        summed_supreme = int(gotted_val) + summed_supreme
    pack =None
    for invest_prog_details in  investment_prog_details.iterator():
        pack = invest_prog_details.plan
            
    # ************* Sum of Smart total ROI For Investors *****************
    # ******** total basic smart ROI********
    unlocked_basic_count = users_investment_progress.objects.filter(package='smart').filter(account_type='unlocked').filter(plan='basic').values_list('count')
    basic_ROI = 0
    total_unlocked_basic_ROI = 0
    for unlocked_basic_ROI_count in unlocked_basic_count.iterator():
        for ROI_count in unlocked_basic_ROI_count:
            basic_ROI = ROI_count + basic_ROI
            # basic_ROI = ROI_count + basic_ROI
            total_unlocked_basic_ROI = basic_ROI * 5000

    locked_basic_count = users_investment_progress.objects.filter(package='smart').filter(account_type='locked').filter(plan='basic').values_list('count')
    basic_ROI = 0
    total_locked_basic_ROI = 0
    for basic_ROI_count in locked_basic_count.iterator():
        for ROI_count in basic_ROI_count:
            basic_ROI = ROI_count + basic_ROI
            total_locked_basic_ROI = basic_ROI * 16000

    # ******** total standard smart ROI********
    unlocked_standard_count = users_investment_progress.objects.filter(package='smart').filter(account_type='unlocked').filter(plan='standard').values_list('count')
    standard_ROI = 0
    total_unlocked_standard_ROI = 0
    for standard_ROI_count in unlocked_standard_count.iterator():
        for ROI_count in standard_ROI_count:
            standard_ROI = ROI_count + standard_ROI
            total_unlocked_standard_ROI = standard_ROI * 14000

    locked_standard_count = users_investment_progress.objects.filter(package='smart').filter(account_type='locked').filter(plan='standard').values_list('count')
    standard_ROI = 0
    total_locked_standard_ROI = 0
    for standard_ROI_count in locked_standard_count.iterator():
        for ROI_count in standard_ROI_count:
            standard_ROI = ROI_count + standard_ROI
            total_locked_standard_ROI = standard_ROI * 48000

    # ******** total premium smart ROI********
    smart_premium_count = users_investment_progress.objects.filter(package='smart').filter(account_type='unlocked').filter(plan='premium').values_list('count')
    premium_ROI = 0
    total_unlock_premium_ROI = 0
    for premium_ROI_count in smart_premium_count.iterator():
        for ROI_count in premium_ROI_count:
            premium_ROI = ROI_count + premium_ROI
            total_unlock_premium_ROI = premium_ROI * 21000

    locked_premium_count = users_investment_progress.objects.filter(package='smart').filter(account_type='locked').filter(plan='premium').values_list('count')
    premium_ROI = 0
    total_lock_premium_ROI = 0
    for premium_ROI_count in locked_premium_count.iterator():
        for ROI_count in premium_ROI_count:
            premium_ROI = ROI_count + premium_ROI
            total_lock_premium_ROI = premium_ROI * 72000

    # ******** total bronze smart ROI********
    unlocked_bronze_count = users_investment_progress.objects.filter(package='smart').filter(account_type='unlocked').filter(plan='bronze').values_list('count')
    bronze_ROI = 0
    total_unlock_bronze_ROI = 0
    for bronze_ROI_count in unlocked_bronze_count.iterator():
        for ROI_count in bronze_ROI_count:
            bronze_ROI = ROI_count + bronze_ROI
            total_unlock_bronze_ROI = bronze_ROI * 28000

    locked_bronze_count = users_investment_progress.objects.filter(package='smart').filter(account_type='locked').filter(plan='bronze').values_list('count')
    bronze_ROI = 0
    total_lock_bronze_ROI = 0
    for bronze_ROI_count in locked_bronze_count.iterator():
        for ROI_count in bronze_ROI_count:
            bronze_ROI = ROI_count + bronze_ROI
            total_lock_bronze_ROI = bronze_ROI * 72000

    # ******** total super_bronze smart ROI********
    unlocked_super_bronze_count = users_investment_progress.objects.filter(package='smart').filter(account_type='unlocked').filter(plan='super_bronze').values_list('count')
    super_bronze_ROI = 0
    total_unlock_super_bronze_ROI = 0
    for super_bronze_ROI_count in unlocked_super_bronze_count.iterator():
        for ROI_count in super_bronze_ROI_count:
            super_bronze_ROI = ROI_count + super_bronze_ROI
            total_unlock_super_bronze_ROI = super_bronze_ROI * 35000

    locked_super_bronze_count = users_investment_progress.objects.filter(package='smart').filter(account_type='locked').filter(plan='super_bronze').values_list('count')
    super_bronze_ROI = 0
    total_lock_super_bronze_ROI = 0
    for super_bronze_ROI_count in locked_super_bronze_count.iterator():
        for ROI_count in super_bronze_ROI_count:
            super_bronze_ROI = ROI_count + super_bronze_ROI
            total_lock_super_bronze_ROI = super_bronze_ROI * 120000

    # ******** total silver smart ROI********
    unlocked_silver_count = users_investment_progress.objects.filter(package='smart').filter(account_type='unlocked').filter(plan='silver').values_list('count')
    silver_ROI = 0
    total_unlock_silver_ROI = 0
    for silver_ROI_count in unlocked_silver_count.iterator():
        for ROI_count in silver_ROI_count:
            silver_ROI = ROI_count + silver_ROI
            total_unlock_silver_ROI = silver_ROI * 49000

    locked_silver_count = users_investment_progress.objects.filter(package='smart').filter(account_type='locked').filter(plan='silver').values_list('count')
    silver_ROI = 0
    total_lock_silver_ROI = 0
    for silver_ROI_count in locked_silver_count.iterator():
        for ROI_count in silver_ROI_count:
            silver_ROI = ROI_count + silver_ROI
            total_lock_silver_ROI = silver_ROI * 120000

    # ******** total super_silver smart ROI********
    locked_super_silver_count = users_investment_progress.objects.filter(package='smart').filter(account_type='unlocked').filter(plan='super_silver').values_list('count')
    super_silver_ROI = 0
    total_unlock_super_silver_ROI = 0
    for super_silver_ROI_count in locked_super_silver_count.iterator():
        for ROI_count in super_silver_ROI_count:
            super_silver_ROI = ROI_count + super_silver_ROI
            total_unlock_super_silver_ROI = super_silver_ROI * 120000

    locked_super_silver_count = users_investment_progress.objects.filter(package='smart').filter(account_type='locked').filter(plan='super_silver').values_list('count')
    super_silver_ROI = 0
    total_lock_super_silver_ROI = 0
    for super_silver_ROI_count in locked_super_silver_count.iterator():
        for ROI_count in super_silver_ROI_count:
            super_silver_ROI = ROI_count + super_silver_ROI
            total_lock_super_silver_ROI = super_silver_ROI * 120000

    # ******** total ROI smart Gold ********
    unlocked_Gold_count = users_investment_progress.objects.filter(package='smart').filter(account_type='unlocked').filter(plan='Gold').values_list('count')
    Gold_ROI = 0
    total_unlock_Gold_ROI = 0
    for Gold_ROI_count in unlocked_Gold_count.iterator():
        for ROI_count in Gold_ROI_count:
            Gold_ROI = ROI_count + Gold_ROI
            total_unlock_Gold_ROI = Gold_ROI * 120000

    locked_Gold_count = users_investment_progress.objects.filter(package='smart').filter(account_type='locked').filter(plan='Gold').values_list('count')
    Gold_ROI = 0
    total_lock_Gold_ROI = 0
    for Gold_ROI_count in locked_Gold_count.iterator():
        for ROI_count in Gold_ROI_count:
            Gold_ROI = ROI_count + Gold_ROI
            total_lock_Gold_ROI = Gold_ROI * 120000

    # ************* Sum of SuperSmart total ROI For Investors *****************
    # ******** total basic SuperSmart ROI********
    unlocked_basic_count = users_investment_progress.objects.filter(package='SuperSmart').filter(account_type='unlocked').filter(plan='basic').values_list('count')
    basic_ROI = 0
    total_unlocked_basic_ROI = 0
    for unlocked_basic_ROI_count in unlocked_basic_count.iterator():
        for ROI_count in unlocked_basic_ROI_count:
            basic_ROI = ROI_count + basic_ROI
            # basic_ROI = ROI_count + basic_ROI
            total_unlocked_basic_ROI = basic_ROI * 5000

    locked_basic_count = users_investment_progress.objects.filter(package='SuperSmart').filter(account_type='locked').filter(plan='basic').values_list('count')
    basic_ROI = 0
    total_locked_basic_ROI = 0
    for basic_ROI_count in locked_basic_count.iterator():
        for ROI_count in basic_ROI_count:
            basic_ROI = ROI_count + basic_ROI
            total_locked_basic_ROI = basic_ROI * 16000

    # ******** total standard SuperSmart ROI********
    unlocked_standard_count = users_investment_progress.objects.filter(package='SuperSmart').filter(account_type='unlocked').filter(plan='standard').values_list('count')
    standard_ROI = 0
    total_unlocked_standard_ROI = 0
    for standard_ROI_count in unlocked_standard_count.iterator():
        for ROI_count in standard_ROI_count:
            standard_ROI = ROI_count + standard_ROI
            total_unlocked_standard_ROI = standard_ROI * 14000

    locked_standard_count = users_investment_progress.objects.filter(package='SuperSmart').filter(account_type='locked').filter(plan='standard').values_list('count')
    standard_ROI = 0
    total_locked_standard_ROI = 0
    for standard_ROI_count in locked_standard_count.iterator():
        for ROI_count in standard_ROI_count:
            standard_ROI = ROI_count + standard_ROI
            total_locked_standard_ROI = standard_ROI * 48000

    # ******** total premium SuperSmart ROI********
    SuperSmart_premium_count = users_investment_progress.objects.filter(package='SuperSmart').filter(account_type='unlocked').filter(plan='premium').values_list('count')
    premium_ROI = 0
    total_unlock_premium_ROI = 0
    for premium_ROI_count in SuperSmart_premium_count.iterator():
        for ROI_count in premium_ROI_count:
            premium_ROI = ROI_count + premium_ROI
            total_unlock_premium_ROI = premium_ROI * 21000

    locked_premium_count = users_investment_progress.objects.filter(package='SuperSmart').filter(account_type='locked').filter(plan='premium').values_list('count')
    premium_ROI = 0
    total_lock_premium_ROI = 0
    for premium_ROI_count in locked_premium_count.iterator():
        for ROI_count in premium_ROI_count:
            premium_ROI = ROI_count + premium_ROI
            total_lock_premium_ROI = premium_ROI * 72000

    # ******** total bronze SuperSmart ROI********
    unlocked_bronze_count = users_investment_progress.objects.filter(package='SuperSmart').filter(account_type='unlocked').filter(plan='bronze').values_list('count')
    bronze_ROI = 0
    total_unlock_bronze_ROI = 0
    for bronze_ROI_count in unlocked_bronze_count.iterator():
        for ROI_count in bronze_ROI_count:
            bronze_ROI = ROI_count + bronze_ROI
            total_unlock_bronze_ROI = bronze_ROI * 28000

    locked_bronze_count = users_investment_progress.objects.filter(package='SuperSmart').filter(account_type='locked').filter(plan='bronze').values_list('count')
    bronze_ROI = 0
    total_lock_bronze_ROI = 0
    for bronze_ROI_count in locked_bronze_count.iterator():
        for ROI_count in bronze_ROI_count:
            bronze_ROI = ROI_count + bronze_ROI
            total_lock_bronze_ROI = bronze_ROI * 72000

    # ******** total super_bronze SuperSmart ROI********
    unlocked_super_bronze_count = users_investment_progress.objects.filter(package='SuperSmart').filter(account_type='unlocked').filter(plan='super_bronze').values_list('count')
    super_bronze_ROI = 0
    total_unlock_super_bronze_ROI = 0
    for super_bronze_ROI_count in unlocked_super_bronze_count.iterator():
        for ROI_count in super_bronze_ROI_count:
            super_bronze_ROI = ROI_count + super_bronze_ROI
            total_unlock_super_bronze_ROI = super_bronze_ROI * 35000

    locked_super_bronze_count = users_investment_progress.objects.filter(package='SuperSmart').filter(account_type='locked').filter(plan='super_bronze').values_list('count')
    super_bronze_ROI = 0
    total_lock_super_bronze_ROI = 0
    for super_bronze_ROI_count in locked_super_bronze_count.iterator():
        for ROI_count in super_bronze_ROI_count:
            super_bronze_ROI = ROI_count + super_bronze_ROI
            total_lock_super_bronze_ROI = super_bronze_ROI * 120000

    # ******** total silver SuperSmart ROI********
    unlocked_silver_count = users_investment_progress.objects.filter(package='SuperSmart').filter(account_type='unlocked').filter(plan='silver').values_list('count')
    silver_ROI = 0
    total_unlock_silver_ROI = 0
    for silver_ROI_count in unlocked_silver_count.iterator():
        for ROI_count in silver_ROI_count:
            silver_ROI = ROI_count + silver_ROI
            total_unlock_silver_ROI = silver_ROI * 49000

    locked_silver_count = users_investment_progress.objects.filter(package='SuperSmart').filter(account_type='locked').filter(plan='silver').values_list('count')
    silver_ROI = 0
    total_lock_silver_ROI = 0
    for silver_ROI_count in locked_silver_count.iterator():
        for ROI_count in silver_ROI_count:
            silver_ROI = ROI_count + silver_ROI
            total_lock_silver_ROI = silver_ROI * 120000

    # ******** total super_silver SuperSmart ROI********
    locked_super_silver_count = users_investment_progress.objects.filter(package='SuperSmart').filter(account_type='unlocked').filter(plan='super_silver').values_list('count')
    super_silver_ROI = 0
    total_unlock_super_silver_ROI = 0
    for super_silver_ROI_count in locked_super_silver_count.iterator():
        for ROI_count in super_silver_ROI_count:
            super_silver_ROI = ROI_count + super_silver_ROI
            total_unlock_super_silver_ROI = super_silver_ROI * 120000

    locked_super_silver_count = users_investment_progress.objects.filter(package='SuperSmart').filter(account_type='locked').filter(plan='super_silver').values_list('count')
    super_silver_ROI = 0
    total_lock_super_silver_ROI = 0
    for super_silver_ROI_count in locked_super_silver_count.iterator():
        for ROI_count in super_silver_ROI_count:
            super_silver_ROI = ROI_count + super_silver_ROI
            total_lock_super_silver_ROI = super_silver_ROI * 120000

    # ******** total Gold SuperSmart ROI********
    unlocked_Gold_count = users_investment_progress.objects.filter(package='SuperSmart').filter(account_type='unlocked').filter(plan='Gold').values_list('count')
    Gold_ROI = 0
    total_unlock_Gold_ROI = 0
    for Gold_ROI_count in unlocked_Gold_count.iterator():
        for ROI_count in Gold_ROI_count:
            Gold_ROI = ROI_count + Gold_ROI
            total_unlock_Gold_ROI = Gold_ROI * 120000

    locked_Gold_count = users_investment_progress.objects.filter(package='SuperSmart').filter(account_type='locked').filter(plan='Gold').values_list('count')
    Gold_ROI = 0
    total_lock_Gold_ROI = 0
    for Gold_ROI_count in locked_Gold_count.iterator():
        for ROI_count in Gold_ROI_count:
            Gold_ROI = ROI_count + Gold_ROI
            total_lock_Gold_ROI = Gold_ROI * 120000


    # count of super_plan packages
    basic_super_count = super_plan_stats.filter(plan='basic').values_list('plan').count()
    standard_super_count = super_plan_stats.filter(plan='standard').values_list('plan').count()
    premium_super_count = super_plan_stats.filter(plan='premium').values_list('plan').count()
    bronze_super_count = super_plan_stats.filter(plan='bronze').values_list('plan').count()
    super_bronze_super_count = super_plan_stats.filter(plan='super_bronze').values_list('plan').count()
    silver_super_count = super_plan_stats.filter(plan='silver').values_list('plan').count()
    super_silver_super_count = super_plan_stats.filter(plan='super_silver').values_list('plan').count()
    Gold_super_count = super_plan_stats.filter(plan='Gold').values_list('plan').count()
    diamond_super_count = super_plan_stats.filter(plan='diamond').values_list('plan').count()
    Ruby_super_count = super_plan_stats.filter(plan='Ruby').values_list('plan').count()
    pearl_super_count = super_plan_stats.filter(plan='pearl').values_list('plan').count()
    emerald_super_count = super_plan_stats.filter(plan='emerald').values_list('plan').count()
    Jasper_super_count = super_plan_stats.filter(plan='Jasper').values_list('plan').count()

    # count of supreme_plan packages
    Whale_count = super_plan_stats.filter(plan='Whale').values_list('plan').count()
    Patriot_count = super_plan_stats.filter(plan='Patriot').values_list('plan').count()

    # **************
    total_smart_depo = smart_plan_stats.count()
    total_super_depo = super_plan_stats.count()
    total_supreme_depo = supreme_plan_stats.count()

    context= {
        'total_unlocked_basic_ROI':total_unlocked_basic_ROI,
        'total_locked_basic_ROI':total_locked_basic_ROI,

        'total_unlocked_standard_ROI':total_unlocked_standard_ROI,
        'total_locked_standard_ROI':total_locked_standard_ROI,

        'total_unlock_premium_ROI':total_unlock_premium_ROI,
        'total_lock_premium_ROI':total_lock_premium_ROI,

        'total_unlock_bronze_ROI':total_unlock_bronze_ROI,
        'total_lock_bronze_ROI':total_lock_bronze_ROI,

        'total_unlock_super_bronze_ROI':total_unlock_super_bronze_ROI,
        'total_lock_super_bronze_ROI':total_lock_super_bronze_ROI,

        'total_unlock_silver_ROI':total_unlock_silver_ROI,
        'total_lock_silver_ROI':total_lock_silver_ROI,

        'total_unlock_super_silver_ROI':total_unlock_super_silver_ROI,
        'total_lock_super_silver_ROI':total_lock_super_silver_ROI,

        'total_unlock_Gold_ROI':total_unlock_Gold_ROI,
        'total_lock_Gold_ROI':total_lock_Gold_ROI,

        # 'perted':perted,

        # 'basic_unlocked_count':basic_unlocked_count,
        # ****************** total ROI for smart plan *******************
        # "gotten_basic_unlocked":gotten_basic_unlocked,
        # "gotten_basic_locked":gotten_basic_locked,

        # "gotten_standard_locked":gotten_standard_locked,
        # "gotten_standard_unlocked":gotten_standard_unlocked,

        # "gotten_premium_locked":gotten_premium_locked,
        # "gotten_premium_unlocked":gotten_premium_unlocked,

        # "gotten_bronze_locked":gotten_bronze_locked,
        # "gotten_bronze_unlocked":gotten_bronze_unlocked,

        # "gotten_super_bronze_locked":gotten_super_bronze_locked,
        # "gotten_super_bronze_unlocked":gotten_super_bronze_unlocked,
        
        # "gotten_silver_locked":gotten_silver_locked,
        # "gotten_silver_locked":gotten_silver_locked,

        # "gotten_super_silver_unlocked":gotten_super_silver_unlocked,
        # "gotten_super_silver_unlocked":gotten_super_silver_unlocked,

        # "gotten_Gold_unlocked":gotten_Gold_unlocked,
        # "gotten_Gold_unlocked":gotten_Gold_unlocked,

        # ****************** total ROI for SuperSmart plan *******************
        # "gotten_basic_unlocked_ss":gotten_basic_unlocked_ss,
        # "gotten_basic_locked_ss":gotten_basic_locked_ss,

        # "gotten_standard_locked_ss":gotten_standard_locked_ss,
        # "gotten_standard_unlocked_ss":gotten_standard_unlocked_ss,

        # "gotten_premium_locked_ss":gotten_premium_locked_ss,
        # "gotten_premium_unlocked_ss":gotten_premium_unlocked_ss,

        # "gotten_bronze_locked_ss":gotten_bronze_locked_ss,
        # "gotten_bronze_unlocked_ss":gotten_bronze_unlocked_ss,

        # "gotten_super_bronze_locked_ss":gotten_super_bronze_locked_ss,
        # "gotten_super_bronze_unlocked_ss":gotten_super_bronze_unlocked_ss,
        
        # "gotten_silver_locked_ss":gotten_silver_locked_ss,
        # "gotten_silver_locked_ss":gotten_silver_locked_ss,

        # "gotten_super_silver_unlocked_ss":gotten_super_silver_unlocked_ss,
        # "gotten_super_silver_unlocked_ss":gotten_super_silver_unlocked_ss,

        # "gotten_Gold_unlocked_ss":gotten_Gold_unlocked_ss,
        # "gotten_Gold_unlocked_ss":gotten_Gold_unlocked_ss,


        "pack":pack,

        "total_amount_deposited":total_amount_deposited,

        "total_locked_amount":total_locked_amount,
        "total_unlocked_amount":total_unlocked_amount,

        "unlocked_types":unlocked_types,
        "locked_types":locked_types,

        "investment_prog_details":investment_prog_details,

        "users_detail":users_detail,

        "smart_plan_stats":smart_plan_stats,
        "super_plan_stats":super_plan_stats,
        "supreme_plan_stats":supreme_plan_stats,

        "total_smart_depo":total_smart_depo,
        "total_super_depo":total_super_depo,
        "total_supreme_depo":total_supreme_depo,

        "summed_smart":summed_smart,
        "summed_super":summed_super,
        "summed_supreme":summed_supreme,
        
        "basic_count":basic_count,
        "standard_count":standard_count,
        "premium_count":premium_count,
        "bronze_count":bronze_count,
        "super_bronze_count":super_bronze_count,
        "silver_count":silver_count,
        "super_silver_count":super_silver_count,
        "Gold_count":Gold_count,

        "basic_super_count":basic_super_count,
        "standard_super_count":standard_super_count,
        "premium_super_count":premium_super_count,
        "bronze_super_count":bronze_super_count,
        "super_bronze_super_count":super_bronze_super_count,
        "silver_super_count":silver_super_count,
        "super_silver_super_count":super_silver_super_count,
        "Gold_super_count":Gold_super_count,
        "diamond_super_count":diamond_super_count,
        "Ruby_super_count":Ruby_super_count,
        "pearl_super_count":pearl_super_count,
        "emerald_super_count":emerald_super_count,
        "Jasper_super_count":Jasper_super_count,

        "Whale_count":Whale_count,
        "Patriot_count":Patriot_count,

    }
    return render(request, 'gentannie_stats/gentannie_stats.html', context)

def user_stats(request):
    users_stats = users_details.objects.all().order_by('-username')

    context = {
        "users_stats":users_stats,
    }
    return render(request, 'gentannie_stats/user_stats.html',context)

def marketing_stats(request):

    # marketer's summary
    mark_001_details = Gem001_client.objects.all()
    mark_001_summed_total = 0
    for market_sum in mark_001_details.iterator():
        gotted_val = market_sum.amount
        mark_001_summed_total = int(gotted_val) + mark_001_summed_total

    mark001_percent_earned = mark_001_summed_total * 0.05
    # client_count = mark_001_details.filter('client').count()

    mark_002_details = Gem002_client.objects.all()
    mark_002_summed_total = 0
    for market_sum in mark_002_details.iterator():
        gotted_val = market_sum.amount
        mark_002_summed_total = int(gotted_val) + mark_002_summed_total

    mark002_percent_earned = mark_002_summed_total * 0.05
    # client_count = mark_00_details.count()

    mark_003_summed_total = 0
    mark_003_details = Gem003_client.objects.all()
    for market_sum in mark_003_details.iterator():
        gotted_val = market_sum.amount
        mark_003_summed_total = int(gotted_val) + mark_003_summed_total

    mark003_percent_earned = mark_003_summed_total * 0.05
    # client_count = mark_00_details.count()

    mark_004_details = Gem004_client.objects.all()
    mark_004_summed_total = 0
    for market_sum in mark_004_details.iterator():
        gotted_val = market_sum.amount
        mark_004_summed_total = int(gotted_val) + mark_004_summed_total

    mark004_percent_earned = mark_004_summed_total * 0.05
    # client_count = mark_00_details.count()

    mark_005_summed_total = 0
    mark_005_details = Gem005_client.objects.all()
    for market_sum in mark_005_details.iterator():
        gotted_val = market_sum.amount
        mark_005_summed_total = int(gotted_val) + mark_005_summed_total

    mark005_percent_earned = mark_005_summed_total * 0.05
    # client_count = mark_00_details.count()

    mark_006_summed_total = 0
    mark_006_details = Gem006_client.objects.all()
    for market_sum in mark_006_details.iterator():
        gotted_val = market_sum.amount
        mark_006_summed_total = int(gotted_val) + mark_006_summed_total

    mark006_percent_earned = mark_006_summed_total * 0.05
    # client_count = mark_00_details.count()

    context = {
        "mark_001_summed_total":mark_001_summed_total,
        "mark001_percent_earned":mark001_percent_earned,
        
        "mark_002_summed_total":mark_002_summed_total,
        "mark002percent_earned":mark002_percent_earned,

        "mark_003_summed_total":mark_003_summed_total,
        "mark003_percent_earned":mark003_percent_earned,

        "mark_004_summed_total":mark_004_summed_total,
        "mark004_percent_earned":mark004_percent_earned,

        "mark_005_summed_total":mark_005_summed_total,
        "mark005_percent_earned":mark005_percent_earned,

        "mark_006_summed_total":mark_006_summed_total,
        "mark006_percent_earned":mark006_percent_earned,

    }
    return render(request, 'gentannie_stats/marketing_stats.html',context)
