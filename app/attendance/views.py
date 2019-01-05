from django.shortcuts import render
from .models import *

# Create your views here.

def index(request):
    return render(request,'app/index.html')

def login(request):
    return render(request,'app/login.html')

def register(request):
    if request.method == 'POST':
        r_name = request.POST['name']
        r_email = request.POST['email']
        r_phone = request.POST['phone']
        r_password = request.POST['password']
        r_confirm = request.POST['confirm']
        r_username = request.POST['username']
        regfor = request.POST['optradio']
        error = ''

        if r_password == r_confirm:
            if regfor == 'teacher':
                if not Teacher.objects.filter(username=r_username).exists():
                    Teacher.objects.create(name=r_name,username=r_username,email=r_email,password=r_password,phone_no=r_phone,pic_location='none')
                    error = {'message': 'User Created Succesfully'}
                else:
                    error = {'message':'User Already Exists'}


            if regfor == 'student':
                if not Student.objects.filter(username=r_username).exists():
                    Student.objects.create(name=r_name,username=r_username,email=r_email,password=r_password,phone_no=r_phone,pic_location='none')
                    error = {'message':'User Created Succesfully'}
                else:
                    error = {'message': 'User Already Exists'}

            return render(request, 'app/register.html',error)
        else:
            error = {'message': 'Password  Doesnt Matches'}

        return render(request, 'app/register.html', error)


    return render(request,'app/register.html')


