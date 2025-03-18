# import cv2
# import os
# import numpy as np
# from django.conf import settings
# from .models import Employee, Attendance
# from datetime import date

# # Load OpenCV's pre-trained face detector (Haar cascade)
# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# # Function to load employee images
# def load_employee_images():
#     employee_faces = {}
#     employees = Employee.objects.all()

#     for emp in employees:
#         if emp.user.profile.profile_image:
#             image_path = emp.user.profile.profile_image.path
#             if os.path.exists(image_path):  # Ensure file exists
#                 img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
#                 employee_faces[emp.user.username] = img
#                 print(f"Loaded image for {emp.user.username}")
#             else:
#                 print(f"Image not found for {emp.user.username}")

#     return employee_faces


# # Function to capture and recognize faces
# def recognize_faces():
#     employee_faces = load_employee_images()
    
#     cap = cv2.VideoCapture(0, cv2.CAP_MSMF) # Use DirectShow to fix webcam issues

    
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

#         for (x, y, w, h) in faces:
#             detected_face = gray[y:y+h, x:x+w]

#             # Compare detected face with stored employee images
#             for username, stored_face in employee_faces.items():
#                 try:
#                     # Resize detected face to match stored face
#                     detected_face_resized = cv2.resize(detected_face, (stored_face.shape[1], stored_face.shape[0]))

#                     # Compare using Mean Squared Error
#                     diff = np.sum((detected_face_resized - stored_face) ** 2)
#                     if diff < 5000000:  # Adjust this threshold based on testing
#                         emp = Employee.objects.get(user__username=username)

#                         # Mark attendance
#                         today = date.today()
#                         attendance, created = Attendance.objects.get_or_create(
#                             emp=emp, date=today, defaults={"status": "Present"}
#                         )

#                         if not created:
#                             attendance.status = "Present"
#                             attendance.save()

#                         print(f"Attendance marked for {username}")

#                         # Draw rectangle & show name
#                         cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
#                         cv2.putText(frame, username, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
#                 except Exception as e:
#                     print("Error processing face:", e)

#         cv2.imshow('Face Recognition Attendance', frame)

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()
