from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect
from .models import *
from django.shortcuts import render_to_response


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
        broadcast_set = broadcast_list(request.session['username'])
        return render(request,'admin_panel/student/index.html',{'active_broadcast':broadcast_set})

    elif type == 'teacher':
        broadcast_set =  active_broadcast(request.session['username']) #fetching the active broadcasting done by teacher
        dep = Department.objects.all()
        course = Course.objects.all()
        context = {'department': dep, 'course': course,'active_broadcast':broadcast_set}
        return render(request, 'admin_panel/teacher/index.html',context)


def active_broadcast(teacher_name): #for teachere
    broadcastingTeacher_id = Teacher.objects.get(username=teacher_name)
    try:
        cls = Class.objects.filter(t_id = broadcastingTeacher_id,broadcast_attendance=True)
        return cls
    except(Class.DoesNotExist):
       pass

def broadcast_list(student_name): #for student
    #condition are:
    # teaher and student must be from same department
    # teacher and student in same course
    # broadcast_attendance = True in Class model
    # attendance table doesn't consists of the pra class id.
    try:
        active_broadcast = Class.objects.filter(broadcast_attendance=True) #filter list of active attendance

    except(Class.DoesNotExist):
        return HttpResponseRedirect('/user_profile',{'errormsg':'No broadcasting Yet.'})

    student_id = Student.objects.get(username=student_name).id #logged in student id



    student_dep_id = From.objects.get(s = student_id).d.id #student from deptid


    student_enrolled_course = Enroll.objects.filter(s = student_id)

    # surround with try catch here.
    student_attended_class = Attends.objects.all()

    for b in active_broadcast:
        if b.dep_id.id == student_dep_id:
            for course in student_enrolled_course:
                if course.c.id == b.course_id.id:
                    # now i've got the way to extract which broadcast to display
                    # to which student
                    #now i need to check whether the such class_id exists in the attends class or not
                    if Attends.objects.filter(cl_id = b.id,std_id = student_id).exists():
                        pass
                    else:
                        return b





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
        teacher_username = request.session['username']
        bt_id = Teacher.objects.get(username=teacher_username)
        if request.method == 'POST':

            try:
                b = Class.objects.get(broadcast_attendance=True,t_id=bt_id)
                print('asd')
                return HttpResponseRedirect('user_panel',{'msg':'Cannot broadcast more than one attendance.'})

            except(Class.DoesNotExist):
                dep_id = Department.objects.get(pk=request.POST['department'])
                course_id = Course.objects.get(pk=request.POST['course'])
                Class.objects.create(t_id = bt_id,broadcast_attendance=True,dep_id=dep_id,course_id=course_id)
                return HttpResponseRedirect('user_panel',{'msg': 'Attendance broadcasted succesfully.'})

        else:
            return redirect('/user_panel')

    else:

        return redirect('/404Error')

def yesSir(request,id):
    std_id = Student.objects.get(username = request.session["username"])
    cl_id = Class.objects.get(id=id)
    Attends.objects.create(cl_id = cl_id,std_id=std_id)
    return redirect('/user_panel')