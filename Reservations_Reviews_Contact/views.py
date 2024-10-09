from django.shortcuts import render,redirect
from .models import ContactUs,Reservation,Review, Career
from django.contrib import messages
from Product.models import Product
from authentication.models import Order,Newsletter
from authentication.views import menu_list
from datetime import datetime

from functions import send_email_contact, send_email_reservation,send_email_newsletter
# Create your views here.
def contact_us(request):
    if request.method == 'POST':
        if  request.GET.get('form')=='jobpost':
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            file = request.FILES['file']

            if Career.objects.filter(email=email).exists():
                messages.error(request,'Already Applied')
                return redirect('contact_us')
            Career.objects.create(name=name,email=email,phone=phone,file=file).save()
            messages.success(request,'Applied successfully')
            return redirect('contact_us')

        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        contact = ContactUs.objects.create(name=name,email=email,phone=phone,message=message)
        contact.save()
        send_email_contact(request,email,name,contact.created_at)
        messages.success(request,'Submited successfully')
        return redirect('contact_us')
    
    return render(request,'contact.html',{'title':'Contact Us','result_list':menu_list()})


def reservation(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        date = request.POST.get('date')
        time = request.POST.get('time')
        persons = request.POST.get('persons')
        
        message = request.POST.get('message',None)
        if Reservation.objects.filter(email=email,phone=phone,date=date,time=time).exists():

            messages.error(request,f'Already Booked  With Email : {email} \n Date : {date}\n Time : {time}')
            return redirect('home')
        

        reservation = Reservation.objects.create(name=name,email=email,phone=phone,message=message,date=date,time=time,no_persons=persons)
        reservation.save()

        send_email_reservation(request,reservation)
        messages.success(request,'Submited successfully')
        return redirect('home')
    
    return render(request,'reservation.html',{'title':'Reservation','result_list':menu_list()})


def newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if Newsletter.objects.filter(email=email).exists():
            send_email_newsletter(email)
            messages.error(request,'Email Already Subscribed')
        else:
            Newsletter.objects.create(email=email).save()
            messages.success(request,"Thank You for Subscribtion !")
            return redirect('home')
            
    return redirect('home')

def review(request):
    if request.method=='POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        file = request.FILES['file']
        item_id = request.POST.get('item_id')
        order_id = request.POST.get('order_id')
        rating = request.POST.get('rating')
        review = Review.objects.create(name=name,email=email,phone=phone,message=message,created_at = datetime.now()
                                       )
        
        if file:
            review.file = file
        if item_id:
            review.item = Product.objects.get(id= item_id)
        if  order_id:
            review.order = Order.objects.get(id = order_id)
        if  rating:
            review.rating = rating
        review.save()
        messages.success(request,"thank you for your Review")
        return redirect('home')
    items = Product.objects.all().distinct()
    if request.user.is_authenticated:
        orders = Order.objects.filter(customer_email = request.user.email)
    else:
        orders = []
    reviwes = Review.objects.order_by("-created_at").all().distinct()
    if request.GET.get('orderId'):
        selected_order_id = int(request.GET.get('orderId'))
    else:
        selected_order_id =None
    star_range = [1,2,3,4,5]
    return render(request,'review-form.html',{'title':'Reviews','star_range':star_range,'items':items,'orders':orders,'reviwes':reviwes,'selected_order_id':selected_order_id,'result_list':menu_list()})