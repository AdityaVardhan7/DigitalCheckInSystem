from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ProfileUpdateForm, EmployeeForm
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404

from django.contrib.auth.decorators import user_passes_test

def superuser_check(user):
    if not user.is_superuser:
        messages.error(user, "Access Denied! Only admins can view this page.")
    return user.is_superuser

# User login view

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Log in the user

            # Redirect based on user type
            if user.is_superuser:
                return redirect('admin-dashboard')  # Redirect superuser to admin dashboard
            else:
                return redirect('profile')  # Redirect normal user to profile page
    else:
        form = AuthenticationForm()
    
    return render(request, 'account/login.html', {'form': form})

# User logout view
def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout


# User registration view
def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            Profile.objects.create(user=user)  # Create profile for new user
            return redirect('login')  # Redirect to login after registration
    else:
        user_form = UserRegisterForm()
    
    return render(request, 'account/register.html', {'user_form': user_form})

# Profile update view
@login_required
def profile(request):
    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile')  # Redirect to the profile page after update
    else:
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    return render(request, 'account/profile.html', {'profile_form': profile_form})


@user_passes_test(lambda user: user.is_superuser, login_url='login')
def admin_profile(request):
    user = request.user
    
    # Fetch or create the Employee & Profile objects
    employee, created = Employee.objects.get_or_create(user=user)
    profile, created = Profile.objects.get_or_create(user=user)

    title = "My Profile"

    if request.method == "POST":
        form = EmployeeForm(request.POST, request.FILES, instance=employee)

        if form.is_valid():
            # Update User model
            user.username = form.cleaned_data['username']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()

            # Update Profile model
            profile.contact = form.cleaned_data['contact']
            if 'profile_image' in request.FILES:
                profile.profile_image = request.FILES['profile_image']  # Save new profile image
            profile.save()

            # Update Employee model
            employee = form.save(commit=False)
            employee.user = user  # Ensure correct user assignment
            employee.save()

            messages.success(request, "Profile updated successfully!")
            return redirect('admin-profile')  # Redirect back to the profile page

        else:
            messages.error(request, "Please correct the errors below.")  # Show form errors

    else:
        # Pre-fill form with existing data
        form = EmployeeForm(instance=employee, initial={
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'contact': profile.contact,
        })

    return render(request, 'admin/profile.html', {'form': form, 'employee': employee, 'title': title})

@user_passes_test(lambda user: user.is_superuser, login_url='login')
def admin_dashboard(request):
    total_employees = Employee.objects.filter(status="Active").count() 
    present = 0
    absent = total_employees-present

    context = {
        'total_employees': total_employees,
        'present': present,
        'absent': absent

    }
    return render(request, 'admin/dashboard.html', context)

@user_passes_test(lambda user: user.is_superuser, login_url='login')
def employees(request):
    employees = Employee.objects.all()
    return render(request, 'admin/employees.html', {'employees': employees})


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError, transaction
from .models import Profile, Employee
from .forms import EmployeeForm

@user_passes_test(lambda user: user.is_superuser, login_url='login')
def add_employee(request):
    title = "Add New Employee"
    if request.method == "POST":
        form = EmployeeForm(request.POST, request.FILES)  # Handle file uploads (profile image)
        if form.is_valid():
            try:
                with transaction.atomic():  # Ensures all objects are created together
                    # Create User
                    user = User.objects.create_user(
                        username=form.cleaned_data['username'],
                        first_name=form.cleaned_data['first_name'],
                        last_name=form.cleaned_data['last_name'],
                        email=form.cleaned_data['email'],
                        password=form.cleaned_data['password']
                    )

                    # Create Profile
                    profile = Profile.objects.create(
                        user=user,
                        profile_image=form.cleaned_data['profile_image'],
                        contact=form.cleaned_data['contact']
                    )

                    # Create Employee
                    employee = Employee.objects.create(
                        user=user,
                        dep=form.cleaned_data['dep'],
                        role=form.cleaned_data['role'],
                        status=form.cleaned_data['status']
                    )

                messages.success(request, "Employee added successfully!")
                return redirect('employees')  # Redirect to employee list page

            except IntegrityError:
                messages.error(request, "Username already exists. Please choose a different username.")
    
    else:
        form = EmployeeForm()
    
    return render(request, 'admin/add_employee.html', {'form': form, 'title': title})


