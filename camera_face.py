# -*- coding: utf-8 -*-
import cv2
from util import get_face_info, get_face_location, frame2base64, get_hand_info
import util
import face_util
import gesture_util
import os
import random

token_key = '【获取的 token key】'
glasses_img = ['images/glasses/'+img for img in os.listdir('images/glasses')]

glasses = cv2.imread('images/glasses/glasses6.png', cv2.IMREAD_UNCHANGED)


cap = cv2.VideoCapture(0)
while True:
    _, image = cap.read()
    detect_img = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_base64 = frame2base64(image)
    face_data = get_face_info(image_base64, token_key)
    hand_data = get_hand_info(image_base64, token_key)
    _, cls_list = util.get_hand_cls_and_bbox(hand_data)
    if face_data:
        location = get_face_location(face_data)
        face_num = util.get_face_num(face_data)
        landmark4 = util.get_landmark4(face_data)
        if util.compare_hand(cls_list, 'Heart_single'):
            detect_img = gesture_util.draw_heart_single(detect_img)
        if util.compare_hand(cls_list, 'Ok'):
            detect_img = gesture_util.draw_firework(detect_img)
        if util.compare_hand(cls_list, 'One'):
            glasses = cv2.imread(glasses_img[1], cv2.IMREAD_UNCHANGED)
            detect_img = gesture_util.draw_one(detect_img)
        if util.compare_hand(cls_list, 'Two'):
            glasses = cv2.imread(glasses_img[2], cv2.IMREAD_UNCHANGED)
            detect_img = gesture_util.draw_two(detect_img)
        if util.compare_hand(cls_list, 'Three'):
            glasses = cv2.imread(glasses_img[3], cv2.IMREAD_UNCHANGED)
            detect_img = gesture_util.draw_three(detect_img)
        if util.compare_hand(cls_list, 'Four'):
            glasses = cv2.imread(glasses_img[4], cv2.IMREAD_UNCHANGED)
            detect_img = gesture_util.draw_four(detect_img)
        if util.compare_hand(cls_list, 'Five'):
            glasses = cv2.imread(glasses_img[5], cv2.IMREAD_UNCHANGED)
            detect_img = gesture_util.draw_five(detect_img)
        if util.compare_hand(cls_list, 'Fist'):
            glasses = cv2.imread(glasses_img[random.randint(0, len(glasses_img)-1)], cv2.IMREAD_UNCHANGED)
        if util.compare_hand(cls_list, 'ILY'):
            detect_img = gesture_util.draw_love(detect_img)

        detect_img = face_util.wear_glasses(detect_img, glasses, face_num, landmark4)
        detect_img = cv2.flip(detect_img, 1)
    else:
        detect_img = cv2.flip(detect_img, 1)
    # for i, cls in enumerate(cls_list):
    #     if cls != 'Face':
    #         cv2.putText(detect_img, cls, (50, 50 + 100 * i), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    cv2.imshow('pic', detect_img)
    key = cv2.waitKey(500) & 0xFF
    if key == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
