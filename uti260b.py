import numpy as np
import cv2
import pytesseract


class Uti260b:

    def __init__(self):
        self.camera = None
        self.camera_id = None

    def connect(self):
        success = False
        if self.camera is None:
            if self.camera_id is None:
                print("Camera not found")
            try:
                self.camera = cv2.VideoCapture(self.camera_id)
            except Exception:
                print(f"Couldn't connect to camera #{self.camera_id}")
            else:
                success = True
        else:
            print(f"Camera #{self.camera_id} already opened")
            success = True
        return success

    def disconnect(self):
        rval = self.camera.release()
        return rval

    def preview(self):
        if self.camera is None:
            print("Preview unavailable, camera not connected")
            return False

        cv2.namedWindow("preview", flags=cv2.WINDOW_NORMAL)

        if self.camera.isOpened():  # try to get the first frame
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
        id = 0
        camera_found = False
        while not camera_found and id < 20:
            camera = cv2.VideoCapture(id)
            if camera.isOpened():
                status, frame = camera.read()
                if status and frame.shape[:2] == (321, 240):
                    print(camera.get)
                    camera_found = True
                    self.camera_id = id
                camera.release()
            id += 1
        if camera_found:
            return True
        return False


if __name__ == "__main__":
    cam = Uti260b()
    cam.find_camera()
    cam.connect()
    cam.preview()
    cam.disconnect()