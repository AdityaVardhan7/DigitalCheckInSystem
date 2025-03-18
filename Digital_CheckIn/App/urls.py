from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='Index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('admin-dashboard', views.admin_dashboard, name="admin-dashboard"),
    path('employees/', views.employees, name='employees'),
    path('add-employee/', views.add_employee, name='add_employee'),
    path('employees/delete/<int:employee_id>/', views.delete_employee, name='delete_employee'),
    path('employees/update/<int:employee_id>/', views.update_employee, name='update_employee'),
    path('departments/', views.departments, name='departments'),
    path('add-department/', views.add_department, name='add_department'),
    path('department/update/<int:department_id>/', views.update_department, name="update_department"),
    path('department/delete/<int:department_id>/', views.delete_department, name="delete_department"),
    path('admin-profile/', views.admin_profile, name='admin-profile'),

    
    path('face-recognition/', views.recognize_employee, name="face-recognition"),
    # path('check_in/', views.check_in_with_camera, name='check_in_with_camera'),
    path('admin-attendance/', views.attendance_list, name='attendance_list'),
    path('check_in/', views.check_in, name='check_in'),
    path('recognize_face/', views.recognize_face, name='recognize_face'),


]
