import numpy as np
import cv2
import pytesseract
import time
from pygrabber.dshow_graph import FilterGraph

FRAME_DELAY = 10
VIDEO_FPS = 20
RESOLUTION = (321, 240)


class Uti260b:

    def __init__(self):
        self.camera = None
        self.camera_id = None

    def connect(self):
        success = False
        if self.camera is None:
            if self.camera_id is None:
                print("Camera not found")
            else:
                try:
                    self.camera = cv2.VideoCapture(self.camera_id)
                except cv2.error:
                    print(f"Couldn't connect to camera #{self.camera_id}")
                else:
                    success = True
        else:
            print(f"Camera #{self.camera_id} already opened")
            success = True
        return success

    def disconnect(self):
        if self.camera is None:
            rval = True
        else:
            rval = self.camera.release()
        return rval

    def preview(self):
        if self.camera is None:
            print("Preview unavailable, camera not connected")
            return False

        cv2.namedWindow("preview", flags=cv2.WINDOW_NORMAL)

        if self.camera.isOpened():
            rval, frame = self.camera.read()
        else:
            rval = False
            print("Couldn't read from camera")
        recording = False
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        writer = None

        while rval:
            cv2.imshow("preview", frame)
            rval, frame = self.camera.read()
            key = cv2.waitKey(FRAME_DELAY)
            if key == 27:  # exit on ESC
                break
            if key in [ord('c'), ord('C'), ord('с'), ord('С')]:
                current_time = time.strftime("%d%m%Y-%H%M%S")
                image_name = "img\\" + current_time + ".bmp"
                cv2.imwrite(image_name, frame)
                print('Image captured')
            if key in [ord('r'), ord('R'), ord('к'), ord('К')]:
                if not recording:
                    current_time = time.strftime("%d%m%Y-%H%M%S")
                    video_name = "video\\" + current_time + ".avi"
                    writer = cv2.VideoWriter(video_name, fourcc, VIDEO_FPS, RESOLUTION[::-1])
                    recording = True
                    print('Recording started')
                elif writer is None:
                    print('Recording not started')
                else:
                    recording = False
                    writer.release()
                    print('Recording stopped')

            if recording:
                writer.write(frame)

        cv2.destroyWindow("preview")

    def find_camera(self):
        camera_found = False
        available_cameras = self.get_available_cameras()

        for index, name in available_cameras.items():
            if name == "UVC Camera":
                camera = cv2.VideoCapture(index)
                if camera.isOpened():
                    status, frame = camera.read()
                    if status and frame.shape[:2] == RESOLUTION:
                        camera_found = True
                        self.camera_id = index
                    camera.release()

        if camera_found:
            return True
        return False

    def is_found(self):
        return self.camera_id is not None

    def is_connected(self):
        return self.camera is not None

    @staticmethod
    def get_available_cameras():
        devices = FilterGraph().get_input_devices()
        available_cameras = {}
        for index, name in enumerate(devices):
            available_cameras[index] = name
        return available_cameras


if __name__ == "__main__":
    cam = Uti260b()
    cam.find_camera()
    cam.connect()
    if cam.is_connected():
        cam.preview()
    cam.disconnect()