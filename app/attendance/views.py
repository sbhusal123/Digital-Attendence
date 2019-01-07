from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect
from .models import *
from django.shortcuts import render_to_response
from django.template import RequestContext


# Create your views here.

def profile(request):
    s_username = request.session['username']
    type = request.session['type']
    context = ''

    #authentication
    if 'username' not in request.session:
        return redirect('/404Error')
    else:
        if type == 'teacher':
            context = Teacher.objects.filter(username=s_username)

        elif type == 'student':
            context = Student.objects.filter(username=s_username)


    #updating_fields
    if request.method == 'POST':
        model = ''
        u_email = request.POST['email']
        u_password = request.POST['password']
        u_phone = request.POST['phone']

        if type == 'teacher':
            model = Teacher.objects.get(username=s_username)

        elif type == 'student':
            model = Student.objects.get(username=s_username)

        model.email = u_email
        model.password = u_password
        model.phone_no = u_phone
        model.save()
        pass

    return render(request,'admin_panel/profile.html', {'details':context})

def user_logout(request):
    if 'username' and 'type' in request.session:
        del request.session['username']
        del request.session['type']

    return redirect('/login')



def index(request):
    return render(request,'app/index.html')

def user_panel(request): #dashboard page

    if 'username' not in request.session:
        return redirect('/404Error')

    type = request.session['type']

    if type == 'student':
        return render(request,'admin_panel/student/index.html')

    elif type == 'teacher':
        broadcast_set =  active_broadcast(request.session['username'])
        return render(request, 'admin_panel/teacher/index.html',{'active_broadcast':broadcast_set})


def active_broadcast(teacher_name):
    broadcastingTeacher_id = Teacher.objects.get(username=teacher_name)
    try:
        cls = Class.objects.filter(t_id = broadcastingTeacher_id,broadcast_attendance=True)
        return cls
    except(Class.DoesNotExist):
       pass

def broadcastDelete(request,id):
    if 'username' not in request.session:
        return redirect('/404Error')

    Class.objects.get(id=id).delete()
    return redirect('/user_panel')
    pass

def broadcastStop(request,id):
    if 'username' not in request.session:
        return redirect('/404Error')
    c = Class.objects.get(id=id)
    c.broadcast_attendance = False
    c.save()
    return redirect('/user_panel')
    pass








def basic_tables(request):
    if 'username' not in request.session:
        return redirect('/404Error')
    return render(request, 'admin_panel/basic-table.html')

def error(request):
    return render(request,'admin_panel/404.html')

def login(request):
    if 'username' in request.session:
        return redirect('/user_panel')

    if request.method == "POST":
        l_username = request.POST['username']
        l_password = request.POST['password']
        logfor = request.POST['optradio']

        message = ''

        if logfor =='student':
            if Student.objects.filter(username = l_username,password = l_password).exists():
                request.session['username'] = l_username
                request.session['type'] = logfor
                response = HttpResponseRedirect('/user_panel')
                return response
            else:
                message = 'Not a valid User. Enter Valid Details'

        elif logfor =='teacher':
            if Teacher.objects.filter(username=l_username, password=l_password).exists():
                request.session['username'] = l_username
                request.session['type'] = logfor
                response = HttpResponseRedirect('/user_panel')
                return response
            else:
                message = 'Not a valid User. Enter Valid Details'

        return render(request, 'app/login.html',{'message':message})

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


def broadcastAttendance(request):
    if 'username' in request.session and request.session['type'] == 'teacher':
        if request.method == 'POST':
            teacher_username =  request.session['username']
            bt_id = Teacher.objects.get(username=teacher_username)
            b_date = request.POST['date']
            b_time = request.POST['time']
            Class.objects.create(t_id = bt_id,date=b_date,time = b_time,broadcast_attendance=True)
            return redirect('/user_panel')
        else:
            return redirect('/user_panel')

    else:
        return redirect('/404Error')