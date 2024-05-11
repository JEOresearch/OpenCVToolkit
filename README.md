# OpenCVToolkit
A toolkit that allows you to test various OpenCV image processing functions in real time

Basic usage is shown here: https://youtu.be/9vVMupPmk1g

This tool allows you to learn about and experiment with different OpenCV functions. You can specify a path to a video in the code, or it will default to a Webcam feed if it doesn't find a video. 

A graphical user interface (GUI) is provided that allows you to select image processing operations (in the order you select them). Users can dynamically select various operations like thresholding, edge detection, and more, and adjust their parameters in real-time.

OpenCV Features
- Binary Thresholding
- Canny Edge Detection
- Gaussian Blur
- Grayscale Conversion
- Hough Line Transform
- Contour Detection
- Erosion

AND
** Dynamic Operation Ordering: Operations are applied in the order they are activated.
** Resizable Output: Video display automatically resizes to maintain the aspect ratio.

Setup and Requirements:

To run this application, you need Python installed on your system along with the following libraries:

- opencv-python: For image processing
- numpy: For numerical operations
- Pillow: For image handling in Tkinter
- tkinter: For the GUI

If necessary, install the required packages using pip:
- pip install opencv-python numpy Pillow

Download the script to your local machine.
- Update the video_path in the script to point to a valid video file on your system, or use the webcam by default.

Change the file path in the Python script for your own video.

Run the script:
python path_to_script.py

Using the Application
- Launch the Application: Run the script, and the GUI should open.
- Select Operations: Check the boxes next to each operation to enable them.
- Adjust Parameters: Use the sliders next to each operation to adjust its parameters.
- View Results: The main canvas displays the video with the applied operations.
- Order of Operations: The order in which operations are applied can be changed dynamically by toggling the operations off and back on in the desired order.

Quitting the Application
- Click the "Quit" button at the bottom of the control panel to close the application.
