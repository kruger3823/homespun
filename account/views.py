from multiprocessing import context
from os import closerange
from django.http.response import Http404
from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from . models import *
from . forms import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render
from .models import Post




# Create your views here.


def index(request):
    return render(request,'index.html')
def rating(request):
    return render(request,'rating.html')
def review(request):
    if request.method=="POST":
        pname=request.POST.get('pname')
        uname=request.POST.get('uname')
        review=request.POST.get('review')
        rate=request.POST.get('rate')
        shop=request.POST.get('shop')
       
        revw(pname=pname,uname=uname,review=review,rate=rate,shop=shop).save()
    return render(request,'review.html')
def view_stock(request):
    cr=stock_det.objects.filter(user__id=request.user.id)
    return render(request,'view_stock.html',{'cr':cr})

def view_review(request):
    cr=revw.objects.all()
    return render(request,'view_review.html',{'cr':cr})

def stock_details(request):
    if request.method=="POST":
        name=request.POST.get('name')
        cate=request.POST.get('cate')
        qua=request.POST.get('qua')
        num=request.POST.get('num')
        stock_det(name=name,cate=cate,qua=qua,num=num,user=request.user).save()
    return render(request,'stock_details.html')



def shop_register(request):
    reg=False
    if request.method=='POST':
        user_form=UserForm(data=request.POST)
        shop_form=ShopRegisterForm(request.POST,request.FILES)
        if user_form.is_valid() and shop_form.is_valid():
            user=user_form.save()
            user.save()
            profile=shop_form.save(commit=False)
            profile.user=user
            profile.save()

            reg=True
            return redirect('user_login')
        else:
            HttpResponse("invalid form")
    else:
         user_form=UserForm()
         shop_form=ShopRegisterForm()
    return render(request,'shop_register.html',{'register':reg,'user_form':user_form,'shop_form':shop_form}) 




def tutor_register(request):
    reg=False
    if request.method=='POST':
        user_form=UserForm(data=request.POST)
        tutor_form=TutorRegisterForm(request.POST,request.FILES)
        if user_form.is_valid() and tutor_form.is_valid():
            user=user_form.save()
            user.save()
            profile=tutor_form.save(commit=False)
            profile.user=user
            profile.save()

            reg=True
            return redirect('user_login')
        else:
            HttpResponse("invalid form")
    else:
         user_form=UserForm()
         tutor_form=TutorRegisterForm()
    return render(request,'tutor_register.html',{'register':reg,'user_form':user_form,'tutor_form':tutor_form}) 



def customer_register(request):
    reg=False
    if request.method=='POST':
        user_form=UserForm(data=request.POST)
        customer_form=CustomerRegisterForm(request.POST,request.FILES)
        if user_form.is_valid() and customer_form.is_valid():
            user=user_form.save()
            user.save()
            profile=customer_form.save(commit=False)
            profile.user=user
            profile.save()

            reg=True
            return redirect('user_login')
        else:
            HttpResponse("invalid form")
    else:
         user_form=UserForm()
         customer_form=CustomerRegisterForm()
    return render(request,'customer_register.html',{'register':reg,'user_form':user_form,'customer_form':customer_form}) 



def volunteer_register(request):
    reg=False
    if request.method=='POST':
        shop=Shop.objects.get(user=request.user)
        print(shop)
        user_form=UserForm(data=request.POST)
        volunteer_form=VolunteerRegisterForm(request.POST,request.FILES)
        if user_form.is_valid() and volunteer_form.is_valid():
            user=user_form.save()
            user.save()
            profile=volunteer_form.save(commit=False)

            profile.user=user
            profile.shop=shop
            profile.save()

            reg=True
            return redirect('user_login')
        else:
            HttpResponse("invalid form")
    else:
         user_form=UserForm()
         volunteer_form=VolunteerRegisterForm()
    return render(request,'volunteer_register.html',{'register':reg,'user_form':user_form,'volunteer_form':volunteer_form}) 



def registrations(request):
    return render(request,'registrations.html')




def user_login(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('dashboard'))
            else:
                return HttpResponse("Not active")
        else:
            return HttpResponse("Invalid username or password")
    else:
        
        return render(request,'login.html')


def dashboard(request):
    #list=Todo.objects.all()
    return render(request,'dashboard.html')



@login_required
def user_logout(request):
    logout(request)
    return redirect('index')



def volunteer(request):
    our_volunteer=Volunteer.objects.filter(shop=request.user.shop,availability_status='available')
    print(our_volunteer)
    return render(request,'our_volunteer.html',{'our_volunteer':our_volunteer})


def update_volunteer(request,volunteer_id):
    my_volunteer=Volunteer.objects.get(id=volunteer_id)
    if request.method=="POST":
        my_volunteer=Volunteer.objects.get(id=volunteer_id)
        update_form=UpdateForm(request.POST,instance=my_volunteer.user)
        
        update_profile_form=UpdateProfileForm(request.POST,instance=my_volunteer)
        
        if update_form.is_valid() and update_profile_form.is_valid():
            update_form.save()
            update_profile_form.save()
            messages.success(request,f'Your Account has been Updated')
            return redirect('dashboard')
    else:
        update_form=UpdateForm(instance=my_volunteer.user)
        update_profile_form=UpdateProfileForm(instance=my_volunteer)
    context={
        'update_form':update_form,
        'update_profile_form':update_profile_form
    }
    return render(request,'update_volunteer.html',context)



