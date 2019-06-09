from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Q
from .models import *
from django.urls import reverse
import os


#new imports:
from django.views.generic import (View,TemplateView,
                                ListView,DetailView,
                                CreateView, UpdateView,
                                DeleteView)
import datetime

from django.contrib.auth.mixins import LoginRequiredMixin #login required for class views



# Create your views here.

def profile(request):
    context = ''

    #authentication
    if 'username' not in request.session:
        return redirect('/404Error')
    else:
        s_username = request.session['username']
        type = request.session['type']
        if type == 'teacher':
            context = Teacher.objects.filter(username=s_username)

        elif type == 'student':
            context = Student.objects.filter(username=s_username)
        elif type == "department":
            return HttpResponse("Department Profile is under construction.")


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
        try:
            '''
            surrounded with try catch because the following code checks the database for
            exietence of the some entity in the Class and Attends table.
            
            What if the system is fresh and runing for first time without the data on the tables
            mentioned above.
            '''
            broadcast_set = broadcast_list(request.session['username'])  # active attendance broadcast fetched
            today = datetime.date.today

            student_tuple = Student.objects.get(username=request.session["username"])
            # for today attended class. Context name = today_attended_class_detail, returns Associated objects
            class_object_for_attended_class = Class.objects.filter(attends__std_id = student_tuple)

            associated_object_for_attended_class = Associated.objects.filter(class_id__in = class_object_for_attended_class)




            return render(request, 'admin_panel/student/dashboard.html',
                          {'active_broadcast': broadcast_set, 'today_attended_class_detail': associated_object_for_attended_class, 'today': today})
        except:
            return render(request, 'admin_panel/student/dashboard.html')



    elif type == 'teacher':
        teacher_object = Teacher.objects.get(username=request.session['username'])
        context = {}
        try:
            #placed inside try because if active broadcast doesn't exists then returns error.
            broadcast_set =  active_broadcast(request.session['username'])  # fetching the active broadcasting done by teacher
            context["active_broadcast"] = broadcast_set
        except:
            context["no_active_broadcast"] = 'No active broadcast exists.'

        if Teaches.objects.filter(t = teacher_object) and worksFor.objects.filter(t = teacher_object):

            broadcasting_department_choice = worksFor.objects.filter(t = teacher_object) #checknig weather the teacher is assigned to department

            broadcasing_course_choioce =  Teaches.objects.filter(t = teacher_object) #checking weather the teacher is assigned to course

            context['worksFor'] = broadcasting_department_choice
            context['teaches'] = broadcasing_course_choioce
             #later edit
            return render(request, 'admin_panel/teacher/dashboard.html',context)
        else:
            context ['error_message'] = "Please contact department administrator. You are not assigned to department or course"
            return render(request, 'admin_panel/teacher/dashboard.html',context)

    elif type == "department":
        return HttpResponse("Dashboard page is under construction.")




def active_broadcast(teacher_name): #for teachere
    broadcastingTeacher_id = Teacher.objects.get(username=teacher_name)
    try:
        cls = Associated.objects.filter(t_id = broadcastingTeacher_id,class_id__broadcast_attendance = True)
        return cls
    except(Class.DoesNotExist):
       pass

def broadcast_list(student_name): #for student
    # Returns the corresponding associated object for following suitable condition

    #condition are:
    # teaher and student must be from same department
    # teacher and student in same course
    # broadcast_attendance = True in Class model
    # attendance table doesn't consists of the broadcasted class id.

    try:
        active_broadcast = Class.objects.filter(broadcast_attendance=True) #filter list of active attendance

    except:
        return HttpResponseRedirect('/user_profile',{'errormsg':'No broadcasting Yet.'})

    student_id = Student.objects.get(username=student_name) #logged in student id
    student_dep_id = From.objects.get(s = student_id).d #student from deptid
    student_enrolled_course = Enroll.objects.filter(s = student_id) #student_enrolled courses
    enrolled_course_list = []
    for enroll in student_enrolled_course:
        enrolled_course_list.append(enroll.c.name)


    # surround with try catch here.
    student_attended_class = Attends.objects.all()


    active_associated =  Associated.objects.filter(class_id__broadcast_attendance=True,dep_id = student_dep_id,
                                                   course_id__name__in=enrolled_course_list)

    for b in active_associated:
        print(b.class_id.id)
        if Attends.objects.filter(cl_id = b.class_id, std_id = student_id):
            pass
        else:
            return b


def broadcastDelete(request,id):
    # remocing the class removes the objects from associated as well as class object
    if 'username' not in request.session:
        return redirect('/404Error')
    associated_object = Associated.objects.get(id=id)
    Associated.objects.get(id=id).delete() #remove the associated tuple
    Class.objects.get(id = associated_object.class_id.id).delete() #remove the class tuple
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


