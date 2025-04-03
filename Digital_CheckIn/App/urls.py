from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='Index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('admin-dashboard', views.admin_dashboard, name="admin-dashboard"),
    path('employees/', views.employees, name='employees'),
    path('add-employee/', views.add_employee, name='add_employee'),
    path('employees/delete/<int:employee_id>/', views.delete_employee, name='delete_employee'),
    path('employees/update/<int:employee_id>/', views.update_employee, name='update_employee'),
    path('departments/', views.departments, name='departments'),
    path('add-department/', views.add_department, name='add_department'),
    path('department/update/<int:department_id>/', views.update_department, name="update_department"),
    path('department/delete/<int:department_id>/', views.delete_department, name="delete_department"),
    path('profile/', views.user_profile, name='profile'),

    
   
    path('admin-attendance/', views.attendance_list, name='attendance_list'),   
    path('capture-attendance/', views.capture_face, name='capture_attendance'),
    path('process_image/', views.process_image, name='process_image'),
    path('mannual/', views.mannual, name="mannual"),
    path('toggle-attendance/<int:employee_id>/', views.toggle_attendance, name='toggle_attendance'),
    path('attendance/export/', views.export_attendance, name='export_attendance'),


    path('leaves/', views.leave_list, name='leave_list'),
    path('leave/<int:leave_id>/<str:status>/', views.update_leave_status, name='update_leave_status'),
    
    path('apologies/', views.apology_list, name='apology_list'),
    path('apology/<int:apology_id>/<str:status>/', views.update_apology_status, name='update_apology_status'),
    



    # Employee features
    path('employee-dashboard', views.employee_dashboard, name="employee-dashboard"),
    path('my-attendance/', views.my_attendance, name='my_attendance'),


    path('leave-history/', views.leave_history, name='leave_history'),
    path('apply-leave/', views.apply_leave, name='apply_leave'),
    path('leave/edit/<int:leave_id>/', views.edit_leave, name='edit_leave'),
    path('leave/delete/<int:leave_id>/', views.delete_leave, name='delete_leave'),


    path('apology-history/', views.apology_history, name='apology_history'),
    path('submit-apology/', views.submit_apology, name='submit_apology'),
    path('apology/edit/<int:apology_id>/', views.edit_apology, name='edit_apology'),
    path('apology/delete/<int:apology_id>/', views.delete_apology, name='delete_apology'),






]
