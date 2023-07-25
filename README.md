# Hand Gesture Volume Control 

![Hand Gesture Volume Control Example](hand_gesture_volume_control.gif)

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Hand Gesture Volume Control is a Computer Vision project that allows you to control the system's audio volume using hand gestures detected from a webcam input. The project uses the [Mediapipe Hands](https://google.github.io/mediapipe/solutions/hands) solution to detect hand landmarks in real-time and calculates the distance between the thumb and index finger tips. This distance is then mapped to the system's volume range to control the volume level based on specific hand gestures.

## Features

- Real-time hand gesture recognition for volume control
- Webcam feed with hand landmarks and volume control bar display
- Audio volume control using hand gestures
- Hand gesture feedback on successful volume control

## Requirements

To run this project, you need the following dependencies:

- Python (>= 3.6)
- OpenCV (cv2)
- Mediapipe
- NumPy
- Pycaw

## Installation

1. Clone the repository to your local machine:

```bash
git clone https://github.com/TLILIFIRAS/Hand-Gesture-Volume-Control.git
cd hand-gesture-volume-control
```

2. Install the required dependencies using 'pip' :
   
   pip install opencv-python mediapipe numpy pycaw

# Usage

**Make sure you have a webcam connected to your computer.**

1. Run the `hand_gesture_volume_control.py` script:

    ```bash
    python hand_gesture_volume_control.py
    ```

The script will open a window showing the webcam feed with hand landmarks and a volume control bar.

2. Perform the following hand gestures to control the volume:

   - Pinch your thumb and index finger together to decrease the volume.
   - Stretch your thumb and index finger apart to increase the volume.

As you perform the gestures, the volume will change accordingly, and the volume control bar will reflect the changes.

Release the gestures to set the desired volume level.

## How It Works

The project uses the Mediapipe Hands solution to detect hand landmarks in the webcam feed. The distance between the thumb and index finger tips is calculated using the `math.hypot()` function. The calculated distance is then mapped to the system's volume range using `np.interp()` to control the volume level. The `pycaw` library is used to interact with the system's audio volume interface and set the volume level.

## Contributing

Contributions to this project are welcome. If you find any issues or have any suggestions for improvements, please feel free to open an issue or submit a pull request. Make sure to follow the existing code style and guidelines.

## License

This project is licensed under the MIT License. Feel free to use, modify, and distribute the code as per the terms of the license.

  


