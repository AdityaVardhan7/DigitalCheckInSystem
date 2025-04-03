from django import forms
from django.contrib.auth.models import User
from .models import *

class UserRegisterForm(forms.ModelForm):
    # Additional fields for user registration
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    password = forms.CharField(widget=forms.PasswordInput())

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image', 'contact']

from .models import Department

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Department Name'}),
        }



from django import forms
from django.contrib.auth.models import User
from .models import Profile, Employee, Department


from django import forms
from django.contrib.auth.models import User
from .models import Employee, Department, Profile

class EmployeeForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
    )
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}),
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}),
    )
    profile_image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'}),
    )
    contact = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter contact number'}),
    )
    dep = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        empty_label="Select Department",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    role = forms.ChoiceField(
        choices=[('', 'Select Role')] + Employee.ROLE_CHOICES,  # Add a default option
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False  # Allow null values
    )
    status = forms.ChoiceField(
        choices=[("Active", "Active"), ("Inactive", "Inactive")],
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Employee
        fields = [
            'username', 'first_name', 'last_name', 'email', 'password',
            'profile_image', 'contact', 'dep', 'role', 'status'
        ]



class LeaveApplicationForm(forms.ModelForm):
    class Meta:
        model = Leaves
        fields = ['start_date', 'end_date', 'reason']
        widgets = {
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter reason for leave'}),
        }

class ApologyForm(forms.ModelForm):
    class Meta:
        model = Apology
        fields = ['date', 'reason']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter your reason...'}),
        }