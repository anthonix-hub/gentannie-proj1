from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.fields.related import OneToOneField
from django.http import request
from tinymce.models import HTMLField
from django.db.models.signals import post_save
from django.dispatch import receiver
from tinymce.models import HTMLField
# from .utils import generate_ref_code

User = get_user_model()

pending = 'pending'
comfirmed = "comfirmed"
rejected = "rejected"
status = [(pending,'pending'), (comfirmed,'comfirmed'), (rejected,'rejected')]

payment_pending = 'payment_pending'
payment_done = "payment_done"
payment_declined = "payment_declined"
pay_state = [(payment_pending,'payment_pending'), (payment_done,'payment_done'), (payment_declined,'payment_declined')]

smart = 'smart'
SuperSmart = 'SuperSmart'
supreme = 'supreme'
package = [(smart, 'smart'), (SuperSmart, 'SuperSmart'), (supreme, 'supreme')]

basic = 'basic'
standard = 'standard'
premium = 'premium'
bronze = 'bronze'
super_bronze = 'super_bronze'
silver = 'silver'
super_silver = 'super_silver'
Gold = 'Gold'
smart_plan = [
    (basic, 'basic'), (standard, 'standard'),(premium, 'premium'), (bronze, 'bronze'),(super_bronze, 'super_bronze'), (silver, 'silver'),(super_silver, 'super_silver'), (Gold, 'Gold')
]

basic = 'basic'
standard = 'standard'
premium = 'premium'
bronze = 'bronze'
super_bronze = 'super_bronze'
silver = 'silver'
super_silver = 'super_silver'
Gold = 'Gold'
diamond = 'diamond'
Ruby = 'Ruby'
peal =  'peal'
emerald = 'emerald'
Jasper = 'Jasper'
SuperSmart_plan = [
    (basic, 'basic'),(standard,'standard'),(premium,'premium'),(bronze,'bronze'),
    (super_bronze,'super_bronze'),(silver,'silver'),(super_silver,'super_silver'),(Gold,'Gold'),
    (diamond, 'diamond'), (Ruby, 'Ruby'),(peal, 'peal'), (emerald, 'emerald'), (Jasper, 'Jasper')
]

Whale = 'Whale'
Patriot = 'Patriot'
supreme_plan = [(Whale, 'Whale'), (Patriot, 'Patriot')]

locked = 'locked'
unlocked = 'unlocked'
type = [(locked, 'locked'), (unlocked, 'unlocked')]


class users_details(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    middle_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    Email_address = models.EmailField(max_length=50)
    profile_pic = models.FileField(upload_to='Images', )
    account_number = models.CharField(max_length=20, )
    account_name = models.CharField(max_length=50, )
    bank_name = models.CharField(max_length=50, )
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.username) + str(self.account_name) + str(self.account_number) + str(self.phone_number)    

# @receiver(post_save, sender=User)
# def update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         users_details.objects.create(username=instance)
        # users_investment_progress.objects.create(user=instance)
    # instance.users_details.save()

class users_investment_progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.CharField(max_length=20, default='NONE')  
    plan = models.CharField(max_length=20, default='none')    
    account_type = models.CharField(max_length=20, default='NONE')    
    amount_deposited = models.CharField(max_length=20, default=0.00)
    ROI = models.CharField(max_length=20, default=0.00)
    deposit_status = models.CharField(max_length=15, choices=status, default=pending)
    date_created = models.DateTimeField(auto_now_add=True)
    Due_date = models.DateTimeField(auto_now_add=False, null=True,blank=True)
    proof = models.FileField(upload_to='Images')
    Roll_out_time = models.DateField(auto_now=True)
    payment_status = models.CharField(max_length=20, choices=pay_state, default=None, null=True, blank=True)
    # payment_count = models.IntegerField(default=0)
    life_span = models.CharField(max_length=50)
    hault = models.BooleanField(default=False)
    withdraw_request = models.BooleanField(default=False)
    count = models.IntegerField(null=True, blank=True, default=0)
    class Meta:
        ordering = ['-date_created']
    def __str__(self):
        return str(self.user) + str(self.ROI) + str(self.package) + str(self.date_created) +str(self.Roll_out_time) 

#  ******** investment plans models ***********
class smart(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.CharField(max_length=30, default='smart', null=True, blank=True)
    plan_name = models.CharField(max_length=30, choices=smart_plan, null=True, blank=True)
    amount_deposited = models.CharField(max_length=20, default=0.00)
    ROI = models.CharField(max_length=20, default=0.00)
    deposit_status = models.CharField(max_length=15, choices=status, default=pending)
    account_type = models.CharField(max_length=30, choices=type)
    request = models.BooleanField(default=False)
    payment_status = models.CharField(max_length=20, choices=pay_state, default=None, null=True, blank=True)
    due_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    payment_proof = models.FileField(upload_to='images')
    created_date = models.DateTimeField(auto_now_add=True)
    payment_count = models.IntegerField(default=0)


    # def __str__(self):
    #     return str(self.username) + str(self.plan_name) + str(self.plan) + str(self.account_type) + str(self.created_date)    

class SuperSmart(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.CharField(max_length=30, default='SuperSmart', null=True, blank=True)
    plan_name = models.CharField(max_length=30, choices=SuperSmart_plan)
    amount_deposited = models.CharField(max_length=20, default=0.00)
    ROI = models.CharField(max_length=20, default=0.00)
    deposit_status = models.CharField(max_length=15, choices=status, default=pending)
    payment_status = models.CharField(max_length=20, choices=pay_state, default=None, null=True, blank=True)
    account_type = models.CharField(max_length=30, choices=type)
    request = models.BooleanField(default=False)
    payment_proof = models.FileField(upload_to='images')
    due_date = models.DateTimeField(auto_now_add=False, null=True,blank=True )
    created_date = models.DateTimeField(auto_now_add=True)
    payment_count = models.IntegerField(default=0)

    def __str__(self):
        return str(self.username) + str(self.plan_name) + str(self.account_type)

class supreme(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.CharField(max_length=30, default='supreme', null=True, blank=True)
    amount_deposited = models.CharField(max_length=20, default=0.00)
    ROI = models.CharField(max_length=20, default=0.00)
    deposit_status = models.CharField(max_length=15, choices=status, default=pending)
    payment_status = models.CharField(max_length=20, choices=pay_state, default=None, null=True, blank=True)
    plan_name = models.CharField(max_length=30, choices=supreme_plan)
    payment_proof = models.FileField(upload_to='images')
    request = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    request = models.BooleanField(default=False)
    payment_count = models.IntegerField(default=0)


    def __str__(self):
            return str(self.username) + str(self.plan_name) + str(self.payment_count)

class withdrawal_table(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # user = models.ForeignKey(User, on_delete=None)
    amount = models.CharField(max_length=20)
    requested_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=status)
    comfirmed_payment = models.BooleanField()

class smart_payment_comfirm(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    request = models.BooleanField()

class super_payment_comfirm(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    request = models.BooleanField()

class supreme_payment_comfirm(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    request = models.BooleanField()

class notify_user(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    message = HTMLField(max_length=49000)
    message_time = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.username) + str(self.message_time)

class notify_all_user(models.Model):
    message = HTMLField(max_length=999)
    sent_date = models.DateTimeField(auto_now_add=True)

    # def __str__(self) -> str:
    #     return self.sent_time

class withdrawal_tabel(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    amount  = models.IntegerField()
    date_filled = models.DateTimeField(auto_now_add=True)
    package = models.CharField(max_length=30)

    