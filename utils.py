import cv2
import numpy as np

def show(img, title=""):
    cv2.imshow("", img)
    cv2.waitKey(0)

def imshow_hstack(image_a, image_b, title=""):
    image = np.hstack((image_a, image_b))
    show(image, title)