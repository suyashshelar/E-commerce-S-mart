from django.contrib import admin
from smartapp.models import Products,Cart,Order

# Register your models here.
class ProductsAdmin(admin.ModelAdmin):
    list_display=['id','name','type','quantity','details','price','pimage']
    list_filter=['type','quantity','price']
admin.site.register(Products,ProductsAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display=['id','pid','uid','quantity']
admin.site.register(Cart,CartAdmin)

class OredrAdmin(admin.ModelAdmin):
    list_display= ['id','orderid','uid','pid','quantity']
admin.site.register(Order,OredrAdmin)