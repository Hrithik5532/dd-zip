from django.shortcuts import render,redirect,HttpResponse
from .models import Product,SubCategory
from authentication.models import Cart,OrderItem,Order,Address
from django.db.models import Q
import paypalrestsdk
from functions import send_email_order_confirm
from authentication.views import menu_list
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

paypalrestsdk.configure({
    "mode": "sandbox",  # or "live"
    "client_id": "ATpf7nvhrmIQKiOh3aVwTtr1ElkasrtmYl5yjAj68zpCJFiG8sQeZBMsJn6fOAV8oI2-ecTKEXtWcsLL",
    "client_secret": "EMtjs8aKxlQNGfMvMsLO5jseDuRGYP0M7x0Ynt7RQAnzSA2dZzDDtB3OKQEJkicSIotM4YKkTruRsPVw"
})


# Create your views here.
def menu(request):

    products =  Product.objects.all()[::-1]
    if request.user.is_authenticated:
        cart_item_list = [i.product.id for i in Cart.objects.filter(user=request.user)]
    else:
        cart_item_list=[]
    
    breakfast = Product.objects.filter(category__name ='Breakfast')
    lunch = Product.objects.filter(category__name ='Lunch')
    dinner = Product.objects.filter(category__name ='Dinner')
    drinks = Product.objects.filter(category__name ='Drinks')
    subcategory = SubCategory.objects.all()
    filter_products= None
    if request.GET.get('filter')=='on':
        search = request.GET.get('search')
        veg = request.GET.get('veg')
        nonveg = request.GET.get('noneveg')
        bestSeller = request.GET.get('bestSeller')
        topRated = request.GET.get('topRated')

        if search != None:
            filter_products = Product.objects.filter(
                Q(name__icontains=search) | Q(description__icontains=search) | Q(category__name__icontains=search) | Q(subcategory__name__icontains=search)
                    ).distinct()
        else:
            filter_products =  Product.objects.all()[::-1]
        
        if veg == 'on':
            filter_products = Product.objects.filter(veg_or_Nonveg ='Veg')


        if nonveg == 'on':
            filter_products = Product.objects.filter(veg_or_Nonveg ='Non-Veg')

    return render(request,'menu-1.html',{'title':'Menu','result_list':menu_list(),'filter_products':filter_products,'subcategory':subcategory,'drinks':drinks,'dinner':dinner,'lunch':lunch,'breakfast':breakfast,'products':products,'cart_item_list':cart_item_list})


def order_create(request):
    if not request.user.is_authenticated:
        return redirect('login')
 
    
    order_type = request.POST.get('order_type',"Delivery")

    cart_items = Cart.objects.filter(user=request.user)
    try :
        address = Address.objects.get(user=request.user,is_default=True)
    except :
        messages.error(request,"Please add Address")
        return render()

        
        
        
    order = Order.objects.create(
        customer_first_name = request.user.first_name,
        customer_last_name = request.user.last_name,
        customer_contact = request.user.phone,
        customer_email = request.user.email,
        address_line_1 = address.address_line_1,
        address_line_2 = address.address_line_2,
        city = address.city,
        state = address.state,
        postal_code = address.postal_code,

        payment_status= 'Pending',
        order_type=order_type
    )
    sub_total = 0
    for i in cart_items:
        order_item = OrderItem.objects.create(
            product = i.product,
            quantity = i.quantity,
            total= i.total_price,
            price = i.product.price,

        )
        sub_total = round(float(sub_total) + float(i.total_price),2)
        order.order_items.add(order_item)
        order.sub_total = sub_total
        order.save()

    order.deliveryCharges = 0
    order.total = round(float(order.sub_total) + (0),2)
    order.save()
    
    
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": "http://127.0.0.1:8000/order-menu/payment/execute/",
            "cancel_url": "http://127.0.0.1:8000/order-menu/payment/cancel/"
        },
        "transactions": [{
            "amount": {
                "total": order.total,
                "currency": "eur"
            },
            "description": "Payment description"
        }]
    })


    if payment.create():
        request.session['paypal_payment_id'] = payment.id
        order.payment_id = payment.id
        order.save()
        for link in payment.links:
            if link.method == "REDIRECT":
                redirect_url = str(link.href)
                return redirect(redirect_url)


    else:
        messages.error(request,"Payment Canceled")
        return render(request,'payment-failed.html',{'title':'Payment Failed','order':order,'payment':payment})


@csrf_exempt
def payment_execute(request):

    
    payment_id = request.session.get('paypal_payment_id')
    if payment_id is None:
        return redirect('home')
    
    payment = paypalrestsdk.Payment.find(payment_id)
    if payment:
      
        order = Order.objects.get(payment_id=payment_id)
       
      

        order.payment_amount = order.total
        order.payment_status = "Completed"
        order.save()

        Cart.objects.filter(user=request.user).delete()
        send_email_order_confirm(request,request.user,order,'success')
        cntx={
                    'payment':payment,
                    'order':order
        }
        # You can perform any additional actions here, such as updating your database
        messages.success(request,'Order Placed! You can check on order Track')
        return render(request,'order-success.html',cntx)
    else:
        # Payment failed
        order = Order.objects.filter(payment_id=payment_id)[0]
        
       
        order.payment_status = "Failed"
        order.save()

        send_email_order_confirm(request,request.user,order,'failed')

    return render(request, 'payment-failed.html',{'title':'Payment Failed','result_list':menu_list()})    
    # return render(request, 'order-success.html')
