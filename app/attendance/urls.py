from django.urls import path

from . import views

app_name = 'myapp'

urlpatterns = [

    #coupled code for login.
    # required action for corresponding teacher/student is performed by checknig 'type' key in session
    path('login', views.login,name='login'), #login for student and teacher only


    #teacher's url
    path('teacher', views.teacher_dashboard,name='teacher_dashboard'), #dashboard panel for student and teacher only
    path('teacher/profile', views.teacher_profile,name='teacher_profile'), #need to handle not assigned courses and department
    path('teacher/ledger', views.teacher_ledger,name='teacher_legder'),
    path('teacher/missing_lectures', views.teacher_missingLectures,name='teacher_missing_lectures'),


    # for teachers only. Related to attendance broadcast.
    # this broadcast delete and creating was for testing by hotspot creation as id demo in Hackathon.
    # for future of this project out of scope. Needs modifiction as this process will be replaced by the Teacher GUI applicaion.
    # only for teachers
    path('broadcast', views.broadcastAttendance,name="broadcast"),
    path('broadCastDelete/<int:id>', views.broadcastDelete,name="broadcastDelete"),
    path('broadCastStop/<int:id>', views.broadcastStop,name="broadcastStop"),

    #student's panel
    path('student', views.student_dashboard,name='student_dashboard'),
    path('student/profile', views.student_profile,name='student_profile'), #need to handle not assigned courses and department
    path('student/ledger', views.student_ledger,name='student_ledger'),
    path('student/missing_lectures', views.student_missingLectures,name='student_missing_lectures'),

    #for student YesSir for broadcasted attendance
    path('yesSir/<int:id>', views.yesSir, name='yesSir'),

    # Error page
    path('404Error', views.error),

    # non classified urls
    path('', views.index,name='index'), #default url for application home page
    path('register', views.register,name='register'), #registered for student and teacher too, based on radio button value

    #logout for department/teacher/student.
    # just deleting the session key value
    path('logout', views.user_logout,name='logout'),

    # department related urls
    path('department', views.departmentLogin, name='department'), # department login panel url
    path('department/teacher',views.TeacherListView.as_view(), name='teacher_list'), #url redirected after login
    path('department/student/approve/<int:student_id>', views.approveStudent, name='approve_student'),
    path('department/student/remove/<int:student_id>', views.removeStudent, name='remove_student'),


    path('department/teacher/<int:pk>',views.TeacherDetailView.as_view(), name='teacher_detail'),
    path('department/student', views.ManageStudent.as_view(), name='manage_student'), #multiple view problem solved
    path('department/student/<int:pk>',views.StudentDetailView.as_view(), name='student_detail'), #direct access problem. security issue
    path('department/course', views.CourseListView.as_view(), name='course_list'),
    path('department/course/<int:pk>',views.CourseDetailView.as_view(), name='course_detail'),

]