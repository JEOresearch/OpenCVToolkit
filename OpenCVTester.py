import cv2
import tkinter as tk
import numpy as np
from tkinter import ttk
from PIL import Image, ImageTk

class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        # Initialize an ordered list of operations
        self.active_operations = []
        
        # Specify the path to the video file
        video_path = "C:/Storage/Source Videos/cat2.mp4"  # Update this path as needed

        # Try to open the video file first
        self.vid = cv2.VideoCapture(video_path)
        if not self.vid.isOpened():  # If the video file fails to open
            print("Unable to open video file at", video_path, "- falling back to webcam.")
            self.vid = cv2.VideoCapture(video_source)  # Fallback to webcam
            if not self.vid.isOpened():
                raise ValueError("Unable to open video source", video_source)

        # Determine the aspect ratio and size for the canvas
        if self.vid.isOpened():
            # Obtain the default width and height from the video source
            original_width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
            original_height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
            new_width = 840
            aspect_ratio = original_width / original_height
            new_height = int(new_width / aspect_ratio)

        # Frame for the video feed
        self.video_frame = tk.Frame(window)
        self.video_frame.pack(side=tk.TOP, fill=tk.X)  # Changed to top and fill X for width adjustment

        # Canvas for displaying video, now dynamically sized
        self.canvas = tk.Canvas(self.video_frame, width=new_width, height=new_height)
        self.canvas.pack()

        # Frame for controls
        self.controls_frame = tk.Frame(window)
        self.controls_frame.pack(side=tk.TOP, fill=tk.X)  # Changed to top and fill X for horizontal layout


        # Operations and their parameters
        self.operations = {
            'Binary Thresholding': [('thresh', 0, 255, 125), ('maxValue', 1, 255, 125)],
            'Canny Edge Detection': [('threshold1', 0, 255, 125), ('threshold2', 0, 255, 125)],
            'Gaussian Blur': [('kernel size', 1, 31, 15)],
            'Grayscale Conversion': [],
            'Hough Line Transform': [('rho', 1, 10, 5), ('theta', 1, 180, 1), ('threshold', 1, 200, 100), ('minLineLength', 10, 100, 15), ('maxLineGap', 1, 50, 5)],
            'Contour Detection': [],
            'Erosion': [('kernel size', 1, 31, 15)],
            'Dilation': [('kernel size', 1, 31, 15)] 
        }
        self.operation_states = {}

        # Create controls for each operation
        for operation, params in self.operations.items():
            op_frame = tk.Frame(self.controls_frame)
            op_frame.pack(fill=tk.X, padx=5, pady=5)

            # Checkbox to enable/disable the operation
            var = tk.BooleanVar()
            chk = tk.Checkbutton(op_frame, text=operation, var=var, command=lambda op=operation, v=var: self.update_active_operations(op, v))
            chk.pack(side=tk.LEFT)
            self.operation_states[operation] = (var, {})

            # Sliders for parameters
            for param in params:
                param_name, min_val, max_val, default_val = param
                label = tk.Label(op_frame, text=param_name)
                label.pack(side=tk.LEFT)
                slider = ttk.Scale(op_frame, from_=min_val, to=max_val, orient=tk.HORIZONTAL)
                slider.set(default_val)  # Set slider to the default value
                slider.pack(side=tk.LEFT)
                self.operation_states[operation][1][param_name] = slider

        # Quit button
        self.btn_quit = ttk.Button(self.controls_frame, text="Quit", command=self.window.destroy)
        self.btn_quit.pack(side=tk.BOTTOM)

        # Start video stream
        self.delay = 15
        self.update()

        self.window.mainloop()

    def update_active_operations(self, operation, var):
        if var.get():
            if operation not in self.active_operations:
                self.active_operations.append(operation)
        else:
            if operation in self.active_operations:
                self.active_operations.remove(operation)


    def update(self):
        ret, frame = self.vid.read()
        if ret:
            # Resize the frame to maintain aspect ratio
            original_height, original_width = frame.shape[:2]
            new_width = 840
            aspect_ratio = original_width / original_height
            new_height = int(new_width / aspect_ratio)

            # Resize the frame
            frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)

            # Apply operations in the order they were activated
            for operation in self.active_operations:
                state, params = self.operation_states[operation]
                if state.get():  # Check if the operation is enabled
                    if operation == 'Binary Thresholding':
                        thresh = params['thresh'].get()
                        maxValue = params['maxValue'].get()
                        _, frame = cv2.threshold(frame, thresh, maxValue, cv2.THRESH_BINARY)
                    elif operation == 'Canny Edge Detection':
                        threshold1 = params['threshold1'].get()
                        threshold2 = params['threshold2'].get()
                        frame = cv2.Canny(frame, threshold1, threshold2)
                        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)  # Convert back to BGR for uniformity in display
                    elif operation == 'Gaussian Blur':
                        kernel_size = int(params['kernel size'].get())
                        # Ensure the kernel size is odd
                        if kernel_size % 2 == 0:
                            kernel_size += 1
                        frame = cv2.GaussianBlur(frame, (kernel_size, kernel_size), 0)
                    elif operation == 'Grayscale Conversion':
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)  # Convert back to BGR for consistent display
                    elif operation == 'Hough Line Transform':
                        rho = params['rho'].get()
                        theta = np.deg2rad(params['theta'].get())  # Convert degrees to radians
                        threshold = int(params['threshold'].get())
                        minLineLength = int(params['minLineLength'].get())  # Assuming these params exist
                        maxLineGap = int(params['maxLineGap'].get())  # Assuming these params exist
                        edges = cv2.Canny(frame, 50, 150)  # First apply edge detection
                        lines = cv2.HoughLinesP(edges, rho, theta, threshold, None, minLineLength, maxLineGap)
                        if lines is not None:
                            for line in lines:
                                x1, y1, x2, y2 = line[0]
                                cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    elif operation == 'Contour Detection':
                        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                        cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)
                    elif operation == 'Erosion':
                        kernel_size = int(params['kernel size'].get())
                        if kernel_size % 2 == 0:
                            kernel_size += 1  # Make sure the kernel size is odd
                        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
                        frame = cv2.erode(frame, kernel, iterations=1)
                    elif operation == 'Dilation':
                        kernel_size = int(params['kernel size'].get())
                        if kernel_size % 2 == 0:
                            kernel_size += 1  # Ensure the kernel size is odd
                        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
                        frame = cv2.dilate(frame, kernel, iterations=1)

               
                                
            if len(frame.shape) == 2:  # This means the image is grayscale
                frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

            # Convert frame to display format and show in the canvas
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        else:
            # If the frame could not be read, reset the video to the start
            self.vid.set(cv2.CAP_PROP_POS_FRAMES, 0)
            return self.update()  # Immediately try to update again

        self.window.after(self.delay, self.update)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

App(tk.Tk(), "OpenCV Testing Toolkit")
