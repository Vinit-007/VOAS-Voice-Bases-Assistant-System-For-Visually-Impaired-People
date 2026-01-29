import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    
    # YOLO Configuration
    YOLO_CONFIG_PATH = os.environ.get('YOLO_CONFIG_PATH') or 'yolov3.cfg'
    YOLO_WEIGHTS_PATH = os.environ.get('YOLO_WEIGHTS_PATH') or 'yolov3.weights'
    YOLO_CLASSES_PATH = os.environ.get('YOLO_CLASSES_PATH') or 'coco.names'
    
    # Camera Configuration
    CAMERA_INDEX = int(os.environ.get('CAMERA_INDEX', 0))
    FOCAL_LENGTH = float(os.environ.get('FOCAL_LENGTH', 1000))
    OBJECT_HEIGHT = float(os.environ.get('OBJECT_HEIGHT', 0.5))
    MIN_DISTANCE = float(os.environ.get('MIN_DISTANCE', 2))
    
    # Detection Thresholds
    CONFIDENCE_THRESHOLD = float(os.environ.get('CONFIDENCE_THRESHOLD', 0.5))
    NMS_THRESHOLD = float(os.environ.get('NMS_THRESHOLD', 0.4))
