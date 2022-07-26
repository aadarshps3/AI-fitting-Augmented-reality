from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import datetime
import re

from .models import *


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'

def phone_number_validator(value):
    if not re.compile(r'^[7-9]\d{9}$').match(value):
        raise ValidationError('This is Not a Valid Phone Number')

GENDER_CHOICES=(
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Others')
    )

class CustomerForm(UserCreationForm):
    FullName = forms.CharField()
    username = forms.CharField()
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    password1 = forms.CharField(widget=forms.PasswordInput, label='password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='confirm password')
    Contact_no = forms.CharField(validators=[phone_number_validator])
    Email = forms.CharField(validators=[
        RegexValidator(regex='^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$', message='Please Enter a Valid Email')])
    class Meta:
        model = Customer
        fields = UserCreationForm.Meta.fields + ('FullName', 'gender', 'Email', 'Contact_no',)




class ProductForm(forms.ModelForm):
    class Meta:
        model = product
        fields = '__all__'


class CheckoutForm(forms.ModelForm):
    phone_no = forms.CharField(validators=[phone_number_validator])
    email = forms.CharField(validators=[
        RegexValidator(regex='^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$', message='Please Enter a Valid Email')],
    )
    pincode = forms.CharField(validators=[
        RegexValidator(regex='^[1-9][0-9]{5}$', message='Please Enter a Valid Pincode')])

    class Meta:
        model = ShippingAddress
        fields = ('customer','email', 'phone_no', 'address', 'city', 'state', 'pincode',)
        widget = {
            'customer':forms.TextInput(attrs={'class': 'input'}),
            'email': forms.TextInput(attrs={'class': 'input'}),
            'phone_no': forms.TextInput(attrs={'class': 'input'}),
            'address': forms.TextInput(attrs={'class': 'input'}),
            'city': forms.TextInput(attrs={'class': 'input'}),
            'state': forms.TextInput(attrs={'class': 'input'}),
            'pincode': forms.TextInput(attrs={'class': 'input'}),
        }


MONTH_CHOICES = (
    ('January', 'January'),
    ('February ', 'February '),
    ('March ', 'March '),
    ('April ', 'April '),
    ('May ', 'May '),
    ('June ', 'June '),
    ('July ', 'July '),
    ('August ', 'August '),
    ('September ', 'September '),
    ('October ', 'October '),
    ('November ', 'November '),
    ('December ', 'December '),
)


def current_year():
    return datetime.date.today().year


def year_choices():
    return [(r, r) for r in range(2021, datetime.date.today().year + 10)]


month = ['January', 'February ', 'March ', 'May ', 'June ', 'July ', 'August ', 'September ', 'October ', 'November ',
         'December ']


class PaymentForm(forms.ModelForm):
    card_no = forms.CharField(validators=[RegexValidator(regex='^.{16}$', message='Please Enter a Valid Card No')])
    card_cvv = forms.CharField(validators=[RegexValidator(regex='^.{3}$', message='Please Enter a Valid CVV')])
    expiry_month = forms.ChoiceField(choices=MONTH_CHOICES, widget=forms.Select(attrs={'class': 'form-control', }))
    expiry_year = forms.TypedChoiceField(coerce=int, choices=year_choices, initial=current_year,
                                         widget=forms.Select(attrs={'class': 'form-control', }))

    class Meta:
        model = Payment
        fields = ('card_no', 'card_cvv', 'expiry_month', 'expiry_year')

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rating', 'review')

class ComplaintForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput)

    class Meta:
        model = Complaint
        fields = ('complaint','date')