def ledger(request):
    if 'username' not in request.session:
        return redirect('/404Error')

    if request.session["type"] == "student":
        student_tuple = Student.objects.get(username=request.session["username"])
        course = Enroll.objects.filter(s=student_tuple)
        attended_class = Attends.objects.filter(std_id = student_tuple)

        if request.method == 'POST':  # for filtering the records
            date = request.POST["date"]
            date =  datetime.datetime.strptime(date, "%b. %d, %Y").date()
            course_filter = request.POST["course"]
            return render(request, 'admin_panel/student/basic-table.html',
                          {'attended_class': attended_class, 'course': course,'date_filter':date,'course_filter':course_filter})

        else:
            return render(request, 'admin_panel/student/basic-table.html',{'attended_class':attended_class,'course':course})

    if request.session["type"] == "teacher":
        return render(request, 'admin_panel/teacher/basic-table.html')


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
                response = HttpResponseRedirect(reverse('myapp:user_panel'))#here,reverse is used to avoid hardcoded urls.
                return response
            else:
                message = 'Not a valid User. Enter Valid Details'

        elif logfor =='teacher':
            if Teacher.objects.filter(username=l_username, password=l_password).exists():
                request.session['username'] = l_username
                request.session['type'] = logfor
                response = HttpResponseRedirect(reverse('myapp:user_panel')) #here,reverse is used to avoid hardcoded urls.
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
        broadcasting_teacher_id = Teacher.objects.get(username=teacher_username)
        if request.method == 'POST':
            if Associated.objects.filter(class_id__broadcast_attendance=True,t_id = broadcasting_teacher_id):
                return HttpResponse("Cannot broadcast more than one attendance at a time.")

            else:
                dep_id = Department.objects.get(name=request.POST['department_name'])
                course_id = Course.objects.get(name=request.POST['course_name'])
                # Class.objects.create(t_id = bt_id,broadcast_attendance=True,dep_id=dep_id,course_id=course_id)

                broadcasted_class =  Class.objects.create(broadcast_attendance=True)

                broadcasted_class.save()

                Associated.objects.create(t_id = broadcasting_teacher_id,dep_id = dep_id,course_id = course_id,class_id = broadcasted_class)

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

def missingLectures(request):
    if 'username' in request.session and request.session["type"] == "student":
        course = Enroll.objects.filter(s__username__contains=request.session["username"])
        missing = Attends.objects.filter(~Q(std_id__username__contains=request.session["username"]))

        if request.method == 'POST':
            course_filter = request.POST["course"]
            return render(request,'admin_panel/student/blank.html',{'missing':missing,'course':course,'course_filter':course_filter})
        else:
            return render(request, 'admin_panel/student/blank.html',{'missing': missing, 'course': course})

    elif 'username' in request.session and request.session["type"] == "teacher":
        return render(request,'admin_panel/teacher/blank.html')
    else:
        return redirect('/404Error')


def departmentLogin(request):

    if "type" in request.session and request.session["type"] == "department":
        return HttpResponseRedirect(reverse('myapp:teacher_list'))

    elif "type" not in request.session:
        if request.method == "POST":
            l_username = request.POST['username']
            l_password = request.POST['password']
            if Department.objects.filter(name=l_username, password=l_password).exists():
                request.session["username"] = l_username #creates a session variable named dep_name to store which dep logged in
                request.session['type'] = "department"
                return HttpResponseRedirect(reverse('myapp:teacher_list'))
            else:
                return render(request, 'admin_panel/department/department_login.html', {'message':'Invalid password'})

        else:
            dep_list = Department.objects.all()
            context = {'dep_list':dep_list}
            return render(request,'admin_panel/department/department_login.html',context) #as shown template file has been moved



def approveStudent(request,student_id):
    logged_in_department =  request.session["username"]
    currently_logged_in_department =  Department.objects.get(name = logged_in_department)
    selected_student = Student.objects.get(pk = student_id)

    From.objects.create(s=selected_student,d = currently_logged_in_department)
    return redirect('/department/student') #need to pass message saying that student has been verified

def removeStudent(request,student_id):
    logged_in_department = request.session["username"]
    currently_logged_in_department = Department.objects.get(name=logged_in_department)
    selected_student = Student.objects.get(pk=student_id)
    From.objects.get(s=selected_student,d = currently_logged_in_department).delete()
    return redirect('/department/student')

class ManageStudent(ListView):
    # Students pending for department approval
    model = Student
    template_name = "admin_panel/department/manage_student.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ManageStudent, self).get_context_data(*args, **kwargs)
        logged_in_department_name = self.request.session["username"]

        loged_in_dep_object = Department.objects.get(name = logged_in_department_name)
        context['pending_students'] =  Student.objects.filter(from__d__isnull=True)
        context['approved_student'] = From.objects.filter(d = loged_in_dep_object)
        return context



class TeacherListView(ListView): #Login required class list view
    context_object_name = 'teachers'
    model = Teacher
    template_name = "admin_panel/department/teacher_list.html"
#     Security issue with the url. if url is directly provided acces is passed instead of foridding.





class TeacherDetailView(DetailView):
    context_object_name = 'teacher_detail'
    model = Teacher
    template_name = "admin_panel/department/teacher_detail.html"
    #     Security issue with the url. if url is directly provided acces is passed instead of foridding.



class StudentEnrolledListView(ListView):
    # Students in the current department
    #  as the department name is stored in the session. Passing to the template and then comparing with dep name
    context_object_name = 'students'
    model = Student #from
    template_name = "admin_panel/department/manage_student.html"



class StudentDetailView(DetailView):
    # This is to show the students detail on click the student name in "department/student" in Students enrolled in current department
    context_object_name = 'student_detail'
    model = Student
    template_name = "admin_panel/department/manage_student.html"
    #     Security issue with the url. if url is directly provided acces is passed instead of foridding.

class CourseListView(ListView):
    context_object_name = 'courses'
    model = Course
    template_name = "admin_panel/department/course_detail.html"
    #     Security issue with the url. if url is directly provided acces is passed instead of foridding.

class CourseDetailView(DetailView):
    context_object_name = 'course_detail'
    model = Course
    template_name = "admin_panel/department/course_detail.html"
    #     Security issue with the url. if url is directly provided acces is passed instead of foridding.
