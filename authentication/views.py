from django.shortcuts import render,redirect,HttpResponse
from .models import *
from django.http import JsonResponse
from geopy.distance import geodesic
import json
from geopy.geocoders import Nominatim
from Articles.models import Articles,Gallery
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import random
from django.db.models import Sum

from functions import send_email_otp
from Product.models import SubCategory,Product
from Reservations_Reviews_Contact.models import Review


def online_ordering(request):
    return render(request,'order-online.html')

def menu_list():
    subcategories = SubCategory.objects.all()
    result_list = []

    for subcategory in subcategories:
        products = Product.objects.filter(subcategory=subcategory)
        
        if len(result_list) !=0 and len(result_list[-1]) !=2:

                result_list[-1].append({'subcategory': subcategory.name, 'products': products})
        else:
                result_list.append([{'subcategory': subcategory.name, 'products': products}])
                
                
    return result_list

from Reservations_Reviews_Contact.models import Review
def get_lat_long(address):
    geolocator = Nominatim(user_agent="user_agent")  # Replace with your app name
    location = geolocator.geocode(address)
    
    if location:
        latitude = location.latitude
        longitude = location.longitude
        return latitude, longitude
    else:
        return None
# address = "16 Headingley Lane, Headingley, Leeds, LS6 2AS"
address = "Leeds LS6 1BL"
result = get_lat_long(address)

if result:
    store_latitude, store_longitude = result

store_location = (store_latitude, store_longitude)  # Replace with actual coordinates
print("!@#@@!@@@!!@#@@",store_location)



def home(request):
    breakfast = Product.objects.filter(category__name ='Breakfast')
    lunch = Product.objects.filter(category__name ='Lunch')
    dinner = Product.objects.filter(category__name ='Dinner')
    drinks = Product.objects.filter(category__name ='Drinks')
    if request.user.is_authenticated:
        cart_item_list = [i.product.id for i in Cart.objects.filter(user=request.user)]
    else:
        cart_item_list=[]

    products = Product.objects.all()[::-1]
    
    articles = Articles.objects.order_by('-id').all()[:4]

    top_selling_products = Product.objects.annotate(
        total_quantity_sold=Sum('orderitem__quantity')
    ).order_by('-total_quantity_sold')[:10]

    reviews =Review.objects.order_by('-created_at').all()[:3]
    gallery_img=Gallery.objects.order_by('-id').all()[:10] 
    return render(request,'index-4.html',{'gallery_img':gallery_img,'title':'Home','reviews':reviews,'top_selling_products':top_selling_products,'articles':articles,'result_list':menu_list(),'products':products,'cart_item_list':cart_item_list,'breakfast':breakfast,'dinner':dinner,'lunch':lunch,'drinks':drinks})
    # return HttpResponse(result_list)


def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('pass')
        if User.objects.filter(email=email).exists():
            user = authenticate(request, username=email, password=password)
        else:
            messages.error(request,'Email is not registered')
            return redirect('register')
        if user:
            login(request, user)
            if not request.user.is_verified:
                return redirect('otp')
            
            return redirect('home')
        else:
            messages.error(request,'Wrong Password')
            return redirect('login')
        
    return render(request,"login.html",{'login':True,'title':'Login'})

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        password = request.POST.get('pass1')
        check = request.POST.get('check')
        
        if User.objects.filter(email=email).exists():
            messages.error(request,"Email Already Register.")
        
        
        user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=email,
                phone=mobile,
            )
        user.set_password(password)
        user.save()

        if check =='on':
            Newsletter.objects.create(email=email).save()
        user = authenticate(request, username=email, password=password)
        
        if user:
            login(request, user)
            return redirect('otp')


    return render(request,"login.html",{'register':True,'title':'Registere','result_list':menu_list()})

def logout_view(request):
    logout(request)
    return redirect('login')




def add_address(request):
    if request.method =='POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        add_line_1 = request.POST.get('add_line_1')
        add_line_2 = request.POST.get('add_line_2')
        city= request.POST.get('city')
        state= request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        mobile = request.POST.get('mobile')

        addresses = Address.objects.filter(user=request.user,is_default=True)
        for i in addresses:
            i.is_default = False
            i.save()

        Address.objects.create(user=request.user,first_name=first_name,last_name=last_name,address_line_1=add_line_1,address_line_2=add_line_2
                               ,city=city,state=state,postal_code=zip_code,mobile=mobile,is_default=True).save()

        

    return redirect('my-cart')

