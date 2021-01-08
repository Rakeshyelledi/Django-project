from django.contrib import admin
from django.urls import path
from Onlinegrocery import views
from django.contrib.auth import views as v

urlpatterns = [ 
	path("",views.home,name="hom"),

	# admin releated urls starts from here 

	# path('admin/', admin.site.urls),
	path("admlg/",v.LoginView.as_view(template_name="html/adminlogin.html"),name="adlgn"),
	path("adminds/",views.admindashboard,name="addsh"),
	path("prod/",views.products,name="prodt"),
	path("addprod/",views.addproducts,name="addprodt"),
	path("deleprod/<int:pk>",views.deleteproducts,name='del'),
	path("updatprod/<int:pk>",views.updateproducts,name="update"),
	
	# admin urls ended

	path("abt/",views.about,name="abot"),
	path("cnt/",views.contact,name="cont"),
	path("reg/",views.register,name="regist"),	
	path("lg/",v.LoginView.as_view(template_name="html/login.html"),name="lgn"),
	path("log/",v.LogoutView.as_view(template_name="html/logout.html"),name="logt"),
	path("adcr/<int:pk>", views.addtocart,name="adtcrt"),
	path("cr",views.cart,name="crt"),
	path("rmcr/<int:pk>",views.removefromcart,name="remcrt"),
	path("cusadr",views.customeraddress,name="custaddrs"),
	path("pay",views.paymentsuccess,name="payment"),
	path("myord/",views.myorder,name="myorde"),

	path("upson",views.updatesoon,name="soon")
]