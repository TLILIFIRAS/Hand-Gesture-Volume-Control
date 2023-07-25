import cv2
import mediapipe as mp
import time

class HandDetector:
    def __init__(self, max_num_hands=2, min_detection_confidence=0.5):
        # Create mediapipe objects for hand detection
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=True, max_num_hands=max_num_hands,
                                        min_detection_confidence=min_detection_confidence)
        self.previous_time = 0

    def detect_hands(self, frame):
        # Convert the frame from BGR to RGB and flip it horizontally
        frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
        frame.flags.writeable = False

        # Process the frame using the hand detection model
        results = self.hands.process(frame)

        # Set the frame to be writable again
        frame.flags.writeable = True

        # Convert the frame back to BGR format
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Create an empty list to store the hand landmarks
        hand_landmarks_list = []
        myhand_landmarks=[]
        # If hand landmarks are detected, draw them on the frame and store in the list
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                height, width, _ = frame.shape
                self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                # Store the hand landmarks in the list
                hand_landmarks_list.append(hand_landmarks)


        # Print the positions of each hand landmark
        if hand_landmarks_list:
            for hand_landmarks in hand_landmarks_list:
                for idx, landmark in enumerate(hand_landmarks.landmark):
                    myhand_landmarks.append([idx,int(landmark.x * width),int(landmark.y * height)])
                    #print(f"Hand {hand_landmarks_list.index(hand_landmarks) + 1}, Landmark {idx}: "
                                 # f"{int(landmark.x * width)}, {int(landmark.y * height)}")

        # Calculate and display the FPS (Frames Per Second) on the frame
        current_time = time.time()
        fps = 1 / (current_time - self.previous_time)
        self.previous_time = current_time
        cv2.putText(frame, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 196, 255), 2)

        return frame, myhand_landmarks



    def run_hand_detection(self):
        cap = cv2.VideoCapture(0)

        while cap.isOpened():
            success, frame = cap.read()
            height, width, _ = frame.shape
            if not success:
                print("Empty Frame")
                continue

            # Detect hands in the current frame and get the hand landmarks list
            frame_with_hands, hand_landmarks_list = self.detect_hands(frame)

            # Display the frame with hand landmarks and FPS
            cv2.imshow('Hand Detection', frame_with_hands)

            # Exit the loop if 'q' is pressed
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        # Release the video capture and close the window
        cap.release()
        cv2.destroyAllWindows()


# Usage of the HandDetector class
if __name__ == "__main__":
    hand_detector = HandDetector()
    hand_detector.run_hand_detection()
