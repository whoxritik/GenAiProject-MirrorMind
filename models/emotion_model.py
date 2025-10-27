import tensorflow as tf
from tensorflow import keras
import numpy as np
import os
import requests
import zipfile
from typing import Tuple, List, Optional

class EmotionModelBuilder:
    """
    Build and train CNN models for emotion recognition
    """
    
    def __init__(self):
        self.emotion_labels = ['angry', 'happy', 'neutral', 'sad', 'surprised', 'tired']
        self.input_shape = (48, 48, 1)  # Grayscale images
        
    def create_cnn_model(self, num_classes: int = 6) -> keras.Model:
        """
        Create a CNN model for emotion recognition
        
        Args:
            num_classes: Number of emotion classes
            
        Returns:
            Compiled Keras model
        """
        model = keras.Sequential([
            # First Convolutional Block
            keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=self.input_shape),
            keras.layers.BatchNormalization(),
            keras.layers.Conv2D(32, (3, 3), activation='relu'),
            keras.layers.MaxPooling2D((2, 2)),
            keras.layers.Dropout(0.25),
            
            # Second Convolutional Block
            keras.layers.Conv2D(64, (3, 3), activation='relu'),
            keras.layers.BatchNormalization(),
            keras.layers.Conv2D(64, (3, 3), activation='relu'),
            keras.layers.MaxPooling2D((2, 2)),
            keras.layers.Dropout(0.25),
            
            # Third Convolutional Block
            keras.layers.Conv2D(128, (3, 3), activation='relu'),
            keras.layers.BatchNormalization(),
            keras.layers.Conv2D(128, (3, 3), activation='relu'),
            keras.layers.MaxPooling2D((2, 2)),
            keras.layers.Dropout(0.25),
            
            # Fully Connected Layers
            keras.layers.Flatten(),
            keras.layers.Dense(512, activation='relu'),
            keras.layers.BatchNormalization(),
            keras.layers.Dropout(0.5),
            keras.layers.Dense(256, activation='relu'),
            keras.layers.Dropout(0.5),
            keras.layers.Dense(num_classes, activation='softmax')
        ])
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def create_lightweight_model(self, num_classes: int = 6) -> keras.Model:
        """
        Create a lightweight model for faster inference
        
        Args:
            num_classes: Number of emotion classes
            
        Returns:
            Compiled lightweight Keras model
        """
        model = keras.Sequential([
            keras.layers.Conv2D(16, (5, 5), activation='relu', input_shape=self.input_shape),
            keras.layers.MaxPooling2D((2, 2)),
            keras.layers.Conv2D(32, (3, 3), activation='relu'),
            keras.layers.MaxPooling2D((2, 2)),
            keras.layers.Conv2D(64, (3, 3), activation='relu'),
            keras.layers.MaxPooling2D((2, 2)),
            keras.layers.Flatten(),
            keras.layers.Dense(128, activation='relu'),
            keras.layers.Dropout(0.5),
            keras.layers.Dense(num_classes, activation='softmax')
        ])
        
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def preprocess_data(self, images: np.ndarray, labels: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Preprocess image data and labels for training
        
        Args:
            images: Raw image data
            labels: Emotion labels
            
        Returns:
            Preprocessed images and one-hot encoded labels
        """
        # Normalize pixel values
        images = images.astype('float32') / 255.0
        
        # Ensure proper shape
        if len(images.shape) == 3:
            images = np.expand_dims(images, axis=-1)
        
        # One-hot encode labels
        labels_onehot = keras.utils.to_categorical(labels, num_classes=len(self.emotion_labels))
        
        return images, labels_onehot
    
    def augment_data(self) -> keras.preprocessing.image.ImageDataGenerator:
        """
        Create data augmentation generator
        
        Returns:
            ImageDataGenerator with augmentation settings
        """
        return keras.preprocessing.image.ImageDataGenerator(
            rotation_range=10,
            width_shift_range=0.1,
            height_shift_range=0.1,
            shear_range=0.1,
            zoom_range=0.1,
            horizontal_flip=True,
            fill_mode='nearest'
        )
    
    def train_model(self, 
                   model: keras.Model,
                   train_images: np.ndarray,
                   train_labels: np.ndarray,
                   validation_data: Tuple[np.ndarray, np.ndarray] = None,
                   epochs: int = 50,
                   batch_size: int = 32,
                   use_augmentation: bool = True) -> keras.callbacks.History:
        """
        Train the emotion recognition model
        
        Args:
            model: Keras model to train
            train_images: Training images
            train_labels: Training labels
            validation_data: Optional validation data tuple
            epochs: Number of training epochs
            batch_size: Training batch size
            use_augmentation: Whether to use data augmentation
            
        Returns:
            Training history
        """
        # Setup callbacks
        callbacks = [
            keras.callbacks.EarlyStopping(
                monitor='val_loss' if validation_data else 'loss',
                patience=10,
                restore_best_weights=True
            ),
            keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss' if validation_data else 'loss',
                factor=0.5,
                patience=5,
                min_lr=1e-7
            ),
            keras.callbacks.ModelCheckpoint(
                'best_emotion_model.h5',
                monitor='val_accuracy' if validation_data else 'accuracy',
                save_best_only=True
            )
        ]
        
        # Train with or without augmentation
        if use_augmentation:
            datagen = self.augment_data()
            datagen.fit(train_images)
            
            history = model.fit(
                datagen.flow(train_images, train_labels, batch_size=batch_size),
                epochs=epochs,
                validation_data=validation_data,
                callbacks=callbacks,
                steps_per_epoch=len(train_images) // batch_size,
                verbose=1
            )
        else:
            history = model.fit(
                train_images, train_labels,
                batch_size=batch_size,
                epochs=epochs,
                validation_data=validation_data,
                callbacks=callbacks,
                verbose=1
            )
        
        return history
    
    def evaluate_model(self, model: keras.Model, test_images: np.ndarray, test_labels: np.ndarray) -> Dict:
        """
        Evaluate model performance
        
        Args:
            model: Trained model
            test_images: Test images
            test_labels: Test labels
            
        Returns:
            Dictionary with evaluation metrics
        """
        # Get predictions
        predictions = model.predict(test_images)
        predicted_classes = np.argmax(predictions, axis=1)
        true_classes = np.argmax(test_labels, axis=1)
        
        # Calculate metrics
        from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
        
        accuracy = accuracy_score(true_classes, predicted_classes)
        precision, recall, f1, _ = precision_recall_fscore_support(true_classes, predicted_classes, average='weighted')
        conf_matrix = confusion_matrix(true_classes, predicted_classes)
        
        # Per-class accuracy
        class_accuracies = {}
        for i, emotion in enumerate(self.emotion_labels):
            class_mask = (true_classes == i)
            if np.sum(class_mask) > 0:
                class_acc = accuracy_score(true_classes[class_mask], predicted_classes[class_mask])
                class_accuracies[emotion] = class_acc
        
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'confusion_matrix': conf_matrix,
            'class_accuracies': class_accuracies
        }
    
    def save_model(self, model: keras.Model, filename: str = 'emotion_model.h5'):
        """Save trained model to file"""
        model.save(filename)
        print(f"Model saved as {filename}")
    
    def load_model(self, filename: str = 'emotion_model.h5') -> Optional[keras.Model]:
        """Load saved model from file"""
        try:
            if os.path.exists(filename):
                return keras.models.load_model(filename)
            else:
                print(f"Model file {filename} not found")
                return None
        except Exception as e:
            print(f"Error loading model: {e}")
            return None
    
    def create_transfer_learning_model(self, base_model_name: str = 'MobileNetV2') -> keras.Model:
        """
        Create a model using transfer learning
        
        Args:
            base_model_name: Name of base model for transfer learning
            
        Returns:
            Transfer learning model
        """
        # Convert grayscale to RGB for pretrained models
        if base_model_name == 'MobileNetV2':
            base_model = keras.applications.MobileNetV2(
                input_shape=(48, 48, 3),
                alpha=1.0,
                include_top=False,
                weights='imagenet'
            )
        else:
            raise ValueError(f"Unsupported base model: {base_model_name}")
        
        # Freeze base model
        base_model.trainable = False
        
        # Add custom layers
        model = keras.Sequential([
            keras.layers.Lambda(lambda x: tf.repeat(x, 3, axis=-1), input_shape=self.input_shape),  # Convert grayscale to RGB
            keras.layers.Resizing(48, 48),
            base_model,
            keras.layers.GlobalAveragePooling2D(),
            keras.layers.Dropout(0.2),
            keras.layers.Dense(len(self.emotion_labels), activation='softmax')
        ])
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.0001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def download_pretrained_model(self, url: str, filename: str = 'emotion_model.h5') -> bool:
        """
        Download a pre-trained model from URL
        
        Args:
            url: URL to download model from
            filename: Local filename to save model
            
        Returns:
            True if successful, False otherwise
        """
        try:
            print(f"Downloading model from {url}...")
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"Model downloaded successfully as {filename}")
            return True
            
        except Exception as e:
            print(f"Error downloading model: {e}")
            return False
