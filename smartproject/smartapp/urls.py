
from django.urls import path
from smartapp import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',views.home),
    path('contactus',views.contactus),
    path('profile',views.profile),
    path('category/<val>',views.searchbycategory),
    path('sort/<direction>',views.sortbyprice),
    path('pricerange',views.rangeofprice),
    path('productdetails/<pid>',views.productdetails),
    path('register',views.register),
    path('login',views.loginuser),
    path('logout',views.logoutuser),
    path('addtocart/<productid>',views.addtocart),
    path('displaycart',views.displaycart),
    path('addtocart/<productid>/displaycart',views.buynow),
    path('updatequantity/<cartid>/<operation>',views.quantity),
    path('removecart/<cartid>',views.removecart),
    path('placeorder',views.placeorder),
    path('addaddress',views.addaddress),
    path('update_address/<aid>',views.update_address),
    path('display_address',views.display_address),
    path('continue_to_payment',views.continuetopayment),
    path('confirmorder',views.confirmorder),
 ]
urlpatterns += static(settings.MEDIA_URL,document_root= settings.MEDIA_ROOT)
