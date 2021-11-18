import pyrealsense2.pyrealsense2 as rs
import numpy as np
import cv2
import pickle
import sys
from utils.data import encode_vec, decode_vec
import requests
from random import choice
from string import ascii_letters
from hashlib import md5
from random import randint

# sys.path.append('/home/pi/tmp')

from modules.facerec import FaceRec
from modules.streamhandler import StreamHandler

pipe = StreamHandler()
facerec = FaceRec()

accept = False


def get_frames(mode, request):
    processed = False
    sprocessed = False
    registered = False
    message = ''
    scredit = 15
    k = 0
    while True:


        # UI render frames
        color_image, depth_colormap = pipe.get_frame()
        cv2.putText(color_image, message, (20, 460), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 5)
        if sprocessed:
            cv2.putText(color_image, f"+{scredit} social credit!", (400, 30), cv2.FONT_HERSHEY_DUPLEX, 0.7,
                        (33, 143, 252), 2)


        bbs = facerec.get_bounding_boxes(color_image)
        accept, target_bb = facerec.validate_image(color_image, depth_colormap, bbs)

        # render_to_screen(color_image)
        # cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.rectangle(color_image, (target_bb[0], target_bb[1]), (target_bb[2], target_bb[3]), color=(0, 255, 0),
                      thickness=5)

        # Vitality check
        if not accept and not (registered or processed):
            cv2.putText(color_image, "Come Closer", (20, 460), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 5)
        elif not (registered or processed):
            cv2.putText(color_image, "Come a little bit closer and please wait", (20, 460), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 0), 5)
            face_descriptor, _ = facerec.process_frame(color_image, target_bb)
            fdesc = encode_vec(list(face_descriptor))

            if mode == 'registration' and not registered:
                fname = request.query['fname']
                lname = request.query['lname']
                tname = request.query['tname']
                bcard = request.query['bcard']
                phone = request.query['phone']

                namehash = md5((fname + lname + tname).encode()).hexdigest()
                bcard = md5(bcard.encode()).hexdigest()
                resp = requests.post('http://10.206.0.190:8080/register', json={'fdesc': fdesc,
                                                                               'namehash': namehash,
                                                                               'name': fname,
                                                                               'payment_token': bcard,
                                                                               'phone': phone}
                                    ).text
                if resp == 'ok':
                    print('ok')
                    registered = True
                    message = f"Successfully registered, {fname}"
                elif resp == 'already':
                    print('already')
                    message = "Already registered"
                    registered = True

            if mode == 'processing' and not processed:
                k += 1
                print(k)
                resp = requests.post('http://10.206.0.190:8080/process',
                                    json={'fdesc': fdesc}).text
                if resp[:2] == 'ok':
                    print('ok')
                    message = f'Successfully processed, {resp[2:]}!'
                    sprocessed = True
                    scredit = randint(10, 300)
                    cv2.putText(color_image, message, (20, 460), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 5)
                    processed = True
                elif k > 70:
                    print('not ok')
                    message = f'You are not registered'
                    cv2.putText(color_image, message, (20, 460), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 5)
                    processed = True

        imgencode = cv2.imencode('.jpg', color_image)[1]
        string_image = imgencode.tostring()


        yield (b'--frame\r\n'
               b'Content-Type: text/plain\r\n\r\n' + string_image + b'\r\n')