def delete_volunteer(request,id):
    deleteemp = Volunteer.objects.get(id=id)
    deleteemp.delete()
    messages.success(request,'Record deleted succefully')
    return redirect('volunteer')



def home_servicers(request):
    category=HomeServicerCategory.objects.all()
    if request.method=="GET":
        category=HomeServicerCategory.objects.all()
        location=request.GET.get('location')
        category1=request.GET.get('category')
        try:
            servicer=HomeServicer.objects.filter(location__icontains=location) and HomeServicer.objects.filter(category=category1,availability_status='available')
            print(servicer)
            return render(request,'home_servicers.html',{'servicer':servicer,'category':category})
        except:
            pass
        
    return render(request,'home_servicers.html',{'category':category})



def servicer_booking(request,servicer_id):
    servicer=HomeServicer.objects.get(id=servicer_id)
    if request.method=="POST":
        servicer=HomeServicer.objects.get(id=servicer_id)
        booking_form=BookingForm(request.POST)
        if booking_form.is_valid():
            bookings=Booking(customer=request.user.customer,wanted_date=booking_form.cleaned_data['wanted_date'],place=booking_form.cleaned_data['place'])
            bookings.servicer=servicer
            bookings.save()
            return redirect('view_customer_bookings')
        else:
            return HttpResponse("Invalid Form")
    booking_form=BookingForm()
    return render(request,'booking_form.html',{'booking_form':booking_form})


def view_customer_bookings(request):
    customer_bookings=Booking.objects.filter(customer=request.user.customer)
    
    print(customer_bookings)
    return render(request,'view_bookings.html',{'customer_bookings':customer_bookings})


def view_servicer_bookings(request):
    servicer_bookings=Booking.objects.filter(servicer=request.user.homeservicer)
    print(servicer_bookings)
    return render(request,'view_bookings.html',{'servicer_bookings':servicer_bookings})


def delete_booking(request,id):
    delete_booking = Booking.objects.get(id=id)
    delete_booking.delete()
    messages.success(request,'Record deleted succefully')
    return redirect('view_customer_bookings')


def update_booking(request,booking_id):
    booking=Booking.objects.get(id=booking_id)
    print(booking)
    update_booking_form=UpdateBookingForm(instance=booking)
    if request.method=="POST":
        update_booking_form=UpdateBookingForm(request.POST,request.FILES,instance=booking)
        update_booking_form.save()
        return redirect('view_servicer_bookings')
    return render(request,'update_bookings.html',{'update_booking_form':update_booking_form})



def update_availablity_volunteer(request):
    my_volunteer=Volunteer.objects.get(user=request.user)
    print(my_volunteer.availability_status)
    if request.method=="POST":
        my_volunteer=Volunteer.objects.get(user=request.user)
        update_form=VolunteerAvailabilityForm(request.POST,instance=my_volunteer)
        print(my_volunteer.availability_status)
        if update_form.is_valid():
            update_form.save()
            
            messages.success(request,f'Your Account has been Updated')
            return redirect('dashboard')
    else:
        update_form=VolunteerAvailabilityForm(instance=my_volunteer.user)
        
    context={
        'update_form':update_form,
        
    }
    return render(request,'update_volunteer_availability.html',context)



def update_availablity_servicer(request):
    my_servicer=HomeServicer.objects.get(user=request.user)
    print(my_servicer.availability_status)
    if request.method=="POST":
        my_servicer=HomeServicer.objects.get(user=request.user)
        update_form=ServicerAvailabilityForm(request.POST,instance=my_servicer)
        print(my_servicer.availability_status)
        if update_form.is_valid():
            update_form.save()
            
            messages.success(request,f'Your Account has been Updated')
            return redirect('dashboard')
    else:
        update_form=VolunteerAvailabilityForm(instance=my_servicer.user)
        
    context={
        'update_form':update_form,
        
    }
    return render(request,'update_servicer_availability.html',context)

def service_workers(request, category):
    try:
        hsc, _ = HomeServicerCategory.objects.get_or_create(servicer_category_name = category)
        data = HomeServicer.objects.filter(category = hsc)
        return render(request, 'account/service_workers.html', {'data': data})
    except Exception as e:
        print(e)
        raise Http404









def createpost(request):
        if request.method == 'POST':
            if request.POST.get('filename') and request.POST.get('description') and request.POST.get('file'):
                post=Post()
                post.filename= request.POST.get('filename')
                post.description= request.POST.get('description')
                post.file= request.POST.get('file')
                post.save()
                meg="Uploaded successully"
                
                return redirect('dashboard')  

        else:
                meg='failed'
                return render(request,'uploadd.html')





def showvideo(request):
     alldata= Post.objects.all()
     context={'Post':alldata}
     return render(request,'show.html',context)

def ssvideo(request):
     alldata= Post.objects.all()
     context={'Post':alldata}
     return render(request,'show.html',context)

    