def my_profile(request):
    if not request.user.is_verified:
        messages.info(request,'Emil Not Verified !')
        return redirect('otp')
    address = Address.objects.filter(user = request.user)
    user = User.objects.get(email=request.user.email)
    slug= request.GET.get('slug')
    if request.method == 'POST':
        if slug == 'profile':
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            phone = request.POST.get('phone')
            
            user.first_name = fname
            user.last_name = lname
            user.phone = phone
            user.save()
        
        if slug == 'address':
            id = request.POST.get('id')
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            contact = request.POST.get('contact')
            address_line_1 = request.POST.get('address_line_1')
            address_line_2 = request.POST.get('address_line_2')
            city = request.POST.get('city')
            state = request.POST.get('state')
            postal_code = request.POST.get('postal_code')
            is_default = request.POST.get('is_default')
            
            add = Address.objects.get(id=id)
            add.first_name = fname
            add.last_name = lname
            add.mobile = contact
            add.address_line_1 = address_line_1
            add.address_line_2 = address_line_2
            add.city = city
            add.state = state
            add.postal_code = postal_code
            if is_default:
                for i in Address.objects.filter(user=request.user):
                    i.is_default = False
                    i.save()
                add.is_default = True
                
            add.save()
        return redirect('my-profile')
    if slug =='delete':
            id = request.GET.get('id')
            Address.objects.get(id=id).delete()
            if  Address.objects.filter(user=request.user).exists():
                for i in Address.objects.filter(user=request.user):
                        i.is_default = False
                        i.save()
                add =Address.objects.filter(user=request.user).first()
                add.is_default = True
                add.save()
            return redirect('my-profile')
        
    return render(request,'Profile.html',{'address':address,'title':'My Profile'})

def order_history(request):
    orders = Order.objects.filter(customer_email=request.user.email)[::-1]
    return render(request,'order-history.html',{'orders':orders,'title':'Order History'})







def otp(request):
    if request.user.is_authenticated:
        if request.user.is_verified :
            return redirect('home')
            
    if not request.user.is_verified:

        email = request.user.email
        user = User.objects.get(email=email)
        

        if request.method == 'POST':
            otp = request.POST.get('otp')
            print("!!!!!!!!!!!!!!!",otp)
            if int(user.otp) == int(otp):
                
                user.is_verified = True
                user.otp = ''
                user.save()

                request.session.pop('signup_email', None)
                messages.success(request,'Email Verified')
                return redirect('home')
                            
            else:
                messages.error(request,f'OTP Invalid {otp}')
                return redirect('otp')
            
        if len(str(user.otp)) != 6 :
            otp = random.randint(100000, 999999)
            user.otp = otp
            user.save()
        
        # send opt to email
            send_email_otp(user=user,otp=otp)
        else:
            messages.error(
                request,'Already Send on email'
            )
        return render(request,'otp.html',{'title':'OTP Verification'})




def add_cart(request):
    if not request.user.is_authenticated:
        return JsonResponse({'message': 'Login required'}, status=401)
    
    if request.GET.get('itemId'):
            id = request.GET.get('itemId')
            qty = int(request.GET.get('qty'))

            if qty == 0:
                return JsonResponse({'message': 'Error'}, status=400)

            product = Product.objects.get(id=id)
            if Cart.objects.filter(user=request.user,product=product).exists():
                cart_item = Cart.objects.get(user=request.user,product=product)
                cart_item.quantity =qty
                cart_item.total_price = round(cart_item.quantity * float(product.price),2)
                cart_item.save()
            else:
                cart_item = Cart.objects.create(user=request.user,product=product,quantity=int(qty),
                                                total_price =round(qty * float(product.price),2) )
                cart_item.save()
            print("!!!!!!!!",'added')
            return JsonResponse({'message': 'Added successfully'})
    else:
        return JsonResponse({'message': 'Invalid request'}, status=400)




# from django.shortcuts import redirect

# def session_cart(request):
#     if request.GET.get('itemId'):
#         id = request.GET.get('itemId')
#         qty = int(request.GET.get('qty'))

#         if qty == 0:
#             return JsonResponse({'message': 'Error'}, status=400)

#         product = Product.objects.get(id=id)

