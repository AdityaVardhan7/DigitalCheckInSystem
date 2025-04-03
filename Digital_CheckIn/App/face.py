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
    face_array = detected_faces[0]['face']
    face_array = (face_array * 255).astype(np.uint8)  # Convert float (0-1) to uint8 (0-255)

    # Save and show the extracted face
    cv2.imwrite("extracted_face.jpg", cv2.cvtColor(face_array, cv2.COLOR_RGB2BGR))
    cv2.imshow("Extracted Face", face_array)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("No faces detected.")
