from deepface import DeepFace
import numpy as np
import cv2

def extract_face_encoding(image_path):
    try:
        # Load the image
        image = cv2.imread(image_path)

        # Check if the image is successfully loaded
        if image is None:
            raise Exception(f"Unable to load image at {image_path}")

        # Use DeepFace to extract faces from the image
        detected_faces = DeepFace.extract_faces(image, detector_backend='opencv')

        # Ensure that at least one face is detected
        if detected_faces:
            # Extract the first detected face
            face_image = detected_faces[0]['face']
            
            # Use DeepFace to extract the face encoding (embedding)
            result = DeepFace.represent(face_image, model_name='VGG-Face', enforce_detection=False)

            # Ensure face encoding is extracted
            if result:
                # The result is a list of dictionaries, we access the 'embedding' field
                face_encoding = result[0]['embedding']

                # Convert the embedding to a numpy array
                face_encoding_array = np.array(face_encoding)

                return face_encoding_array
            else:
                raise Exception("Face encoding extraction failed")
        else:
            raise Exception("No face detected in the image")

    except Exception as e:
        raise Exception(f"Error during face recognition: {str(e)}")

# Example usage
image_path = "test_image.jpg"
face_encoding = extract_face_encoding(image_path)
print("Face encoding:", face_encoding)
