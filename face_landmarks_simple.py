import cv2
import imutils
import base64
from math import atan2, degrees
from urllib.request import urlopen, Request
import json
import numpy as np


def pic_base64(image):
    with open(image, 'rb') as f:
        base64_data = base64.b64encode(f.read())
    return base64_data


def overlay_transparent(background_img, img_to_overlay_t, x, y, overlay_size=None):
    bg_img = background_img.copy()
    # convert 3 channels to 4 channels
    if bg_img.shape[2] == 3:
        bg_img = cv2.cvtColor(bg_img, cv2.COLOR_BGR2BGRA)

    if overlay_size is not None:
        img_to_overlay_t = cv2.resize(img_to_overlay_t.copy(), overlay_size)

    b, g, r, a = cv2.split(img_to_overlay_t)

    mask = cv2.medianBlur(a, 5)

    h, w, _ = img_to_overlay_t.shape
    roi = bg_img[int(y - h / 2):int(y + h / 2), int(x - w / 2):int(x + w / 2)]

    img1_bg = cv2.bitwise_and(roi.copy(), roi.copy(), mask=cv2.bitwise_not(mask))
    img2_fg = cv2.bitwise_and(img_to_overlay_t, img_to_overlay_t, mask=mask)

    bg_img[int(y - h / 2):int(y + h / 2), int(x - w / 2):int(x + w / 2)] = cv2.add(img1_bg, img2_fg)

    # convert 4 channels to 3 channels
    bg_img = cv2.cvtColor(bg_img, cv2.COLOR_BGRA2BGR)

    return bg_img


def angle_between(p1, p2):
    x_diff = p2[0] - p1[0]
    y_diff = p2[1] - p1[1]
    return degrees(atan2(y_diff, x_diff))


def get_face_info(image_base64, token_key):
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
    params_d = dict()
    params_d['image'] = str(image_base64, encoding='utf-8')
    params_d['image_type'] = 'BASE64'
    params_d['face_field'] = 'landmark'
    params_d['max_face_num'] = 10
    params = json.dumps(params_d).encode('utf-8')
    access_token = token_key
    request_url = request_url + "?access_token=" + access_token
    request = Request(url=request_url, data=params)
    request.add_header('Content-Type', 'application/json')
    response = urlopen(request)
    content = response.read()
    if content:
        data = json.loads(content)
        assert data['error_code'] == 0, data
        # pprint(data)
        return data['result']


def get_face_num(data):
    return data['face_num']


def get_landmark4(data):
    landmarks = list()
    face_num = get_face_num(data)
    for i in range(face_num):
        landmark = list()
        for j in range(4):
            x = data['face_list'][i]['landmark'][j]['x']
            y = data['face_list'][i]['landmark'][j]['y']
            landmark.append(list(map(int, (x, y))))
        landmarks.append(landmark)
    return landmarks


def wear_glasses(image, glasses, face_num, landmark4):
    for i in range(face_num):
        landmark = landmark4[i]
        lmk0 = np.array(landmark[0])  # right eye center
        lmk1 = np.array(landmark[1])  # left eye center
        # for j in range(len(landmark))[:2]:
        #     cv2.circle(image, (landmark[j][0], landmark[j][1]), 1, (0, 255, 0), 2)

        glasses_center = np.mean([lmk0, lmk1], axis=0)  # put glasses's center to this center
        glasses_size = np.linalg.norm(lmk0 - lmk1) * 2  # the width of glasses mask
        angle = -angle_between(lmk0, lmk1)

        rotated_glasses = imutils.rotate_bound(glasses, -angle)
        # cv2.imwrite("blog/images/rotate_glasses.png", rotated_glasses)
        try:
            image = overlay_transparent(image, rotated_glasses, glasses_center[0], glasses_center[1],
                                        overlay_size=(int(glasses_size),
                                                      int(rotated_glasses.shape[0] * glasses_size /
                                                          rotated_glasses.shape[1])))
        except:
            print('failed overlay image')
    return image


def main():
    token_key = '【获取的 token key】'

    image_name = 'images/faces/04.jpg'
    image = cv2.imread(image_name)

    glasses = cv2.imread('images/glasses/glasses6.png', cv2.IMREAD_UNCHANGED)

    image_base64 = pic_base64(image_name)
    face_data = get_face_info(image_base64, token_key)
    landmark4 = get_landmark4(face_data)
    face_num = get_face_num(face_data)
    image = wear_glasses(image, glasses, face_num, landmark4)
    cv2.imshow('glasses', image)
    cv2.waitKey()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
