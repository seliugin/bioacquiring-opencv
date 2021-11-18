import pyrealsense2.pyrealsense2 as rs
import numpy as np
import cv2
import pickle
import sys

# sys.path.append('/home/pi/tmp')

from modules.facerec import FaceRec
from modules.streamhandler import StreamHandler

pipe = StreamHandler()
facerec = FaceRec()

accept = False


# def stream():
#     while True:
#         # UI render frames
#         color_image, depth_colormap = pipe.get_frame()
#
#
#         imgencode = cv2.imencode('.jpg', color_image)[1]
#         string_image = imgencode.tostring()
#         yield string_image
