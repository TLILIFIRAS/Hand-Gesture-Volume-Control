# Import required libraries
import cv2
import numpy as np
import HandDetectionModule as HDM
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Pycaw Setup - Get the system's audio volume interface
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
volume_range = volume.GetVolumeRange()
min_volume = volume_range[0]
max_volume = volume_range[1]

# Set webcam window dimensions
window_width = 1280
window_height = 720

# Initialize the webcam
cap = cv2.VideoCapture(0)
cap.set(3, window_width)
cap.set(4, window_height)

# Initialize time variables for FPS calculation
cur_time = 0
prev_time = 0

# Create an instance of the HandDetector class
detector = HDM.HandDetector()

# Initialize volume variables
vol = 0
vol_bar = 400
vol_per = 0

while True:
    # Read frame from the webcam
    success, frame = cap.read()

    # Detect hands in the frame and get hand landmarks
    frame_with_hands, hand_landmarks = detector.detect_hands(frame)

    if len(hand_landmarks) != 0:
        # Get the positions of thumb and index finger landmarks
        x1, y1 = hand_landmarks[4][1], hand_landmarks[4][2]  # Thumb tip
        x2, y2 = hand_landmarks[8][1], hand_landmarks[8][2]  # Index finger tip

        # Calculate the center point between the thumb and index finger
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        # Draw circles at the thumb and index finger tips
        cv2.circle(frame_with_hands, (x1, y1), 13, (255, 0, 0), cv2.FILLED)
        cv2.circle(frame_with_hands, (x2, y2), 13, (255, 0, 0), cv2.FILLED)

        # Draw a line between the thumb and index finger tips
        cv2.line(frame_with_hands, (x1, y1), (x2, y2), (0, 255, 0), 3)

        # Draw a circle at the center between the thumb and index finger
        cv2.circle(frame_with_hands, (cx, cy), 13, (2, 0, 34), cv2.FILLED)

        # Calculate the length between the thumb and index finger tips
        length = math.hypot(x2 - x1, y2 - y1)

        # Map the length value to the volume range
        vol = np.interp(length, [30, 200], [min_volume, max_volume])
        vol_bar = np.interp(length, [30, 250], [400, 234])
        vol_per = np.interp(length, [30, 250], [0, 100])

        # Set the system volume to the mapped value
        volume.SetMasterVolumeLevel(vol, None)

        # Print the length and volume on the console
        print(int(length), vol)

        # Draw a circle at the center if the length is less than a threshold (gesture recognized)
        if length < 50:
            cv2.circle(frame_with_hands, (cx, cy), 13, (27, 125, 34), cv2.FILLED)

    # Draw the volume control bar and percentage on the frame
    cv2.rectangle(frame_with_hands, (123, 234), (200, 400), (179, 238, 17), 4)
    cv2.rectangle(frame_with_hands, (123, int(vol_bar)), (200, 400), (179, 238, 17), cv2.FILLED)
    cv2.putText(frame_with_hands, f'{int(vol_per)} %', (127, 450), cv2.FONT_HERSHEY_TRIPLEX, 1, (179, 238, 17), 3)

    # Display the frame with hand landmarks and volume control
    cv2.imshow('Camera ', frame_with_hands)

    # Check for the 'q' key press to exit the loop
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
