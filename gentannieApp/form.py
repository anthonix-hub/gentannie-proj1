from django import forms
from django.db.models import fields
from django.forms import ModelForm, widgets
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import admin
from phonenumber_field.formfields import PhoneNumberField

from django.core.exceptions import ValidationError

from .models import *

def file_size(value): # add this to some file where you can import it from
    # limit = 2 * 1024 
    limit = 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 1 MiB.')

class signupForm (UserCreationForm):
    username = forms.CharField(max_length=20, required=True)
    first_name = forms.CharField(max_length=20, required=True)
    last_name = forms.CharField(max_length=20, required=True)
    # phone_number = IntegerField(required=False)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            # 'phone_number',
            'password1',
            'password2',
            )
        # widgets = {
        #     'username' : TextInput(attrs={'class':'input'}),
        #     'first_name' : TextInput(attrs={'class':'input'}),
        #     'Email' : EmailInput(attrs={'class':'input'}),
        #     'last_name' : TextInput(attrs={'class':'input'}),
        # }
        
    def save(self, commit = True):
        user = super(signupForm,self).save()
        self.middle_name = self.cleaned_data['middle_name']
        # user.phone_number = self.cleaned_data['phone_number']
        if commit:
            user.save()
            return user


class smart_form(ModelForm):
    payment_proof = forms.FileField(validators=[file_size])
    class Meta:
        model = smart
        fields = ('plan_name', 'account_type', 'payment_proof')

class super_form(ModelForm):
    payment_proof = forms.FileField(validators=[file_size])
    class Meta:
        model = SuperSmart
        fields = ('plan_name', 'account_type', 'payment_proof')

class supreme_form(ModelForm):
    payment_proof = forms.FileField(validators=[file_size])
    class Meta:
        model = supreme
        fields = ('plan_name', 'payment_proof')

class users_detailsForm(ModelForm):
# class users_detailsForm(forms.Form):
    # account_number = forms.CharField(max_length=50)
    # account_name = forms.CharField(max_length=50)
    # account_number = forms.CharField(max_length=10)
    # bank_name = forms.CharField(max_length=20)
    # phone_number = forms.CharField()
    # profile_pic = forms.FileField(required=True)

    class Meta:
        model = users_details
        fields = ('account_number', 'account_name', 'bank_name', 'phone_number','profile_pic', )

class withdraw_requestForm(ModelForm):
    class Meta:
        model = withdrawal_table
        fields = ('amount',)


class smart_withdrawalForm(ModelForm):
    class Meta:
        model = smart
        fields = ('request',)

class super_withdrawalForm(ModelForm):
    class Meta:
        model = smart
        fields = ('request',)

class supreme_withdrawalForm(ModelForm):
    class Meta:
        model = smart
        fields = ('request',)

class smart_pay_comfirmForm(ModelForm):
    class Meta:
        model = smart_payment_comfirm
        fields = ('request',)

class super_pay_comfirmForm(ModelForm):
    class Meta:
        model = smart_payment_comfirm
        fields = ('request',)

class supreme_pay_comfirmForm(ModelForm):
    class Meta:
        model = smart_payment_comfirm
        fields = ('request',)
        
