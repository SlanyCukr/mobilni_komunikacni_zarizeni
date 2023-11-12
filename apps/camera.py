import customtkinter as ctk
import tkinter as tk
from picamera import PiCamera
from threading import Thread
import time

class CameraApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Camera App")
        self.attributes("-fullscreen", True)

        self.camera = PiCamera()  # Initialize camera
        self.is_recording = False

        self.setup_ui()

    def setup_ui(self):
        self.take_picture_button = ctk.CTkButton(self, text="Take Picture", command=self.take_picture)
        self.take_picture_button.pack(pady=20)

        self.record_video_button = ctk.CTkButton(self, text="Start Recording", command=self.toggle_video_recording)
        self.record_video_button.pack(pady=20)

    def take_picture(self):
        print("Taking picture...")
        # Implement the camera functionality here
        # Example: self.camera.capture('/path/to/image.jpg')

    def toggle_video_recording(self):
        if self.is_recording:
            print("Stopping recording...")
            self.record_video_button.set_text("Start Recording")
            # Implement stopping the video recording
            # Example: self.camera.stop_recording()
        else:
            print("Starting recording...")
            self.record_video_button.set_text("Stop Recording")
            # Implement starting the video recording
            # Example: self.camera.start_recording('/path/to/video.h264')
        self.is_recording = not self.is_recording

    def on_close(self):
        if self.is_recording:
            # Ensure the recording is stopped before closing
            # Example: self.camera.stop_recording()
        self.camera.close()  # Close the camera
        self.destroy()

if __name__ == "__main__":
    app = CameraApp()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()
