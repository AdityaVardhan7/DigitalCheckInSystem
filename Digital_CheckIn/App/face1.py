import numpy as np
import cv2
from deepface import DeepFace

# Load the image and resize it (optional, depending on your image size)
image_path = "test_image.jpg"
image = cv2.imread(image_path)

# Resize image (optional step to improve speed)
image_resized = cv2.resize(image, (640, 480))  # Resize to a smaller resolution

# Use DeepFace to extract faces with a faster detector (like opencv)
detected_faces = DeepFace.extract_faces(image_resized, detector_backend="opencv")

# Check if faces are detected
if detected_faces:
    # Extract the first detected face
    face_data = detected_faces[0]
    face_array = face_data['face']  # This is the cropped face
    face_confidence = face_data['face_confidence']
    face_area = face_data['facial_area']  # {'x': 6, 'y': 5, 'w': 206, 'h': 206}

    # Display the detected face's area and confidence
    print(f"Facial Area: {face_area}")
    print(f"Face Confidence: {face_confidence}")

    # Check if confidence is above a threshold (e.g., 0.8) before extracting encoding
    if face_confidence > 0.8:
        # Save and show the extracted face
        face_array = (face_array * 255).astype(np.uint8)  # Convert float (0-1) to uint8 (0-255)
        cv2.imwrite("extracted_face.jpg", cv2.cvtColor(face_array, cv2.COLOR_RGB2BGR))
        cv2.imshow("Extracted Face", face_array)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Extract face encoding (embedding)
        face_encoding = DeepFace.represent(face_array, model_name="VGG-Face", enforce_detection=False)

        # Print the face encoding (embedding)
        print("Face Encoding (Embedding):", face_encoding)
    else:
        print("Face confidence is too low, skipping encoding extraction.")
else:
    print("No faces detected.")
