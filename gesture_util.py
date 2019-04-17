import util
import cv2


def draw_heart_single(image):
    like = cv2.imread('images/filter/like.png', cv2.IMREAD_UNCHANGED)
    heart = cv2.imread('images/filter/heart2.png', cv2.IMREAD_UNCHANGED)
    heart = cv2.flip(heart, 1)
    image = util.overlay_transparent(image, heart, 300, 100, overlay_size=(like.shape[0], like.shape[1]))
    image = util.overlay_transparent(image, like, 250, 120, overlay_size=(like.shape[0], like.shape[1]))
    image = util.overlay_transparent(image, like, 200, 100, overlay_size=(like.shape[0], like.shape[1]))
    image = util.overlay_transparent(image, like, 150, 120, overlay_size=(like.shape[0], like.shape[1]))
    image = util.overlay_transparent(image, like, 100, 100, overlay_size=(like.shape[0], like.shape[1]))

    return image


def draw_firework(image):
    ok = cv2.imread('images/filter/ok.png', cv2.IMREAD_UNCHANGED)
    ok = cv2.flip(ok, 1)
    firework2 = cv2.imread('images/filter/fireworks2.png', cv2.IMREAD_UNCHANGED)
    firework3 = cv2.imread('images/filter/fireworks3.png', cv2.IMREAD_UNCHANGED)
    firework5 = cv2.imread('images/filter/fireworks5.png', cv2.IMREAD_UNCHANGED)
    firework6 = cv2.imread('images/filter/fireworks6.png', cv2.IMREAD_UNCHANGED)
    height = int(firework2.shape[0]*0.67)
    width = int(firework2.shape[1]*0.67)
    image = util.overlay_transparent(image, ok, 350, 100, overlay_size=(height, width))
    image = util.overlay_transparent(image, firework2, 250, 120, overlay_size=(height, width))
    image = util.overlay_transparent(image, firework3, 200, 100, overlay_size=(height, width))
    image = util.overlay_transparent(image, firework6, 150, 120, overlay_size=(height, width))
    image = util.overlay_transparent(image, firework5, 100, 100, overlay_size=(height, width))

    return image


def draw_one(image):
    one = cv2.imread('images/filter/one.png', cv2.IMREAD_UNCHANGED)
    one = cv2.flip(one, 1)
    height = int(one.shape[0] * 0.67)
    width = int(one.shape[1] * 0.67)
    image = util.overlay_transparent(image, one, 500, 100, overlay_size=(height, width))
    return image


def draw_two(image):
    two = cv2.imread('images/filter/two.png', cv2.IMREAD_UNCHANGED)
    two = cv2.flip(two, 1)
    height = int(two.shape[0] * 0.67)
    width = int(two.shape[1] * 0.67)
    image = util.overlay_transparent(image, two, 400, 100, overlay_size=(height, width))
    return image


def draw_three(image):
    three = cv2.imread('images/filter/three.png', cv2.IMREAD_UNCHANGED)
    three = cv2.flip(three, 1)
    height = int(three.shape[0] * 0.67)
    width = int(three.shape[1] * 0.67)
    image = util.overlay_transparent(image, three, 300, 100, overlay_size=(height, width))
    return image


def draw_four(image):
    four = cv2.imread('images/filter/four.png', cv2.IMREAD_UNCHANGED)
    four = cv2.flip(four, 1)
    height = int(four.shape[0] * 0.67)
    width = int(four.shape[1] * 0.67)
    image = util.overlay_transparent(image, four, 200, 100, overlay_size=(height, width))
    return image


def draw_five(image):
    five = cv2.imread('images/filter/five.png', cv2.IMREAD_UNCHANGED)
    five = cv2.flip(five, 1)
    height = int(five.shape[0] * 0.67)
    width = int(five.shape[1] * 0.67)
    image = util.overlay_transparent(image, five, 100, 100, overlay_size=(height, width))
    return image


def draw_love(image):
    love1 = cv2.imread('images/filter/loveyou.png', cv2.IMREAD_UNCHANGED)
    love1 = cv2.flip(love1, 1)
    love2 = cv2.imread('images/filter/loveyou1.png', cv2.IMREAD_UNCHANGED)
    love2 = cv2.flip(love2, 1)
    love3 = cv2.imread('images/filter/loveyou2.png', cv2.IMREAD_UNCHANGED)
    love3 = cv2.flip(love3, 1)
    height = int(love1.shape[0] * 0.67)
    width = int(love1.shape[1] * 0.67)
    image = util.overlay_transparent(image, love1, 100, 100, overlay_size=(height, width))
    image = util.overlay_transparent(image, love2, 200, 100, overlay_size=(height, width))
    image = util.overlay_transparent(image, love3, 300, 100, overlay_size=(height, width))
    return image
