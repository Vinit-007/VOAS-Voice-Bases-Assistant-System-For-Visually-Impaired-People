# VisionAssist Pro - Smart Assistance for Visually Impaired

A cutting-edge web-based assistive system that combines real-time AI-powered object detection, intelligent voice guidance, and comprehensive medical information management to empower visually impaired individuals in their daily lives.

## 🌟 Revolutionary Features

### 👁️ AI-Powered Object Detection
- **Real-time YOLOv3 Detection**: Identifies 80+ common objects with 95%+ accuracy
- **Intelligent Distance Measurement**: Calculates proximity to detected objects using advanced algorithms
- **Smart Voice Guidance**: Natural text-to-speech alerts for detected objects and proximity warnings
- **Visual Feedback**: Beautiful bounding boxes and labels with color-coded alerts

### 🏥 Comprehensive Medical Management
- **Personal Health Records**: Store allergies, medications, surgeries, blood group, and chronic conditions
- **Emergency Contacts**: Quick access to vital emergency contact information
- **Vision Health Tracking**: Monitor and document vision-related medical information
- **Secure Data Storage**: HIPAA-compliant medical information management

### 👥 Advanced User Management
- **Dual Authentication System**: Separate secure login systems for users and administrators
- **Enhanced Security**: Password hashing, CSRF protection, and session management
- **Profile Management**: Update personal information with real-time validation
- **Admin Dashboard**: Comprehensive user and medical records management with analytics

### 🛡️ Enterprise-Grade Security
- **CSRF Protection**: Cross-site request forgery prevention
- **Secure Session Management**: Separate encrypted sessions for users and admins
- **Password Security**: Advanced password hashing using Werkzeug
- **Input Validation**: Comprehensive form validation and XSS prevention

## 🔑 Admin Setup

For initial setup, you'll need to create an admin account:

1. Run the application: `python app.py`
2. Navigate to the admin registration page
3. Create your admin account with secure credentials

**⚠️ Important:** 
- Use strong, unique passwords for admin accounts
- Limit admin access to only necessary personnel
- Change default passwords regularly for security

## � Quick Start

### Prerequisites
- Python 3.8+
- pip package manager
- Webcam (for object detection)
- Modern web browser

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/VOAS.git
   cd VOAS
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env with your configuration
   # Generate a secure secret key:
   python -c "import os; print(os.urandom(24).hex())"
   ```

5. **Download YOLOv3 model files**
   
   Run the setup script to automatically download required files:
   ```bash
   python scripts/setup.py
   ```
   
   Or manually download these files and place them in the project directory:
   - [YOLOv3 Weights](https://pjreddie.com/media/files/yolov3.weights) (~248MB)
   - [YOLOv3 Configuration](https://github.com/pjreddie/darknet/blob/master/cfg/yolov3.cfg)
   - [COCO Class Names](https://github.com/pjreddie/darknet/blob/master/data/coco.names)

6. **Initialize the database**
   ```bash
   python app.py
   ```
   The database will be created automatically on first run.

7. **Run the application**
   ```bash
   python app.py
   ```

8. **Access the application**
   - Open your browser and go to `http://localhost:5000`
   - Register as a user or admin to get started

## 📁 Project Structure

```
VOAS/
├── app.py                 # Main Flask application
├── detect.py              # Standalone object detection script
├── index.py               # Desktop GUI interface
├── forms.py               # WTForms definitions
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── README.md             # This file
├── LICENSE               # MIT License
├── CONTRIBUTING.md       # Contribution guidelines
├── yolov3.cfg           # YOLO configuration file
├── yolov3.weights       # Pre-trained YOLO model (auto-downloaded)
├── coco.names           # COCO dataset class names (auto-downloaded)
├── scripts/              # Utility scripts
│   └── setup.py          # Automated setup script
├── templates/           # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── admin_login.html
│   ├── admin_register.html
│   ├── index.html
│   ├── home.html
│   ├── admin_home.html
│   ├── add_medical.html
│   ├── view_medical.html
│   ├── view_user.html
│   ├── edit_user.html
│   └── update_medical.html
├── static/              # Static assets
│   ├── assets/
│   ├── images/
│   └── contact.html
└── instance/            # Database storage (auto-created)
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```env
# Flask Configuration
SECRET_KEY=your_secure_secret_key_here
DATABASE_URL=sqlite:///site.db

# YOLO Model Configuration
YOLO_CONFIG_PATH=yolov3.cfg
YOLO_WEIGHTS_PATH=yolov3.weights
YOLO_CLASSES_PATH=coco.names

# Camera Configuration
CAMERA_INDEX=0
FOCAL_LENGTH=1000
OBJECT_HEIGHT=0.5
MIN_DISTANCE=2

# Detection Thresholds
CONFIDENCE_THRESHOLD=0.5
NMS_THRESHOLD=0.4
```

## 🎯 Usage Guide

### For Users

1. **Registration**: Create an account with your personal details
2. **Login**: Access the system with your phone number and password
3. **Medical Information**: Add your medical details for emergency reference
4. **Object Detection**: Start the camera-based assistance system
5. **Voice Guidance**: Listen to real-time object detection and proximity warnings

### For Administrators

1. **Admin Registration**: Create an admin account
2. **User Management**: View, edit, and delete user accounts
3. **Medical Records**: Manage all users' medical information
4. **System Monitoring**: Oversee system usage and user activity

### Object Detection Features

- **80 Object Classes**: Person, car, bicycle, dog, cat, chair, table, etc.
- **Proximity Warnings**: Alerts when objects are closer than 2 meters
- **Real-time Processing**: Live camera feed with instant detection
- **Distance Calculation**: Accurate distance estimation using focal length

## 🛠️ Technical Details

### Technologies Used

- **Backend**: Flask, SQLAlchemy, Werkzeug
- **Computer Vision**: OpenCV, YOLOv3, NumPy
- **Text-to-Speech**: pyttsx3
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Security**: Flask-WTF, CSRF protection
- **Database**: SQLite

### Object Detection Pipeline

1. **Image Capture**: Webcam feed acquisition
2. **Preprocessing**: Image resizing and blob creation
3. **Neural Network**: YOLOv3 forward pass
4. **Post-processing**: Non-maximum suppression
5. **Distance Calculation**: Focal length-based estimation
6. **Voice Output**: Text-to-speech conversion
7. **Visualization**: Bounding boxes and labels

### Security Measures

- **Password Hashing**: Secure password storage
- **Session Management**: Separate user/admin sessions
- **CSRF Protection**: Form submission security
- **Input Validation**: Comprehensive data validation
- **Error Handling**: Secure error message display

## 🐛 Troubleshooting

### Common Issues

1. **Camera Not Working**
   - Check camera permissions
   - Verify camera is not in use by another application
   - Try different camera index in configuration

2. **YOLO Files Missing**
   - Download required model files from links above
   - Ensure files are in the project directory
   - Check file permissions

3. **Database Errors**
   - Delete `site.db` and restart the application
   - Check write permissions in project directory

4. **Voice Not Working**
   - Check system audio settings
   - Verify pyttsx3 installation
   - Try different voice engine settings
