from django.contrib import admin
from .models import *
admin.site.site_header = " gentannie Portal "
admin.site.index_title = " Welcome to gentannie Admin control_Panel "


class withdrawalAdmin(admin.ModelAdmin):
    list_display = ('username', 'amount', 'package', 'date_filled',)

class notify_userAdmin(admin.ModelAdmin):
    list_display = ('username', 'message', 'message_time')

class notify_all_userAdmin(admin.ModelAdmin):
    list_display = ('message', )

class users_detailsAdmin(admin.ModelAdmin):
    list_display = ('username', 'middle_name','Email_address', 'account_number', 'account_name','phone_number', 'bank_name' ,'date_created','profile_pic',)

class SuperSmartAdmin(admin.ModelAdmin):
    list_display = ('username', 'account_type', 'request', 'amount_deposited', 'ROI', 'payment_count', 'created_date' ,'payment_proof')

class smartAdmin(admin.ModelAdmin):
    list_display = ('username', 'account_type','request', 'amount_deposited', 'ROI', 'payment_count', 'created_date' ,'payment_proof')

class supremeAdmin(admin.ModelAdmin):
    list_display = ('username', 'request', 'amount_deposited', 'ROI','payment_count', 'created_date' ,'payment_proof')

class account_detailsAdmin(admin.ModelAdmin):
    list_display = ('username', 'account_name', 'account_number', 'phone_number', 'date')

class users_investment_progressAdmin(admin.ModelAdmin):
    list_display = ('user', 'package', 'plan', 'withdraw_request' , 'amount_deposited', 'ROI', 'deposit_status', 'account_type', 'life_span', 'count' , 'date_created', 'Due_date','hault', 'payment_status', 'proof', )
    # search_fields = ['user__user',]

admin.site.register(notify_user, notify_userAdmin)
admin.site.register(notify_all_user, notify_all_userAdmin)
admin.site.register(users_details, users_detailsAdmin)
admin.site.register(smart, smartAdmin)
admin.site.register(SuperSmart, SuperSmartAdmin)
admin.site.register(supreme, supremeAdmin)
admin.site.register(users_investment_progress, users_investment_progressAdmin)
# admin.site.register(account_details)
