from django.urls import path

from . import views

app_name = 'myapp'

urlpatterns = [
    path('', views.index,name='index'),
    path('login', views.login,name='login'),
    path('register', views.register,name='register'),
    path('user_panel', views.user_panel,name='user_panel'),
    path('user_panel/ledger', views.ledger,name='basic_tables'),
    path('user_panel/profile', views.profile,name='user_profile'),
    path('logout', views.user_logout,name='logout'),
    path('404Error', views.error),
    path('broadcast', views.broadcastAttendance,name="broadcast"),
    path('broadCastDelete/<int:id>', views.broadcastDelete,name="broadcastDelete"),
    path('broadCastStop/<int:id>', views.broadcastStop,name="broadcastStop"),
    path('yesSir/<int:id>', views.yesSir, name='yesSir'),
    path('user_panel/missing_lectures', views.missingLectures,name='missing_lectures'),
    #modified by suyen
    path('department', views.departmentLogin, name='department'), # this url is loaded before department login and form data is fetched and redirected as per need
    path('department/teacher',views.TeacherListView.as_view(), name='teacher_list'),
    path('department/teacher/<int:pk>',views.TeacherDetailView.as_view(), name='teacher_detail'),
    path('department/student', views.StudentListView.as_view(), name='student_list'),
    path('department/student/<int:pk>',views.StudentDetailView.as_view(), name='student_detail'),
    path('department/course', views.CourseListView.as_view(), name='course_list'),
    path('department/course/<int:pk>',views.CourseDetailView.as_view(), name='course_detail'),
    #modified by surya


]