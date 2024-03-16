from django.shortcuts import render,redirect
from smartapp.models import Products,Cart,Address11,Order
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
from django.contrib import messages
import razorpay
import random
from django.core.mail import send_mail


# Create your views here.
def home(request):
    context={}
    data=Products.objects.all()
    context['products']=data
    return render(request,'index.html',context)

def contactus(request):
    return render(request,'contactus.html')

def profile(request):
    context={}
    user=request.user.id
    orderdetails=Order.objects.filter(uid=user)
    print('profile',orderdetails,user)
    context['data']=orderdetails
    return render(request,'profile.html',context)

def searchbycategory(request,val):
    context={}
    print(val)
    data=Products.objects.filter(type=val)
    context['products']=data
    return render(request,'index.html',context)

def sortbyprice(request,direction):
    col=''
    context={}
    if direction=='asc':
        col='price'
    else:
        col='-price'
    data=Products.objects.all().order_by(col)
    context['products']=data
    return render(request,'index.html',context)

def rangeofprice(request):
    context={}
    min=request.GET['min']
    max=request.GET['max']
    c1=Q(price__gte = min)
    c2=Q(price__lte = max)
    data=Products.objects.filter(c1 & c2)
    context['products']=data
    return render(request,'index.html',context)

def productdetails(request,pid):
    context={}
    data=Products.objects.filter(id= pid)
    context['value']=data[0]
    return render(request,'productdetails.html',context)

def register(request):
    context={}
    if request.method=='GET':
        return render(request,'register.html')
    else:
        n=request.POST['username']
        e=request.POST['useremail']
        p=request.POST['userpassword']
        cp=request.POST['confirmpassword']
        if n=='' or e=='' or p=='' or cp=='':
            context['error']='please fill all the details'
            return render(request,'register.html',context)
        elif p!=cp:
            context['error']='password and confirm password must be same'
            return render(request,'register.html',context)
        else:
            context['success']='Register successfully please login!!'
            users= User.objects.create(username=n,email=e)
            users.set_password(p)
            users.save()
            return render(request,'login.html',context)
   
def loginuser(request):
    if request.method=='GET':
        return render(request,'login.html')
    else:
        context={}
        n=request.POST['username']
        p=request.POST['password']
        if n=="" or p=="":
            context['error']="please fill all the details"
        else:
            user=authenticate(username=n,password=p)
            if user is not None:
                login(request,user)
                messages.success(request,'login successfully') 
                return redirect('/')
            else:
                context['error']="enter correct details"
                return render(request,'login.html',context)

def logoutuser(request):
    context={}
    logout(request)
    context['success']="logout successfully"
    return redirect('/')

def addtocart(request,productid):
    user=request.user.id
    if user is None:
        context={}
        context['error']='Please login'
        return render(request,'login.html',context)
    else:
        userid=request.user.id
        users=User.objects.filter(id=userid)
        products=Products.objects.filter(id=productid)
        cart=Cart.objects.create(pid=products[0],uid=users[0])
        cart.save()
        messages.success(request,'product added to cart') 
        return redirect('/')

def displaycart(request):
    context={}
    user=request.user.id
    data=Cart.objects.filter(uid=user)
    context['cart_items']=data
    count=len(data)
    total=0
    for item in data:
        total += item.pid.price * item.quantity 
    context['count']=count
    context['total']=total
    context['grandtotal']=total+5
    return render(request,'displaycart.html',context)

def placeorder(request):
    context={}
    user=request.user.id
    username=request.user.username
    useremail=request.user.email
    context['name']=username
    context['email']=useremail
    data=Cart.objects.filter(uid=user)
    context['cart_items']=data
    addresses = Address11.objects.filter(uid=user)
    print('user is : ' ,addresses)
    count=len(data)
    total=0
    for item in data:
        total += item.pid.price * item.quantity
    context['count']=count
    context['total']=total
    context['grandtotal']=total+5
    context['address'] = addresses
    return render(request,'placeorder.html',context)

