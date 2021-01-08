from django.shortcuts import render,redirect
from django.http import HttpResponse
from Onlinegrocery.forms import Userregister
from ecommerce import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Onlinegrocery.models import Product
from Onlinegrocery import forms,models

# Create your views here.

# User views start from here

def home(request):
	products=models.Product.objects.all()
	return render(request,'html/home.html',{'products':products})

@login_required
def myorder(request):
	return render(request,'html/myorders.html')

def about(request):
	return render(request,'html/about.html')

def contact(request):
	# sub = forms.ContactusForm()
	# if request.method == 'POST':
	# 	sub = forms.ContactusForm(request.POST)
	# 	if sub.is_valid():
	# 		email = sub.cleaned_data['Email']
	# 		name=sub.cleaned_data['Name']
	# 		message = sub.cleaned_data['Message']
	# 		send_mail(str(name)+' || '+str(email),message, settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
	# 		# return render(request, 'ecom/contactussuccess.html')
	return render(request,'html/contact.html')

@login_required
def userdashboard(request):	
	return render(request,'html/admindashboard.html')

def register(request):
	if request.method == "POST":
		a = Userregister(request.POST)
		if a.is_valid():
			p = a.save(commit=False)
			rc = p.email
			sb = "Welcome to Onlinegrocery"
			msg = "Dear {},You have successfully created your Onlinegrocery account.Congratulations and welcome to a whole new world of grocery shopping.Your details: password:{}".format(p.username,p.password)
			sd = settings.EMAIL_HOST_USER
			snt = send_mail(sb,msg,sd,[rc])
			if snt == 1:
				p.save()
				messages.success(request,"Please check your {} for login creadentials".format(rc))
				return redirect("/lg")
	a = Userregister()
	return render(request,'html/register.html',{'b':a})

@login_required
def addtocart(request,pk):
	products = models.Product.objects.all()
	if 'product_ids' in request.COOKIES:
		product_ids = request.COOKIES['product_ids']
		counter = product_ids.split('|')
		product_count_in_cart = len(set(counter))
	else:
		product_count_in_cart = 1

	response = render(request,'html/home.html',{'products':products,'product_count_in_cart':product_count_in_cart})

	if 'product_ids' in request.COOKIES:
		product_ids = request.COOKIES['product_ids']
		if product_ids == "":
			product_ids = str(pk)
		else:
			product_ids = product_ids+"|"+str(pk)
		response.set_cookie('product_ids',product_ids)
	else:
		response.set_cookie('product_ids',pk)

	product = models.Product.objects.get(id=pk)
	messages.success(request,product.productname + 'Added to cart successfully !'
		)
	return response


def cart(request):
	if 'product_ids' in request.COOKIES:
		product_ids = request.COOKIES['product_ids']
		counter = product_ids.split('|')
		product_count_in_cart = len(set(counter))
	else:
		product_count_in_cart = 0

	products = None
	total = 0
	if 'product_ids' in request.COOKIES:
		product_ids = request.COOKIES['product_ids']
		if product_ids != "":
			product_id_in_cart = product_ids.split('|')
			products = models.Product.objects.all().filter(id__in = product_id_in_cart)

			for k in products:
				total = total+k.price
	return render(request,'html/cart.html',{'products':products,'total':total,'product_count_in_cart':product_count_in_cart})


def removefromcart(request,pk):
	if 'product_ids' in request.COOKIES:
		product_ids = request.COOKIES['product_ids']
		counter = product_ids.split('|')
		product_count_in_cart = len(set(counter))
	else:
		product_count_in_cart = 0

	total = 0
	if 'product_ids' in request.COOKIES:
		product_ids = request.COOKIES['product_ids']
		product_id_in_cart = product_ids.split('|')
		product_id_in_cart = list(set(product_id_in_cart))
		product_id_in_cart.remove(str(pk))
		products = models.Product.objects.all().filter(id__in = product_id_in_cart)

		for k in products:
			total = total+k.price

		value=""
		for i in range(len(product_id_in_cart)):
			if i==0:
				value=value+product_id_in_cart[0]
			else:
				value=value+"|"+product_id_in_cart[i]
		response = render(request,'html/cart.html',{'products':products,'total':total,'product_count_in_cart':product_count_in_cart})
		if value =="":
			response.delete_cookie('product_ids')
		response.set_cookie('product_ids',value)
		return response