@user_passes_test(lambda user: user.is_superuser, login_url='login')
def delete_employee(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    user = employee.user  # Get associated user before deleting employee
    employee.delete()
    user.delete()  # Delete associated user
    messages.success(request, "Employee deleted successfully!")
    return redirect('employees')


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Employee, Profile
from .forms import EmployeeForm

@user_passes_test(lambda user: user.is_superuser, login_url='login')
def update_employee(request, employee_id):
    
    employee = get_object_or_404(Employee, pk=employee_id)
    user = employee.user  # Associated User object
    profile, created = Profile.objects.get_or_create(user=user)  # Ensure profile exists
    title = "Update Employee ("+ user.first_name +" "+ user.last_name + ")"

    if request.method == "POST":
        form = EmployeeForm(request.POST, request.FILES, instance=employee)

        if form.is_valid():
            # Update User model
            user.username = form.cleaned_data['username']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()

            # Update Profile model
            profile.contact = form.cleaned_data['contact']
            if 'profile_image' in request.FILES:
                profile.profile_image = request.FILES['profile_image']  # Save new profile image
            profile.save()

            # Update Employee model
            employee = form.save(commit=False)
            employee.user = user  # Ensure correct user assignment
            employee.save()

            messages.success(request, "Employee updated successfully!")
            return redirect('employees')  # Redirect to employee list page

        else:
            print("Form Errors:", form.errors)
            messages.error(request, "Please correct the errors below.")  # Show form errors


    else:
        # Pre-fill form with existing data
        form = EmployeeForm(instance=employee, initial={
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'password': user.password,
            'contact': profile.contact,
        })

    return render(request, 'admin/add_employee.html', {'form': form, 'employee': employee, 'title': title})


@user_passes_test(lambda user: user.is_superuser, login_url='login')
def departments(request):
    departments = Department.objects.all()  # Fetch all departments
    return render(request, 'admin/departments.html', {'departments': departments})


from .forms import DepartmentForm

@user_passes_test(lambda user: user.is_superuser, login_url='login')
def add_department(request):
    if request.method == "POST":
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Department added successfully!")
            return redirect('departments')  # Redirect to department list view after adding
    else:
        form = DepartmentForm()
    
    return render(request, 'admin/addDepartment.html', {'form': form})


def update_department(request, department_id):
    department = get_object_or_404(Department, pk=department_id)

    if request.method == "POST":
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, "Department updated successfully!")
            return redirect("departments")  # Change to your department list view
        else:
            messages.error(request, "Error updating department. Please check the form.")
    else:
        form = DepartmentForm(instance=department)

    return render(request, "admin/update_department.html", {"form": form, "department": department})

@user_passes_test(lambda user: user.is_superuser, login_url='login')
def delete_department(request, department_id):
    department = get_object_or_404(Department, pk=department_id)
    department.delete()
    messages.success(request, "Department deleted successfully!")
    return redirect("departments")  # Redirect to department list after deletion



def recognize_employee(request):
     return render(request, 'attendance/recognition.html')


import cv2
import face_recognition
import numpy as np
from .models import Employee, Profile, Attendance
from django.http import JsonResponse
from django.utils import timezone

def check_in_with_camera(request):
    """View that captures a face image from the webcam and processes it for recognition."""
    
    # Open the webcam
    cap = cv2.VideoCapture(0)  # 0 is the default webcam

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            # If frame is not captured properly, break the loop
            break
        
        # Convert the frame from BGR to RGB (face_recognition uses RGB)
        rgb_frame = frame[:, :, ::-1]

        # Find all face locations and face encodings in the current frame
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        recognized = False  # To track if the face is recognized

        # Loop through all detected faces
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Draw a rectangle around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Crop the face from the frame to display a zoomed-in version
            face_image = frame[top:bottom, left:right]

            # Show the cropped face in a new window
            cv2.imshow("Cropped Face", face_image)

            # Compare the captured face encoding with stored encodings in the database
            for profile in Profile.objects.all():
                stored_encoding = pickle.loads(profile.face_encoding)  # Load stored face encoding
                match = face_recognition.compare_faces([stored_encoding], face_encoding)

                if match[0]:
                    # Recognized the face, mark attendance as Present
                    employee = Employee.objects.get(user=profile.user)
                    attendance = Attendance(
                        emp=employee, 
                        date=timezone.now().date(),
                        status="Present"
                    )
                    attendance.save()

                    recognized = True
                    # Add a message on the frame
                    cv2.putText(frame, "Attendance Marked", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    break  # Exit after recognizing the face

        if not recognized:
            # Add message if face is not recognized
            cv2.putText(frame, "Face not recognized", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Display the resulting frame with the message
        cv2.imshow("Check-in System", frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close any OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

    return JsonResponse({"message": "Check-in process completed"})


def attendance_list(request):
    # attendances = Attendance.objects.select_related('emp__user').order_by('-date')
    attendances = Attendance.objects.order_by('-date')
    return render(request, 'attendance/attendance_list.html', {'attendances': attendances})

import cv2
import face_recognition
import numpy as np
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Employee, Profile, Attendance
from django.utils import timezone
import pickle
import json

@csrf_exempt
def recognize_face(request):
    """Handle face recognition."""
    
    if request.method == 'POST':
        # Capture the frame from webcam
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()

        if not ret:
            return JsonResponse({'faceRecognized': False})

        rgb_frame = frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        recognized = False
        for face_encoding in face_encodings:
            for profile in Profile.objects.all():
                stored_encoding = pickle.loads(profile.face_encoding)  # Load stored face encoding
                match = face_recognition.compare_faces([stored_encoding], face_encoding)

                if match[0]:
                    recognized = True
                    break
        
        cap.release()

        # Return the status of face recognition
        return JsonResponse({'faceRecognized': recognized})

@csrf_exempt
def check_in(request):
    """Handle check-in after face recognition."""
    
    if request.method == 'POST':
        # Mark attendance as present
        # You can add logic to get the current user and mark the attendance
        # For simplicity, let's just simulate the check-in process:
        
        employee = Employee.objects.first()  # Assuming you get the employee object somehow
        attendance = Attendance(
            emp=employee, 
            date=timezone.now().date(),
            status="Present"
        )
        attendance.save()

        return JsonResponse({"message": "Check-in successful"})
    return JsonResponse({"error": "Invalid request"}, status=400)
