from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from Onlinegrocery import models

class Userregister(UserCreationForm):
	password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Enter You Password"}))
	password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Enter You Confirm Password"}))
	class Meta:
		model = User
		fields = ["first_name","last_name","email","username"]
		widgets = {
		"first_name": forms.TextInput(attrs = {
			"class":"form-control",
			"placeholder":"Enter Your First Name",
			"required":True,
			}),
		"last_name": forms.TextInput(attrs = {
			"class":"form-control",
			"placeholder":"Enter Your Last Name",
			}),
		"email": forms.EmailInput(attrs = {
			"class":"form-control",
			"placeholder":"Enter Your Email",
			"required":True,
			}),
		"username": forms.TextInput(attrs = {
			"class":"form-control",
			"placeholder":"Enter Your User Name",
			"required":True,
			}),
		}

class ProductForm(forms.ModelForm):
	class Meta:
		model = models.Product
		fields = ['productname','price','description','category','product_image']
		widgets = {
		"productname":forms.TextInput(attrs={
			"class":"form-control",
			"placeholder":"Enter Your Product Name",
			"required":True,
			}),
		"price":forms.NumberInput(attrs={
			"class":"form-control",
			"placeholder":"Enter Your Product Price",
			"required":True,
			}),
		"description":forms.Textarea(attrs={
			"class":"form-control",
			"rows":5,
			"cols":10,
			"placeholder":"Enter Your Product Discription",
			"required":True,
			}),
		"category":forms.Select(attrs={
			"class":"form-control",
			}),
		}

class AddressForm(forms.Form):
	Email = forms.EmailField()
	Mobile = forms.IntegerField()
	Address = forms.CharField(max_length=500)







    # Name = forms.CharField(max_length=30)
    # Email = forms.EmailField()
    # Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))