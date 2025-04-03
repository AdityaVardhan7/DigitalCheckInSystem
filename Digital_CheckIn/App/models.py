import face_recognition
from django.db import models
from django.contrib.auth.models import User
import numpy as np
import json
from django.utils.timezone import now



class Department(models.Model):
    dep_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    contact = models.CharField(max_length=15, blank=True, null=True)
    face_encoding = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username
    
    def get_image_path(self):
        """Returns full image path for face recognition"""
        if self.profile_image:
            return self.profile_image.path
        return None
    def set_encoding(self, encoding):
        """Convert numpy array to JSON string before saving."""
        self.face_encoding = json.dumps(encoding.tolist())

    def get_encoding(self):
        """Retrieve and convert JSON string back to numpy array."""
        return np.array(json.loads(self.face_encoding))
    
class Employee(models.Model):
    ROLE_CHOICES = [
        ("Admin", "Admin"),
        ("Staff", "Staff"),
        ("Employee", "Employee"),
    ]
    employee_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # FK to User model
    dep = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=[("Active", "Active"), ("Inactive", "Inactive")], null=True, blank=True
    )


    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.role}"
    
    def save(self, *args, **kwargs):
        """Ensure that if role is 'Admin', the user is a superuser and staff."""
        if self.role == "Admin":
            self.user.is_superuser = True
            self.user.is_staff = True
        else:
            self.user.is_superuser = False
            self.user.is_staff = False
        self.user.save()  # Save the related user object
        super().save(*args, **kwargs)


class Attendance(models.Model):
    attendance_id = models.AutoField(primary_key=True)
    emp = models.ForeignKey(Employee, on_delete=models.CASCADE)  # FK to Employee model
    date = models.DateField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[("Present", "Present"), ("Absent", "Absent")])

    def __str__(self):
        return f"{self.emp.user.username} - {self.date} - {self.status}"
    
STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

class Leaves(models.Model):
    
    leave_id = models.AutoField(primary_key=True)
    emp = models.ForeignKey(Employee, on_delete=models.CASCADE)  # FK to Employee model
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Leave Request by {self.emp.user.username} from {self.start_date} to {self.end_date}"


class Apology(models.Model):
    apology_id = models.AutoField(primary_key=True)
    emp = models.ForeignKey(Employee, on_delete=models.CASCADE)  # FK to Employee model
    date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Apology by {self.emp.user.username} on {self.date}"


class Report(models.Model):
    report_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # FK to User model
    date = models.DateField()

    def __str__(self):
        return f"Report by {self.user.username} on {self.date}"
