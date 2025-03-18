from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.models import User
from .models import Department, Employee, Attendance, Leaves, Apology, Report, Profile

admin.site.register(Profile)
admin.site.register(Department)
admin.site.register(Employee)
admin.site.register(Attendance)
admin.site.register(Leaves)
admin.site.register(Apology)
admin.site.register(Report)
