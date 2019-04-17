# -*- coding:utf-8 -*-
import urllib
from urllib.request import urlopen, Request
from urllib.parse import urlencode
import json
from pprint import pprint
import base64
from math import atan2, degrees
import cv2
import math
from PIL import Image
from io import BytesIO
import requests


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


def get_token_key():
    token_key = ''
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    client_id = '【百度云应用的AK】'  # API key
    client_secret = '【百度云应用的SK】'  # Secret key

    host = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials' \
        f'&client_id={client_id}&client_secret={client_secret}'

    request = Request(host)
    request.add_header('Content-Type', 'application/json; charset=UTF-8')
    response = urlopen(request)
    token_content = response.read()
    if token_content:
        token_info = json.loads(token_content)
        token_key = token_info['access_token']
    return token_key


def pic_base64(image):
    with open(image, 'rb') as f:
        base64_data = base64.b64encode(f.read())
    return base64_data


def frame2base64(frame):
    img = Image.fromarray(frame)
    output_buffer = BytesIO()
    img.save(output_buffer, format='JPEG')
    byte_data = output_buffer.getvalue()
    base64_data = base64.b64encode(byte_data)
    return base64_data


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
        # assert data['error_code'] == 0, data
        # pprint(data)
        return data['result']


def get_face_num(data):
    return data['face_num']


def get_face_list(data):
    return data['face_list']


def get_face_angle(data):
    """include pitch, roll and yaw"""
    return data['face_list'][0]['angle']


def get_face_shape(data):
    """include probability and type"""
    return data['face_list'][0]['face_shape']


def get_face_token(data):
    return data['face_list'][0]['face_token']


def get_face_location(data):
    """include height, left, rotation, top, width"""
    location = []
    face_num = get_face_num(data)
    for i in range(face_num):
        x = data['face_list'][i]['location']['left']
        y = data['face_list'][i]['location']['top']
        w = data['face_list'][i]['location']['width']
        h = data['face_list'][i]['location']['height']
        r = data['face_list'][i]['location']['rotation']
        location.append(list(map(int, (x, y, w, h, r))))
    return location


def rotate_left_top_to_center_xy(left, top, width, height, theta):
    center_x = left - 0.5 * height * math.sin(math.radians(theta)) + 0.5 * width * math.cos(math.radians(theta))
    center_y = top + 0.5 * height * math.cos(math.radians(theta)) + 0.5 * width * math.sin(math.radians(theta))
    return int(center_x), int(center_y)


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


def get_hand_info(image_base64, token_key):
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/gesture"
    params_d = dict()
    params_d['image'] = str(image_base64, encoding='utf-8')
    params = urlencode(params_d)
    access_token = token_key
    request_url = request_url + "?access_token=" + access_token
    res = requests.post(url=request_url,
                        data=params,
                        headers={'Content-Type': 'application/x-www-form-urlencoded'})
    data = res.json()
    return data


def get_hand_num(data):
    return data['result_num']


def get_hand_cls_and_bbox(data):
    result = list()
    cls_list = list()
    hand_num = get_hand_num(data)
    for i in range(hand_num):
        res_dict = data['result'][i]
        cls = res_dict['classname']
        cls_list.append(cls)
        bbox = [res_dict['left'], res_dict['top'], res_dict['width'], res_dict['height']]
        res = [cls] + bbox
        result.append(res)
    return result, cls_list


def compare_hand(cls_list, hand_cls):
    return hand_cls in cls_list


def main():
    pass


if __name__ == "__main__":
    main()