def buynow(request,productid):
    user=request.user.id
    if user is None:
        context={}
        context['error']='Please login'
        return render(request,'login.html',context)
    else:
        userid=request.user.id
        users=User.objects.filter(id=userid)
        products=Products.objects.filter(id=productid)
        cart=Cart.objects.create(pid=products[0],uid=users[0])
        cart.save()
        
        context={}
        user=request.user.id
        data=Cart.objects.filter(uid=user)
        context['cart_items']=data
        count=len(data)
        total=0
        for item in data:
            total += item.pid.price * item.quantity
        context['count']=count
        context['total']=total
        context['grandtotal']=total+5
        return render(request,'displaycart.html',context)

def quantity(request,cartid,operation):
    data=Cart.objects.filter(id=cartid)
    cart=data[0]
    if operation == 'sub':
        data.update(quantity=cart.quantity - 1)
    else:
        data.update(quantity=cart.quantity + 1) 
    return redirect('/displaycart')

def removecart(request,cartid):
    data=Cart.objects.filter(id=cartid)
    data.delete()
    return redirect('/displaycart')

def addaddress(request):
    if request.method=='GET':
        return render(request,'address.html')
    else:
        context={}
        userid=request.user.id
        user = User.objects.get(id = userid)
        n=request.POST['name']
        m=request.POST['mobileno']
        p=request.POST['pincode']
        a=request.POST['address']
        c=request.POST['city']
        s=request.POST['state']
        data=Address11.objects.create(name=n,mobile_number=m,pincode=p,address=a,city=c,state=s,uid=user)
        data.save()
        # context['useraddress']=data
        return redirect ('/placeorder')
    
def update_address(request,aid):
    if request.method=='GET':
        a=Address11.objects.filter(id=aid)
        context={}
        context['address']=a[0]
        return render(request,'update_address.html',context)
    else:
        n=request.POST['name']
        m=request.POST['mobileno']
        p=request.POST['pincode']
        a=request.POST['address']
        c=request.POST['city']
        s=request.POST['state']
        add=Address11.objects.filter(id=aid)
        add.update(name=n,mobile_number=m,pincode=p,address=a,city=c,state=s)
        # context['useraddress']=data
        return redirect ('/placeorder')
    
def display_address(request):
    userid=request.user.id
    data=Address11.objects.filter(uid=userid)
    context={}
    context['users_address']=data
    return render(request,'display_address.html',context)  
    
def continuetopayment(request):
    '''
    get current userid
    calculating bill amnt:
        1.cart fetch
        2.using loop,find bill
    using razorpay make payment
    '''
    context={}
    userid=request.user.id
    data=Cart.objects.filter(uid=userid)
    total=0
    for cart in data:
        total += cart.pid.price * cart.quantity +5
    client = razorpay.Client(auth=("enter your razorpay key id","enter your razorpay secrete key"))
    data = {"amount":total*100, "currency":"INR","receipt":"" }
    payment = client.order.create(data=data)
    context['data'] = payment
    return render(request,'pay.html',context)

def confirmorder(request):
    userid=request.user.id
    # username=request.user.name
    user=User.objects.filter(id=userid)
    mycart=Cart.objects.filter(uid=userid)
    ordid= random.randrange(10000,99999)

    for cart in  mycart:
        pet=Products.objects.filter(id =cart.pid.id)
        ord=Order.objects.create(uid=user[0],pid=pet[0],quantity=cart.quantity,orderid=ordid)
        ord.save()
    mycart.delete()

    msg_body= ' Dear customer we hope this email finds you well and thriving. WE are reaching out to express our heartfelt gratitude for choosing to shop with us at S-MART .We are excited to confirm that we have received your recent order,and we are already hard at work proccessing it. your order id is :'+str(ordid)
    custEmail=request.user.email                #fetch users email
    send_mail(
        "order place successfully",       # email subject
        msg_body,
        "enter your email",  #from
        [custEmail],                         #to
        fail_silently=False,
    )
    messages.success(request,'order placed successfully!!')
    return redirect('/')

