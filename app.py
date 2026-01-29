from flask import Flask, render_template, flash, redirect, url_for, session, request, Response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os
import time
import cv2
import numpy as np
import pyttsx3

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Enable CSRF protection
app.config['WTF_CSRF_ENABLED'] = True
# Session configuration
app.config['SESSION_PERMANENT'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutes
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    uname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    date = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    pass1 = db.Column(db.String(60), nullable=False)

# Authentication decorators
def login_required_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or 'user_type' not in session or session.get('user_type') != 'user':
            flash('Please login as a user to access this page.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def login_required_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or 'user_type' not in session or session.get('user_type') != 'admin':
            flash('Please login as an admin to access this page.', 'danger')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# admin database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)



# models.py
class Medical(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    uname = db.Column(db.String(255))  # Add this line
    address = db.Column(db.String(255))
    allergies = db.Column(db.String(255))
    visionstatus = db.Column(db.String(255))
    medications = db.Column(db.String(255))
    surgeries = db.Column(db.String(255))
    bloodgroup = db.Column(db.String(255))
    age = db.Column(db.String(255))
    chronic_conditions = db.Column(db.String(255))
    emergency_contact = db.Column(db.String(20))
    blood_pressure = db.Column(db.String(15))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        pass1 = request.form['pass1']
        
        try:
            user = Users.query.filter_by(email=email).first()
            if user and check_password_hash(user.pass1, pass1):
                flash('Login successful!', 'success')
                session['user_id'] = user.id
                session['user_type'] = 'user'
                return redirect(url_for('home'))
            else:
                flash('Login failed. Check your email and password.', 'danger')
        except Exception as e:
            flash('Login error. Please try again.', 'danger')
            
    return render_template('login.html')

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        uname = request.form['uname']
        lname = request.form['lname']
        email = request.form['email']
        date = request.form['date']
        address = request.form['address']
        phone = request.form['phone']
        pass1 = request.form['pass1']
        pass2 = request.form['pass2']

        if pass1 == pass2:
            try:
                # Check if user already exists
                existing_user = Users.query.filter(
                    (Users.email == email) | (Users.phone == phone) | (Users.username == username)
                ).first()
                
                if existing_user:
                    if existing_user.email == email:
                        flash('Email already registered. Please use a different email.', 'danger')
                    elif existing_user.phone == phone:
                        flash('Phone number already registered. Please use a different phone number.', 'danger')
                    else:
                        flash('Username already taken. Please choose a different username.', 'danger')
                    return render_template('user_registration.html')
                
                hashed_password = generate_password_hash(pass1)
                new_user = Users(username=username,uname=uname,lname=lname, email=email,date=date,address=address,phone=phone, pass1=hashed_password)
                db.session.add(new_user)
                db.session.commit()
                flash('Registration successful! You can now log in.', 'success')
                return redirect(url_for('login'))
                
            except Exception as e:
                db.session.rollback()
                flash('Registration failed. Please try again.', 'danger')
                return render_template('user_registration.html')
        else:
            flash('Passwords do not match.', 'danger')

    return render_template('user_registration.html')

@app.route('/logout/')
def logout():
    session.clear()  # Clear all session data
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('base'))

@app.route('/admin_logout/')
def admin_logout():
    session.clear()  # Clear all session data
    flash('Admin logged out successfully.', 'info')
    return redirect(url_for('base'))




@app.route('/users/edit/<int:id>', methods=['GET', 'POST'])
@login_required_admin
def edit_user(id):
    try:
        user = Users.query.get_or_404(id)
        if request.method == 'POST':
            # Check for duplicates
            existing_user = Users.query.filter(
                (Users.email == request.form['email']) & (Users.id != id) |
                (Users.phone == request.form['phone']) & (Users.id != id) |
                (Users.username == request.form['username']) & (Users.id != id)
            ).first()
            
            if existing_user:
                if existing_user.email == request.form['email']:
                    flash('Email already exists.', 'danger')
                elif existing_user.phone == request.form['phone']:
                    flash('Phone number already exists.', 'danger')
                else:
                    flash('Username already exists.', 'danger')
                return render_template('edit_user.html', user=user)
            
            # Update user
            user.username = request.form['username']
            user.uname = request.form['uname']
            user.lname = request.form['lname']
            user.email = request.form['email']
            user.date = request.form['date']
            user.address = request.form['address']
            user.phone = request.form['phone']
            if request.form.get('pass1'):  # Only update password if provided
                user.pass1 = generate_password_hash(request.form['pass1'])

            db.session.commit()
            flash('User updated successfully', 'success')
            return redirect(url_for('view_user'))
        else:
            return render_template('edit_user.html', user=user)
    except Exception as e:
        db.session.rollback()
        flash('Error updating user. Please try again.', 'danger')
        return redirect(url_for('view_user'))
    

@app.route('/users/delete/<int:id>', methods=['POST'])
@login_required_admin
def delete_user(id):
    try:
        user = Users.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting user. Please try again.', 'danger')
    return redirect(url_for('view_user'))









@app.route("/home",methods=['GET', 'POST'])
@login_required_user
def home():
    if request.method == 'POST':
        if request.form.get('start_detection') == 'Start Detection':
           return redirect(url_for('start'))
        elif request.form.get('Continue') == 'Continue':
           return render_template("test1.html")
    
    return render_template("home.html")



@app.route("/")
def base():
    return render_template("base.html")


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        try:
            user = User.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                flash('Login successful!', 'success')
                session['user_id'] = user.id
                session['user_type'] = 'admin'
                return redirect(url_for('admin_home'))
            else:
                flash('Login failed. Check your email and password.', 'danger')
        except Exception as e:
            flash('Login error. Please try again.', 'danger')
            
    return render_template('admin_login.html')

@app.route("/admin_home")
@login_required_admin
def admin_home():
    return render_template("admin_home.html")


@app.route('/medical_info/', methods=['GET', 'POST'])
@login_required_user
def medical_info():
    if request.method == 'POST':
        try:
            uname = request.form['uname']
            address = request.form['address']
            allergies = request.form['allergies']
            visionstatus = request.form['visionstatus']
            medications = request.form['medications']
            surgeries = request.form['surgeries']
            bloodgroup = request.form['bloodgroup']
            age = request.form['age']
            chronic_conditions = request.form['chronic_conditions']
            emergency_contact = request.form['emergency_contact']
            blood_pressure = request.form['blood_pressure']

            # Get the user ID from the session
            user_id = session.get('user_id')

            # Check if the user is logged in
            if not user_id:
                flash('Please login to add medical information.', 'danger')
                return redirect(url_for('login'))

            # Create a Medical instance
            medical_info = Medical(
                user_id=user_id,
                uname=uname,
                address=address,
                allergies=allergies,
                visionstatus=visionstatus,
                medications=medications,
                surgeries=surgeries,
                bloodgroup=bloodgroup,
                age=age,
                chronic_conditions=chronic_conditions,
                emergency_contact=emergency_contact,
                blood_pressure=blood_pressure
            )

            # Add and commit the medical_info to the database
            db.session.add(medical_info)
            db.session.commit()
            flash('Medical information added successfully!', 'success')
            return redirect(url_for('home'))

        except Exception as e:
            db.session.rollback()
            flash('Error adding medical information. Please try again.', 'danger')
            return render_template("add_medical.html")

    return render_template("add_medical.html")

@app.route("/database_viewer")
@login_required_admin
def database_viewer():
    try:
        # Get all users
        users = Users.query.all()
        
        # Get all medical records
        medical_records = Medical.query.all()
        
        # Get database statistics
        user_count = Users.query.count()
        medical_count = Medical.query.count()
        
        return render_template('database_viewer.html', 
                             users=users, 
                             medical_records=medical_records,
                             user_count=user_count,
                             medical_count=medical_count)
    except Exception as e:
        flash('Error accessing database viewer. Please try again.', 'danger')
        return redirect(url_for('admin_home'))

@app.route("/users")
@login_required_admin
def users():
    try:
        users = Users.query.all()
        return render_template('view_user.html', users=users)
    except Exception as e:
        flash('Error loading users. Please try again.', 'danger')
        return redirect(url_for('admin_home'))

@app.route("/view_user")
@login_required_admin
def view_user():
    try:
        users = Users.query.all()
        return render_template('view_user.html', users=users)
    except Exception as e:
        flash('Error loading users. Please try again.', 'danger')
        return redirect(url_for('admin_home'))
    

@app.route("/view_medical")
@login_required_admin
def view_medical():
    try:
        user_medical_info = Medical.query.all()
        return render_template('view_medical.html', user_medical_info=user_medical_info)
    except Exception as e:
        flash('Error loading medical records. Please try again.', 'danger')
        return redirect(url_for('admin_home'))

@app.route('/update_medical/<int:id>', methods=['GET', 'POST'])
@login_required_admin
def update_medical(id):
    try:
        medical_info = Medical.query.get_or_404(id)

        if request.method == 'POST':
            # Update medical_info attributes based on the form data
            medical_info.allergies = request.form['allergies']
            medical_info.medications = request.form['medications']
            medical_info.visionstatus = request.form.get('visionstatus', medical_info.visionstatus)
            medical_info.surgeries = request.form.get('surgeries', medical_info.surgeries)
            medical_info.bloodgroup = request.form.get('bloodgroup', medical_info.bloodgroup)
            medical_info.age = request.form.get('age', medical_info.age)
            medical_info.chronic_conditions = request.form.get('chronic_conditions', medical_info.chronic_conditions)
            medical_info.emergency_contact = request.form.get('emergency_contact', medical_info.emergency_contact)
            medical_info.blood_pressure = request.form.get('blood_pressure', medical_info.blood_pressure)

            # Commit the changes to the database
            db.session.commit()
            flash('Medical information updated successfully', 'success')
            return redirect(url_for('view_medical'))

        return render_template('update_medical.html', medical_info=medical_info)
    except Exception as e:
        db.session.rollback()
        flash('Error updating medical information. Please try again.', 'danger')
        return redirect(url_for('view_medical'))



# Route for deleting medical information
@app.route('/delete_medical/<int:id>')
@login_required_admin
def delete_medical(id):
    try:
        medical_info = Medical.query.get_or_404(id)

        # Delete the medical_info from the database
        db.session.delete(medical_info)
        db.session.commit()
        flash('Medical information deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting medical information. Please try again.', 'danger')
    return redirect(url_for('view_medical'))



# detection code



import cv2
import numpy as np
import pyttsx3

# Global variables for camera and detection
camera = None
detection_active = False
voice_enabled = True

def generate_frames():
    global camera, detection_active, voice_enabled
    camera = cv2.VideoCapture(0)
    
    # Initialize text-to-speech engine
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Speed of speech
    
    # Load YOLO model
    net = cv2.dnn.readNetFromDarknet('yolov3.cfg', 'yolov3.weights')
    classes = []
    with open('coco.names', 'r') as f:
        classes = [line.strip() for line in f.readlines()]
    layer_names = net.getLayerNames()
    output_layers = net.getUnconnectedOutLayersNames()
    colors = np.random.uniform(0, 255, size=(len(classes), 3))
    
    FOCAL_LENGTH = 1000  # in pixels
    OBJECT_HEIGHT = 0.5  # in meters
    MIN_DISTANCE = 2  # in meters
    
    last_voice_time = 0
    voice_cooldown = 2  # seconds between voice alerts
    
    while detection_active and camera.isOpened():
        success, frame = camera.read()
        if not success:
            break
        
        # Perform object detection
        height, width, channels = frame.shape
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)
        
        # Process detections
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = center_x - w // 2
                    y = center_y - h // 2
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
        
        # Apply non-max suppression
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        
        # Draw bounding boxes and labels
        current_time = time.time()
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                color = colors[class_ids[i]]
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                
                # Calculate distance
                obj_height = h
                if obj_height > 0:
                    distance = (OBJECT_HEIGHT * FOCAL_LENGTH) / obj_height
                    distance = round(distance, 2)
                    
                    # Add label with distance
                    label_text = f"{label}: {distance}m"
                    if distance < MIN_DISTANCE:
                        label_text = f"WARNING: {label_text}"
                        cv2.putText(frame, label_text, (x, y - 10), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                        
                        # Voice warning for close objects
                        if current_time - last_voice_time > voice_cooldown and voice_enabled:
                            try:
                                engine.say(f"Warning! {label} too close at {distance} meters")
                                engine.runAndWait()
                                last_voice_time = current_time
                            except:
                                pass  # Ignore voice errors
                    else:
                        cv2.putText(frame, label_text, (x, y - 10), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                        
                        # Voice announcement for important objects (less frequent)
                        important_objects = ['person', 'car', 'bicycle', 'dog', 'cat']
                        if label in important_objects and current_time - last_voice_time > voice_cooldown * 2 and voice_enabled:
                            try:
                                engine.say(f"{label} detected at {distance} meters")
                                engine.runAndWait()
                                last_voice_time = current_time
                            except:
                                pass  # Ignore voice errors
        
        # Encode frame for streaming
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
    # Cleanup
    if camera is not None:
        camera.release()

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), 
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/toggle_voice')
@login_required_user
def toggle_voice():
    global voice_enabled
    voice_enabled = not voice_enabled
    return {'voice_enabled': voice_enabled}

@app.route('/stop_detection')
@login_required_user
def stop_detection():
    global detection_active, camera
    detection_active = False
    if camera is not None:
        camera.release()
        camera = None
    flash('Detection stopped successfully.', 'info')
    return redirect(url_for('home'))

@app.route("/start", methods=['GET', 'POST'])
@login_required_user
def start():
    global detection_active
    
    if request.method == 'POST':
        if request.form.get('Start') == 'Start':
            # Validate file existence
            if not os.path.exists('yolov3.cfg') or not os.path.exists('yolov3.weights') or not os.path.exists('coco.names'):
                flash('Required YOLO files not found. Please ensure yolov3.cfg, yolov3.weights, and coco.names are present.', 'danger')
                return render_template("start.html")
            
            # Start detection
            detection_active = True
            return render_template("detection.html")
    else:
        return render_template("start.html")




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
