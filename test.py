import cv2
import numpy as np
from PIL import Image

def test(img):
    # img = cv2.imread(file)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_bound = np.array([10, 20, 20])
    upper_bound = np.array([30, 255, 255])
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    kernel = np.ones((7, 7), np.uint8)

    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    segmented_img = cv2.bitwise_and(img, img, mask=mask)
    ratio = cv2.countNonZero(mask) / (img.size / 3)
    print(ratio)
    cv2.imshow("image", segmented_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    if np.round(ratio*100, 2) >= 20:
        return True
    else:
        return False
