import cv2
import numpy as np
import tensorflow as tf
from tensorflow import keras
import os
from typing import Tuple

class EmotionDetector:
    """
    Emotion detection using CNN model for facial emotion recognition
    """
    
    def __init__(self):
        self.emotion_labels = ['angry', 'happy', 'neutral', 'sad', 'surprised', 'tired']
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.model = self._load_or_create_model()
        
    def _load_or_create_model(self):
        """Load pre-trained model or create a simple CNN model"""
        try:
            # Try to load existing model
            if os.path.exists('emotion_model.h5'):
                return keras.models.load_model('emotion_model.h5')
            else:
                return self._create_simple_model()
        except Exception as e:
            print(f"Error loading model: {e}")
            return self._create_simple_model()
    
    def _create_simple_model(self):
        """Create a simple CNN model for emotion detection"""
        model = keras.Sequential([
            keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(48, 48, 1)),
            keras.layers.MaxPooling2D((2, 2)),
            keras.layers.Conv2D(64, (3, 3), activation='relu'),
            keras.layers.MaxPooling2D((2, 2)),
            keras.layers.Conv2D(128, (3, 3), activation='relu'),
            keras.layers.MaxPooling2D((2, 2)),
            keras.layers.Flatten(),
            keras.layers.Dense(128, activation='relu'),
            keras.layers.Dropout(0.5),
            keras.layers.Dense(len(self.emotion_labels), activation='softmax')
        ])
        
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def detect_emotion(self, frame) -> Tuple[str, float]:
        """
        Detect emotion from a video frame
        
        Args:
            frame: OpenCV frame (BGR format)
            
        Returns:
            Tuple of (emotion_label, confidence_score)
        """
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
            if len(faces) == 0:
                return "neutral", 0.0
            
            # Use the largest face detected
            largest_face = max(faces, key=lambda x: x[2] * x[3])
            x, y, w, h = largest_face
            
            # Extract face region
            face_roi = gray[y:y+h, x:x+w]
            
            # Preprocess for model
            face_resized = cv2.resize(face_roi, (48, 48))
            face_normalized = face_resized / 255.0
            face_input = np.expand_dims(face_normalized, axis=0)
            face_input = np.expand_dims(face_input, axis=-1)
            
            # Predict emotion
            predictions = self.model.predict(face_input, verbose=0)
            emotion_index = np.argmax(predictions[0])
            confidence = float(predictions[0][emotion_index])
            
            emotion_label = self.emotion_labels[emotion_index]
            
            return emotion_label, confidence
            
        except Exception as e:
            print(f"Error in emotion detection: {e}")
            return "neutral", 0.0
    
    def detect_faces_with_emotions(self, frame):
        """
        Detect all faces and their emotions in a frame
        
        Args:
            frame: OpenCV frame (BGR format)
            
        Returns:
            List of tuples: [(x, y, w, h, emotion, confidence), ...]
        """
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
            results = []
            
            for (x, y, w, h) in faces:
                # Extract and process face
                face_roi = gray[y:y+h, x:x+w]
                face_resized = cv2.resize(face_roi, (48, 48))
                face_normalized = face_resized / 255.0
                face_input = np.expand_dims(face_normalized, axis=0)
                face_input = np.expand_dims(face_input, axis=-1)
                
                # Predict emotion
                predictions = self.model.predict(face_input, verbose=0)
                emotion_index = np.argmax(predictions[0])
                confidence = float(predictions[0][emotion_index])
                emotion_label = self.emotion_labels[emotion_index]
                
                results.append((x, y, w, h, emotion_label, confidence))
            
            return results
            
        except Exception as e:
            print(f"Error in face detection: {e}")
            return []
    
    def draw_emotion_on_frame(self, frame, faces_emotions):
        """
        Draw emotion labels and bounding boxes on frame
        
        Args:
            frame: OpenCV frame
            faces_emotions: List from detect_faces_with_emotions()
            
        Returns:
            Frame with annotations
        """
        emotion_colors = {
            'happy': (34, 197, 94),    # Green
            'neutral': (156, 163, 175),  # Gray
            'sad': (59, 130, 246),     # Blue
            'angry': (248, 113, 113),  # Red
            'tired': (167, 139, 250),  # Purple
            'surprised': (245, 158, 11) # Orange
        }
        
        for (x, y, w, h, emotion, confidence) in faces_emotions:
            color = emotion_colors.get(emotion, (156, 163, 175))
            
            # Draw rectangle around face
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            
            # Draw emotion label
            label = f"{emotion}: {confidence:.2f}"
            label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            
            # Background for text
            cv2.rectangle(frame, (x, y-25), (x + label_size[0], y), color, -1)
            
            # Text
            cv2.putText(frame, label, (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        return frame
    
    def get_emotion_distribution(self, frame):
        """
        Get probability distribution of all emotions for the primary face
        
        Args:
            frame: OpenCV frame
            
        Returns:
            Dictionary mapping emotion labels to probabilities
        """
        try:
            emotion, _ = self.detect_emotion(frame)
            
            # For demo purposes, return the detected emotion with high confidence
            # In a real implementation, this would return the full prediction array
            emotion_dist = {label: 0.1 for label in self.emotion_labels}
            emotion_dist[emotion] = 0.8
            
            return emotion_dist
            
        except Exception as e:
            print(f"Error getting emotion distribution: {e}")
            return {label: 1.0/len(self.emotion_labels) for label in self.emotion_labels}