#         if request.user.is_authenticated:
#             # User is authenticated, proceed with the logic
#             try:
#                 cart = request.session.get('cart', [])
#                 total_price = round((qty * float(product.price)), 2)
#                 cart.append({'product': product, 'quantity': qty, 'total_price': total_price})
#                 request.session['cart'] = cart
#             except Exception as e:
#                 return JsonResponse({'error': str(e)})
#         else:
#             # User is not authenticated, redirect to a different URL
#             return redirect('session_cart')  # Assuming you have a 'session_cart' URL pattern

#         return JsonResponse({'message': 'Item added to cart successfully'})
#     else:
#         return JsonResponse({'message': 'Invalid request'}, status=400)

        
    
    


def remove_from_cart(request):
    if not request.user.is_authenticated:
        return JsonResponse({'message': 'Login required'}, status=400)

    if request.GET.get('itemId'):
        id = request.GET.get('itemId')

        product = Product.objects.get(id=id)
        if Cart.objects.filter(user=request.user, product=product).exists():
            cart_item = Cart.objects.get(user=request.user, product=product)
            cart_item.delete()

            return JsonResponse({'message': 'Removed'})
        else:
            return JsonResponse({'message': 'Item not found in the cart'}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request'}, status=400)



def update_session(request,addressId=None):
             
            # addressId = request.GET.get('addressId')
            if addressId != None: 
                for i in Address.objects.filter(user=request.user):
                    i.is_default = False
                    i.save()

                address = Address.objects.get(id=addressId)
                address.is_default = True
                address.save()
                full_address = f'{address.city}, {address.postal_code}'

                result = get_lat_long(full_address)

                if result:
                    user_latitude, user_longitude = result
                    user_location = (user_latitude, user_longitude)  # Replace with actual coordinates
                    distance_km = geodesic(store_location, user_location).meters

                request.session['distance_km'] = distance_km
                request.session['user_location'] = user_location  # Convert to a dictionary with x and y properties
            
            else:
                for i in Address.objects.filter(user=request.user):
                    i.is_default = False
                    i.save()
                add_id =request.GET.get('addressId')
                address = Address.objects.get(id=add_id)
                address.is_default = True
                address.save()
                return redirect('my-cart')


def my_cart(request):
    if not request.user.is_authenticated:
        return redirect('login')

    
 
        # If not, send a request to update_session with the default addressId
    try :
        default_address = Address.objects.get(user=request.user,is_default=True)
    except:
        default_address = None
    if default_address:
            update_session(request, addressId=default_address.id)

    cart_items = Cart.objects.filter(user=request.user)
    Subtotal_price = 0

    for i in cart_items:
        Subtotal_price = float(Subtotal_price + float(i.total_price)) 
    
    addresses = Address.objects.filter(user=request.user)
    try: 
        # delivery_price = float((int(request.session['distance_km'])*10))
        delivery_price =0
        total_price = Subtotal_price + 0
    except:
        delivery_price =0
        total_price = Subtotal_price
        
    return render(request,'my-cart.html',{'title':'My Cart','result_list':menu_list(),'cart_items':cart_items,'addresses':addresses,'total_price':total_price,'delivery_price':delivery_price,'Subtotal_price':Subtotal_price})


def privacypolicy(request):
    return render(request,'privacy-policy.html',{'title':'Privacy Policy','result_list':menu_list()})

def gallery(request):
    gallery_img = Gallery.objects.all()[::-1]
    return render(request,'gallery.html',{'gallery_img':gallery_img,'title':'Gallery','result_list':menu_list()})

def about(request):
    return render(request,'about.html',{'title':'About','result_list':menu_list()})




def forget_password(request):
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()
        return redirect('login')
    
    
    if  request.method == 'GET':
        email = request.GET.get('email')
        otp =  request.GET.get('otp')
        if email:
            if otp:
                user = User.objects.get(email=email)
                if int(user.otp) == int(otp):
                    
                    user.is_verified = True
                    user.otp = ''
                    user.save()
                    return JsonResponse({'User':'Verified'})
                else:
                    return JsonResponse({'User':'Not Verified'})
                    

                    
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                if  len(str(user.otp)) != 6 :
                    otp = random.randint(100000, 999999)
                    user.otp = otp
                    user.save()
                
                # send opt to email
                    send_email_otp(user=user,otp=otp)
                
                return JsonResponse({'User':'Exist'})
            else:
                return JsonResponse({'User':'Not Exist'})

        
    return render(request,'forget.html')