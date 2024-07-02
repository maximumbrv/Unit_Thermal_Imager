import cv2
import time
from pygrabber.dshow_graph import FilterGraph

WAIT_KEY_DELAY = 10
CAMERA_FPS = 15
RESOLUTION = (321, 240)
VIDEO_FOLDER = "video"
IMAGE_FOLDER = "img"


class Uti260b:

    def __init__(self):
        self._camera = None
        self._camera_id = None

    def connect(self):
        success = False
        if self._camera is None:
            if self._camera_id is None:
                print("Camera not found")
            else:
                try:
                    self._camera = cv2.VideoCapture(self._camera_id)
                except cv2.error:
                    print(f"Couldn't connect to camera #{self._camera_id}")
                else:
                    success = True
        else:
            print(f"Camera #{self._camera_id} already opened")
            success = True
        return success

    def disconnect(self):
        if self._camera is None:
            rval = True
        else:
            rval = self._camera.release()
            self._camera = None
            self._camera_id = None
        return rval

    def preview(self):
        if self._camera is None:
            print("Preview unavailable, camera not connected")
            return False

        cv2.namedWindow("preview", flags=cv2.WINDOW_NORMAL)

        if self._camera.isOpened():
            rval, frame = self._camera.read()
        else:
            rval = False
            print("Couldn't read from camera")
        recording = False
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = None

        while rval:
            cv2.imshow("preview", frame)
            rval, frame = self._camera.read()
            key = cv2.waitKey(WAIT_KEY_DELAY)

            if key == 27:  # exit on ESC
                break

            if key in [ord('c'), ord('C'), ord('с'), ord('С')]:
                image_name = self._get_filename_from_time('.bmp', IMAGE_FOLDER)
                cv2.imwrite(image_name, frame)
                print('Image captured')

            if key in [ord('r'), ord('R'), ord('к'), ord('К')]:
                if not recording:
                    video_name = self._get_filename_from_time('.mp4', VIDEO_FOLDER)
                    writer = cv2.VideoWriter(video_name, fourcc, CAMERA_FPS, RESOLUTION[::-1])
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

    def snap(self):
        if self.is_connected():
            status, frame = self._camera.read()
            if not status:
                return None
            else:
                return frame
        else:
            return None

    def find_camera(self):
        camera_found = False
        available_cameras = self._get_available_cameras()

        for index, name in available_cameras.items():
            if name == "UVC Camera":
                camera = cv2.VideoCapture(index)
                if camera.isOpened():
                    status, frame = camera.read()
                    if status and frame.shape[:2] == RESOLUTION:
                        camera_found = True
                        self._camera_id = index
                    camera.release()

        if camera_found:
            return True
        return False

    def is_found(self):
        return self._camera_id is not None

    def is_connected(self):
        return self._camera is not None

    @staticmethod
    def _get_available_cameras():
        devices = FilterGraph().get_input_devices()
        available_cameras = {}
        for index, name in enumerate(devices):
            available_cameras[index] = name
        return available_cameras

    @staticmethod
    def _get_filename_from_time(extension, folder=""):
        current_time = time.strftime("%d%m%Y-%H%M%S")
        file_name = folder + "\\" + current_time + extension
        return file_name


if __name__ == "__main__":
    cam = Uti260b()
    cam.find_camera()
    cam.connect()
    if cam.is_connected():
        cam.preview()
    cam.disconnect()