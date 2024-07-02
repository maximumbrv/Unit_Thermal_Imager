import numpy as np
import cv2
import pytesseract
from pygrabber.dshow_graph import FilterGraph


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
            print(frame.shape)
        else:
            rval = False
            print("Couldn't read from camera")

        while rval:
            cv2.imshow("preview", frame)
            rval, frame = self.camera.read()
            key = cv2.waitKey(10)
            if key == 27:  # exit on ESC
                break

        cv2.destroyWindow("preview")

    def find_camera(self):
        camera_found = False
        available_cameras = self.get_available_cameras()

        for index, name in available_cameras.items():
            if name == "UVC Camera":
                print(f'check camera #{index}: {name}')
                camera = cv2.VideoCapture(index)
                if camera.isOpened():
                    status, frame = camera.read()
                    if status and frame.shape[:2] == (321, 240):
                        camera_found = True
                        self.camera_id = index
                    camera.release()

        if camera_found:
            return True
        return False

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
    cam.preview()
    cam.disconnect()