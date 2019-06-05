from django.urls import path

from . import views

app_name = 'myapp'

urlpatterns = [

    # please place the url accordingly

    # for students panel and teacher panel. Highly coupled code
    # required action for corresponding teacher/student is performed by checknig 'type' key in session
    path('user_panel', views.user_panel,name='user_panel'),
    path('user_panel/profile', views.profile,name='user_profile'),
    path('user_panel/ledger', views.ledger,name='basic_tables'), #shows the attendance leger for student and teacher
    path('login', views.login,name='login'), #login for student and teacher only

    # for teachers only. Related to attendance broadcast.
    # this broadcast delete and creating was for testing by hotspot creation as id demo in Hackathon.
    # for future of this project out of scope. Needs modifiction
    # only for teachers
    path('broadcast', views.broadcastAttendance,name="broadcast"),
    path('broadCastDelete/<int:id>', views.broadcastDelete,name="broadcastDelete"),
    path('broadCastStop/<int:id>', views.broadcastStop,name="broadcastStop"),

    # for students
    path('yesSir/<int:id>', views.yesSir, name='yesSir'),
    path('user_panel/missing_lectures', views.missingLectures,name='missing_lectures'),

    # Error page
    path('404Error', views.error),

    # non classified urls
    path('', views.index,name='index'), #default url for application home page
    path('register', views.register,name='register'), #registered for student and teacher too, based on radio button value


    #logout for department/teacher/student.
    # just deleting the session key value
    path('logout', views.user_logout,name='logout'),



    # department related urls
    path('department', views.departmentLogin, name='department'), # this url is loaded before department login and form data is fetched and redirected as per need
    path('department/teacher',views.TeacherListView.as_view(), name='teacher_list'),
    path('department/teacher/<int:pk>',views.TeacherDetailView.as_view(), name='teacher_detail'),
    path('department/student', views.ManageStudent.as_view(), name='manage_student'), #multiple view problem solved
    path('department/student/<int:pk>',views.StudentDetailView.as_view(), name='student_detail'), #direct access problem. security issue
    path('department/course', views.CourseListView.as_view(), name='course_list'),
    path('department/course/<int:pk>',views.CourseDetailView.as_view(), name='course_detail'),
    path('department/student/approve/<int:student_id>',views.approveStudent, name='approve_student'),
    path('department/student/remove/<int:student_id>',views.removeStudent, name='remove_student'),

]