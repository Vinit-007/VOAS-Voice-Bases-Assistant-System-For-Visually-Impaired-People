import cv2
import numpy as np
import os

def check_files_exist():
    """Check if required YOLO files exist"""
    required_files = ['yolov3.cfg', 'yolov3.weights', 'coco.names']
    missing_files = [file for file in required_files if not os.path.exists(file)]
    if missing_files:
        print(f"Error: Missing required files: {missing_files}")
        return False
    return True

def load_yolo_model():
    """Load YOLO model with error handling"""
    try:
        net = cv2.dnn.readNetFromDarknet('yolov3.cfg', 'yolov3.weights')
        classes = []
        with open('coco.names', 'r') as f:
            classes = [line.strip() for line in f.readlines()]
        layer_names = net.getLayerNames()
        output_layers = net.getUnconnectedOutLayersNames()
        colors = np.random.uniform(0, 255, size=(len(classes), 3))
        return net, classes, output_layers, colors
    except Exception as e:
        print(f"Error loading YOLO model: {e}")
        return None, None, None, None

if not check_files_exist():
    print("Please ensure yolov3.cfg, yolov3.weights, and coco.names are present in the current directory.")
    exit(1)

net, classes, output_layers, colors = load_yolo_model()

if net is None:
    print("Failed to load YOLO model. Exiting.")
    exit(1)

# Camera parameters
FOCAL_LENGTH = 1000  # in pixels
OBJECT_HEIGHT = 0.5  # in meters

try:
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Unable to access camera. Please check camera permissions.")
        exit(1)
    
    print("Object detection started. Press 'q' to quit.")
    
    while True:
        ret, img = cap.read()
        if not ret:
            print("Error: Unable to read from camera.")
            break
            
        height, width, channels = img.shape

        # Perform object detection
        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)

        # Process the detections
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = center_x - w // 2
                    y = center_y - h // 2
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        # Apply non-max suppression to eliminate duplicate detections
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        # Draw bounding boxes for each object detected
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                color = colors[class_ids[i]]
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                cv2.putText(img, label, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Display the resulting image
        cv2.imshow('Blind Assistance', img)

        if cv2.waitKey(1) == ord('q'):
            break

except KeyboardInterrupt:
    print("\nDetection stopped by user.")
except Exception as e:
    print(f"Error during object detection: {e}")
finally:
    # Release resources
    if 'cap' in locals():
        cap.release()
    cv2.destroyAllWindows()
    print("Resources released.")