@login_required
def customeraddress(request):
	product_in_cart = False
	if 'product_ids' in request.COOKIES:
		product_ids = request.COOKIES['product_ids']
		if product_ids != "":
			product_id_in_cart = True

	if 'product_ids' in request.COOKIES:
		product_ids = request.COOKIES['product_ids']
		counter = product_ids.split('|')
		product_count_in_cart = len(set(counter))
	else:
		product_count_in_cart = 0

	# addressForm = forms.AddressForm()
	if request.method == "POST":
		addressForm = forms.AddressForm(request.POST)
		if addressForm.is_valid():

			email = addressForm.cleaned_data['Email']
			mobile = addressForm.cleaned_data['Mobile']
			address = addressForm.cleaned_data['Address']

			total = 0
			if 'product_ids' in request.COOKIES:
				product_ids = request.COOKIES['product_ids']
				if product_ids != "":
					product_id_in_cart = product_ids.split('|')
					products = models.Product.objects.all().filter(id__in = product_id_in_cart)
					for k in products:
						total = total+k.price

			response = render(request,'html/payment.html',{'total':total})
			response.set_cookie('email',email)
			response.set_cookie('mobile',mobile)
			response.set_cookie('address',address)
			return response
	return render(request,'html/customeraddress.html',{'product_in_cart':product_in_cart,'product_count_in_cart':product_count_in_cart})

@login_required
def paymentsuccess(request):
	customer = models.Customer.objects.get(user_id=request.user.id)
	product = None
	email = None
	mobile = None
	address = None
	if 'product_ids' in request.COOKIES:
		product_ids = request.COOKIES['product_ids']
		if product_ids != "":
			product_id_in_cart = product_ids.split('|')
			products = models.Product.objects.all().filter(id__in=product_id_in_cart)
	

# User views ended 

# Admin views starts from here 

@login_required
def admindashboard(request):
	productcount=models.Product.objects.all().count()
	ordercount=models.Orders.objects.all().count()
	orders = models.Orders.objects.all()
	ordered_products = []
	ordered_buys = []
	for order in orders:
		ordered_product = models.Product.objects.all().filter(id = order.product.id)
		ordered_buys = models.Customer.objects.all().filter(id = order.customer.id)
		ordered_products.append(ordered_product)
		ordered_buys.append(ordered_buys)

	mydict = {
	'productcount':productcount,
	'ordercount':ordercount,
	'data':zip(ordered_products,ordered_buys,orders)
	}
	return render(request,'html/admindashboard.html',context=mydict)

@login_required
def products(request):
    productss = models.Product.objects.all()
    return render(request, 'html/productscatalogue.html', {'pro':productss})

@login_required
def addproducts(request):
	a = forms.ProductForm()
	if request.method == "POST":
		a = forms.ProductForm(request.POST,request.FILES)
		if a.is_valid():
			a.save()
			messages.success(request,"{} you have successfully added a new product details in productscatalogue".format(request.user.username))
			return redirect('/prod')
	return render(request,'html/addproducts.html',{'k':a})

@login_required
def updateproducts(request,pk):
	product = models.Product.objects.get(id=pk)
	productForm = forms.ProductForm(instance = product)
	if request.method == "POST":
		productForm = forms.ProductForm(request.POST,request.FILES,instance=product)
		if productForm.is_valid():
			productForm.save()
			messages.warning(request,"{} you have successfully updated the product details in productscatalogue".format(request.user.username))
		return redirect('/prod')	
	return render(request,'html/updateproduct.html',{'productForm':productForm})

@login_required
def deleteproducts(request,pk):
	product = models.Product.objects.filter(id=pk)
	if request.method == "POST":
		product.delete()
		messages.warning(request,"{} you have successfully deleted the product from productscatalogue".format(request.user.username))
		return redirect('/prod')
	return render(request,'html/deleteproduct.html')

@login_required
def updatesoon(request):
	return render(request,'html/updatesoon.html')