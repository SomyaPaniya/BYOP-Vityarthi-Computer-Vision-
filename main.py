import cv2
import winsound
import threading

# Load Haar cascaded classifiers
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

# Global flag to control the alarm thread
alarm_running = False

def play_alarm():
    """
    Function to play beep sound continuously while alarm is active.
    This runs in a separate thread so it doesn't block the webcam feed.
    """
    global alarm_running
    while alarm_running:
        # Beep at 1000 Hz for 500 milliseconds
        winsound.Beep(1000, 500)

def main():
    global alarm_running
    
    # Start video capture (0 is usually the built-in webcam)
    cap = cv2.VideoCapture(0)

    # Configure drowsiness detection parameters
    EYE_CLOSED_FRAMES_THRESHOLD = 15
    closed_frames_counter = 0

    print("Starting webcam feed... Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame. Exiting...")
            break
            
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces dynamically
        # parameters: image, scaleFactor, minNeighbors, minSize
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))
        
        status_text = "No Face Detected"
        text_color = (0, 0, 255) # Red default
        
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2) # Draw blue rectangle around face
            
            # Region of interest (ROI) for eyes is the upper half of the face 
            # to reduce false positives from nostrils/mouths
            roi_gray = gray[y:y+int(h/2), x:x+w]
            roi_color = frame[y:y+int(h/2), x:x+w]
            
            # Detect eyes in the face ROI
            eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=10, minSize=(15, 15))
            
            if len(eyes) == 0:
                # No eyes detected (treating this as eyes closed)
                closed_frames_counter += 1
                status_text = "Eyes Closed"
                text_color = (0, 165, 255) # Orange
            else:
                # Eyes are open! Reset counter
                closed_frames_counter = 0
                status_text = "Awake"
                text_color = (0, 255, 0) # Green
                
                # Visual feedback for eyes
                for (ex, ey, ew, eh) in eyes:
                    # Draw small circles around the eyes
                    cv2.circle(roi_color, (ex + ew//2, ey + eh//2), min(ew, eh)//2, (0, 255, 0), 2)
                    
        # Drowsiness alert logic
        if closed_frames_counter >= EYE_CLOSED_FRAMES_THRESHOLD:
            status_text = "DROWSINESS ALERT!!!"
            text_color = (0, 0, 255) # Red
            
            # Start alarm thread if not already running
            if not alarm_running:
                alarm_running = True
                threading.Thread(target=play_alarm, daemon=True).start()
        else:
            # Stop the alarm thread if the user is awake or no face is continuously detected over threshold
            alarm_running = False
            
        # Put status text on screen
        cv2.putText(frame, status_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 3)
        
        # Display the resulting frame
        cv2.imshow('Drowsiness Detection', frame)
        
        # Quit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    # Cleanup tasks
    alarm_running = False # Stop the alarm thread if it's running
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
    
