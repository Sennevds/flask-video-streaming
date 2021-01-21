import os
import cv2
from base_camera import BaseCamera


class Camera(BaseCamera):
    video_source = 0
    camera = None
    def __init__(self, led):
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            Camera.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
        super(Camera, self).__init__(led)

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def single_frame():
        if(Camera.camera is None):
            Camera.camera = cv2.VideoCapture(Camera.video_source)
        if not Camera.camera.isOpened():
            raise RuntimeError('Could not start camera.')
        _, img = Camera.camera.read()
        rotated=cv2.rotate(img, cv2.ROTATE_180)
        return cv2.imencode('.jpg', rotated)[1].tobytes()

    @staticmethod
    def frames():
        if(Camera.camera is None):
            Camera.camera = cv2.VideoCapture(Camera.video_source)
        if not Camera.camera.isOpened():
            raise RuntimeError('Could not start camera.')

        while True:
            # read current frame
            _, img = Camera.camera.read()
            rotated=cv2.rotate(img, cv2.ROTATE_180)

            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', rotated)[1].tobytes()
