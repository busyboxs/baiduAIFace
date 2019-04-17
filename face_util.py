import util
import cv2
import numpy as np


def draw_rotate_box(image, face_num, location):
    for i in range(face_num):
        loc = location[i]  # format: [[left, top, width, height, rotate], ...]
        # cv2.circle(detect_img, (loc[0], loc[1]), 1, (0, 255, 0), 2)
        loc[0], loc[1] = util.rotate_left_top_to_center_xy(*loc)
        bbox = ((loc[0], loc[1]), (loc[2], loc[3]), loc[4])  # format: ((center_x, center_y), (w, h), rotate)
        box = cv2.boxPoints(bbox)  # list of four point of box, (left_bottom, left_top, right_top, right_bottom)
        box = np.int0(box)
        cv2.drawContours(image, [box], 0, (255, 0, 255), 2)
        # cv2.circle(image, (loc[0], loc[1]), 1, (0, 255, 0), 2)
    return image


def wear_glasses(image, glasses, face_num, landmark4):
    for i in range(face_num):
        landmark = landmark4[i]
        lmk0 = np.array(landmark[0])  # right eye center
        lmk1 = np.array(landmark[1])  # left eye center
        # for j in range(len(landmark))[:2]:
        #     cv2.circle(image, (landmark[j][0], landmark[j][1]), 1, (0, 255, 0), 2)

        glasses_center = np.mean([lmk0, lmk1], axis=0)  # put glasses's center to this center
        glasses_size = np.linalg.norm(lmk0 - lmk1) * 2  # the width of glasses mask
        angle = -util.angle_between(lmk0, lmk1)

        glasses_h, glasses_w = glasses.shape[:2]
        glasses_c = (glasses_w / 2, glasses_h / 2)
        M = cv2.getRotationMatrix2D(glasses_c, angle, 1)
        cos = np.abs(M[0, 0])
        sin = np.abs(M[0, 1])

        # compute the new bounding dimensions of the image
        nW = int((glasses_h * sin) + (glasses_w * cos))
        nH = int((glasses_h * cos) + (glasses_w * sin))

        # adjust the rotation matrix to take into account translation
        M[0, 2] += (nW / 2) - glasses_c[0]
        M[1, 2] += (nH / 2) - glasses_c[1]

        rotated_glasses = cv2.warpAffine(glasses, M, (nW, nH))
        # cv2.imwrite("blog/images/rotate_glasses.png", rotated_glasses)
        try:
            image = util.overlay_transparent(image, rotated_glasses, glasses_center[0], glasses_center[1],
                                             overlay_size=(int(glasses_size),
                                                           int(rotated_glasses.shape[0] * glasses_size /
                                                               rotated_glasses.shape[1])))
        except:
            print('failed overlay image')
    return image


