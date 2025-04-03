import cv2

# Open the webcam
video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

ret, frame = video_capture.read()
if not ret:
    print("❌ ERROR: Camera not accessible. Try again!")
else:
    cv2.imshow("Captured Image", frame)  # Show the captured image
    cv2.imwrite("test_image.jpg", frame)  # Save it for debugging
    print("✅ Image saved as test_image.jpg. Check if it contains a clear face.")

cv2.waitKey(0)
cv2.destroyAllWindows()
video_capture.release()
