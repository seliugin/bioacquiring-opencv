import cv2
import dlib
import numpy as np
from itertools import product
from .normalize import Normalizer


class FaceRec():
    def __init__(self):
        self.frame_width = 640
        self.frame_height = 480

        self.normalizer = Normalizer()

        # opencv
        FACE_PROTO = "/home/pi/tmp/models/deploy.prototxt"
        FACE_MODEL = "/home/pi/tmp/models/res10_300x300_ssd_iter_140000_fp16.caffemodel"
        self.face_net = cv2.dnn.readNetFromCaffe(FACE_PROTO, FACE_MODEL)
        self.face_net.setPreferableTarget(cv2.dnn.DNN_TARGET_MYRIAD)

        # dlib
        predictor_path = "/home/pi/tmp/models/shape_predictor_68_face_landmarks.dat"
        face_rec_model_path = "/home/pi/tmp/models/dlib_face_recognition_resnet_model_v1.dat"

        # detector = dlib.get_frontal_face_detector()
        self.shape_predictor = dlib.shape_predictor(predictor_path)
        self.facerec = dlib.face_recognition_model_v1(face_rec_model_path)

    def get_faces(self, frame, confidence_threshold=0.5):
        """Returns the box coordinates of all detected faces"""
        # convert the frame into a blob to be ready for NN input
        blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104, 177.0, 123.0))

        self.face_net.setInput(blob)
        output = np.squeeze(self.face_net.forward())
        faces = []

        for i in range(output.shape[0]):
            confidence = output[i, 2]
            if confidence > confidence_threshold:
                box = output[i, 3:7] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])

                start_x, start_y, end_x, end_y = box.astype(np.int)

                start_x, start_y, end_x, end_y = start_x - \
                                                 10, start_y - 10, end_x + 10, end_y + 10
                start_x = 0 if start_x < 0 else start_x
                start_y = 0 if start_y < 0 else start_y
                end_x = 0 if end_x < 0 else end_x
                end_y = 0 if end_y < 0 else end_y

                faces.append((start_x, start_y, end_x, end_y))
        return faces

    @staticmethod
    def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
        dim = None
        (h, w) = image.shape[:2]
        if width is None and height is None:
            return image
        if width is None:
            r = height / float(h)
            dim = (int(w * r), height)
        else:
            r = width / float(w)
            dim = (width, int(h * r))
        return cv2.resize(image, dim, interpolation=inter)

    def get_bounding_boxes(self, frame):
        """Predict the age of the faces showing in the image"""
        if frame.shape[1] > self.frame_width:
            frame = image_resize(frame, width=self.frame_width)
        faces = self.get_faces(frame)
        return faces

    def _get_average_depth(self, depthmap, start_x, start_y, end_x, end_y):
        if end_x > self.frame_width or end_y > self.frame_height:
            return 0
        depths = []
        xs = np.arange(start_x, end_x)
        ys = np.arange(start_y, end_y)
        for x, y in product(xs, ys):
            depths.append(depthmap.get_distance(x, y))

        return np.mean(depths)

    def validate_image(self, frame, depthmap, bounding_boxes):
        """Validate image and return target bounding box"""

        if len(bounding_boxes) == 0:
            return False, (0, 0, 0, 0)

        areas = []
        depths = []
        for start_x, start_y, end_x, end_y in bounding_boxes:
            area = (end_x - start_x) * (end_y - start_y)
            areas.append(area)
            depth = self._get_average_depth(depthmap, start_x, start_y, end_x, end_y)
            depths.append(depth)

        target_index = np.argmin(depths)
        if areas[target_index] / (self.frame_width * self.frame_height) < 0.02:
            accept = False
        else:
            accept = True
        return accept, bounding_boxes[target_index]

    @staticmethod
    def _get_smoothed_point_distance(depthmap, point, margin):
        xs = np.arange(0, margin)
        ys = np.arange(0, margin)
        dists = []
        for dx, dy in product(xs, ys):
            x = point.x + dx
            y = point.y + dy
            dist = depthmap.get_distance(x, y)
            if dist != 0:
                dists.append(dist)

        print(dists)
        return np.mean(dists) if len(dists) > 0 else 0.

    def check_liveness(self, depthmap, shape, margin=5):

        dots = shape.parts()
        nose = dots[31]
        r_eye = dots[40]
        l_eye = dots[43]
        mouth = dots[63]
        nose_dist = self._get_smoothed_point_distance(depthmap, nose, margin)
        mouth_dist = self._get_smoothed_point_distance(depthmap, mouth, margin)
        r_eye_dist = self._get_smoothed_point_distance(depthmap, r_eye, margin)
        l_eye_dist = self._get_smoothed_point_distance(depthmap, l_eye, margin)

        if nose_dist == 0 or mouth_dist == 0:
            return False
        if nose_dist >= mouth_dist:
            return False
        else:
            return True

    def process_frame(self, frame, bounding_box):
        """Extract face descriptor and landmarks from image."""
        rect = dlib.rectangle(bounding_box[0], bounding_box[1], bounding_box[2], bounding_box[3])
        shape = self.shape_predictor(frame, rect)
        frame = self.normalizer.yuv_equalize(frame)
        face_descriptor = self.facerec.compute_face_descriptor(frame, shape)

        return face_descriptor, shape
