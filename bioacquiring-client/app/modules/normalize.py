import cv2
import numpy as np


class Normalizer():

    @staticmethod
    def face_rotation(img, shape):
        h, w, c = img.shape
        scale = 0.9
        face_land = shape.parts()
        left_eye_center = Normalizer._find_center_pt(face_land[36:41])
        right_eye_center = Normalizer._find_center_pt(face_land[42:47])
        nose_center = Normalizer._find_center_pt(face_land[27:35])
        trotate = Normalizer._get_rotation_matrix(left_eye_center, right_eye_center, nose_center, img, scale)
        warped = cv2.warpAffine(img, trotate, (w, h))
        return warped

    @staticmethod
    def _find_center_pt(points):
        x = 0
        y = 0
        num = len(points)
        for pt in points:
            x += pt.x
            y += pt.y
        x //= num
        y //= num
        return (x, y)

    @staticmethod
    def _angle_between_2_pt(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        tan_angle = (y2 - y1) / (x2 - x1)
        return (np.degrees(np.arctan(tan_angle)))

    @staticmethod
    def _get_rotation_matrix(left_eye_pt, right_eye_pt, nose_center, face_img, scale):
        eye_angle = Normalizer._angle_between_2_pt(left_eye_pt, right_eye_pt)
        M = cv2.getRotationMatrix2D((nose_center[0] / 2, nose_center[1] / 2), eye_angle, scale)
        return M

    @staticmethod
    def gray_equalize(image):
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.equalizeHist(gray_image)
        img_output = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)
        return img_output

    @staticmethod
    def yuv_equalize(image):
        image_yuv = cv2.cvtColor(image, cv2.COLOR_BGR2YUV);
        image_yuv[:, :, 0] = cv2.equalizeHist(image_yuv[:, :, 0])
        img_output = cv2.cvtColor(image_yuv, cv2.COLOR_YUV2BGR)
        return img_output

    @staticmethod
    def CLAHE(image, gridsize=25):
        bgr = image
        lab = cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB)
        lab_planes = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(gridsize, gridsize))
        lab_planes[0] = clahe.apply(lab_planes[0])
        lab = cv2.merge(lab_planes)
        bgr = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        return bgr
