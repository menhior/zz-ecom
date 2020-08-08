from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *

class ContactForm(forms.Form):
	Your_email = forms.EmailField(required=True)
	subject = forms.CharField(required=True)
	message = forms.CharField(widget=forms.Textarea, required=True)

class CustomerContactForm(forms.Form):
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ["first_name", "last_name",'username', 'email', 'password1', 'password2']


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Type your comment',
        'id': 'usercomment',
        'rows': '4'
    }))
    class Meta:
        model = Comment
        fields = ('content', )

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['status']

class FullOrderForm(ModelForm):
    class Meta:
        model=Order
        fields = '__all__'
        """exclude = ['user']"""

class ShippingAddressForm(ModelForm):
    class Meta:
        model=ShippingAddress
        fields = '__all__'

class CustomerForm(ModelForm):
    class Meta:
        model=Customer
        fields = '__all__'
        exclude = ['user', 'device', 'profile_pic']

class UpdateShippingForm(ModelForm):
    class Meta:
        model=ShippingAddress
        fields = '__all__'
        exclude = ['customer', 'order']


class CustomerForm(ModelForm):
    class Meta:
        model=Customer
        fields = '__all__'
        exclude = ['user', 'device', 'profile_pic']


class AccountInformationForm(ModelForm):
    class Meta:
        model=Customer
        fields = '__all__'
        exclude = ['user', 'device',]
"""class ReviewForm(ModelForm):
	class Meta:
		model = Review
		fields = '__all__'
		exclude = ['user', 'product']
		widgets={
            'DiaryHeading':forms.TextInput(attrs={'placeholder':'Enter Title','class':'Headline'}),
            'DiaryBody':forms.Textarea(attrs={'placeholder':'Start Writing','class':'BodyDiary'}),
        }
        """