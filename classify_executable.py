#!/usr/bin/env python3
import sys
import os
import numpy as np
from tensorflow.keras.models import load_model
import json

def extract_file_features(file_path):
    """Extract features from file for classification"""
    try:
        with open(file_path, "rb") as f:
            file_bytes = f.read()
        
        # Extract basic features (you can modify this based on your model requirements)
        file_size = len(file_bytes)
        
        # Get first 1024 bytes for header analysis
        header_bytes = file_bytes[:1024] if len(file_bytes) >= 1024 else file_bytes + b"\x00" * (1024 - len(file_bytes))
        
        # Convert bytes to numerical features
        header_features = np.array([b for b in header_bytes], dtype=np.float32) / 255.0
        
        # Add file size as a feature (normalized)
        size_feature = min(file_size / (1024 * 1024), 1.0)  # Normalize to MB, cap at 1
        
        # Combine features
        features = np.concatenate([header_features, [size_feature]])
        
        # Reshape for model input (assuming model expects shape (1, 1025))
        features = features.reshape(1, -1)
        
        return features
    except Exception as e:
        return None

def classify_file(file_path, model_path):
    try:
        # Load the model
        model = load_model(model_path)
        
        # Extract features
        features = extract_file_features(file_path)
        if features is None:
            return {"error": "Failed to extract features"}
        
        # Make prediction
        prediction = model.predict(features, verbose=0)
        
        # Assuming binary classification where 1 = executable, 0 = not executable
        is_executable = bool(prediction[0][0] > 0.5)
        confidence = float(prediction[0][0])
        
        return {
            "is_executable": is_executable,
            "confidence": confidence,
            "error": None
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(json.dumps({"error": "Usage: python classify_executable.py <file_path> <model_path>"}))
        sys.exit(1)
    
    file_path = sys.argv[1]
    model_path = sys.argv[2]
    
    result = classify_file(file_path, model_path)
    print(json.dumps(result))
