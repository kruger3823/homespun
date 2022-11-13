from django import forms
from django.db.models import fields
from django.forms.fields import DateField
from . models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class UserForm(UserCreationForm):
    username=forms.CharField(help_text=None,label='Username')
    password1=forms.CharField(help_text=None,widget=forms.PasswordInput,label='Password')
    password2=forms.CharField(help_text=None,widget=forms.PasswordInput,label='Confirm Password')
    class Meta:
        model=User
        fields=('username','password1','password2','email')
        labels=('password1','password','password2','confirm password')
        
        
        
class stockForm(forms.ModelForm):
    class Meta:
        model=stock_det
        fields=('name','cate','qua','num')  
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'cate':forms.TextInput(attrs={'class':'form-control'}),
            'qua':forms.TextInput(attrs={'class':'form-control'}),
            'num':forms.TextInput(attrs={'class':'form-control'}),
        }    
       
        
          


        
class revwForm(forms.ModelForm):
    class Meta:
        model=revw
        fields=('pname','uname','review','rate')
        widgets={
            'pname':forms.TextInput(attrs={'class':'form-control'}),
            'uname':forms.TextInput(attrs={'class':'form-control'}),
            'review':forms.TextInput(attrs={'class':'form-control'}),
            'rate':forms.TextInput(attrs={'class':'form-control'}),
            
        } 


class ShopRegisterForm(forms.ModelForm):
    class Meta:
        model=Shop
        fields=('kudumbasree_unit','phone','license_no','location','proof','category')

        def _init_(self, *args, **kwargs):
            super()._init_(*args, **kwargs)
            self.fields['shop_name'].label = 'Test'


class TutorRegisterForm(forms.ModelForm):
    class Meta:
        model=HomeServicer
        fields=('phone','location')



class CustomerRegisterForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields=('phone','location')



class VolunteerRegisterForm(forms.ModelForm):
    class Meta:
        model=Volunteer
        fields=('phone','qualification','location','id_proof')



class UpdateForm(forms.ModelForm):
    username=forms.CharField(help_text=None,label='Username')
    
    class Meta:
        model=User
        fields=('username',)

class UpdateProfileForm(forms.ModelForm):
    address=forms.Textarea()
    
    class Meta:
        model=Volunteer
        fields=('phone','qualification','location','id_proof')


class VolunteerAvailabilityForm(forms.ModelForm):
    available='available'
    not_available='not_available'
    availability_statuses=[
        (available,'available'),
        (not_available,'not_available')
    ]
    availability_status=forms.ChoiceField(choices=availability_statuses,required=True)
    
    class Meta:
        model=Volunteer
        fields=('availability_status',)


class ServicerAvailabilityForm(forms.ModelForm):
    available='available'
    not_available='not_available'
    availability_statuses=[
        (available,'available'),
        (not_available,'not_available')
    ]
    availability_status=forms.ChoiceField(choices=availability_statuses,required=True)
    
    class Meta:
        model=HomeServicer
        fields=('availability_status',)



class BookingForm(forms.ModelForm):
    wanted_date=DateField(widget=forms.SelectDateWidget)
    class Meta:
        model=Booking
        fields=('wanted_date','place')

class UpdateBookingForm(forms.ModelForm):
    class Meta:
        model=Booking
        fields=('status','paid_status','amount')


