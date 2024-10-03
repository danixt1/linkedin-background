import cv2
import numpy as np
from PIL import ImageGrab
import sys

def change_perspective(image, src_points, dst_points):
    M = cv2.getPerspectiveTransform(src_points, dst_points)
    transformed_image = cv2.warpPerspective(image, M, image.shape[1::-1])
    return transformed_image
def full_change_perspective(image,height_reduction):
    [x,y] = image.shape[0:2]
    reduction_pixels = int(image.shape[0] * (height_reduction / 100))
    src_points = np.float32([[0, 0], [y - 1, 0], [0, x - 1], [y - 1, x - 1]])
    dst_points = np.float32([[0, 0], [y - 1, reduction_pixels], [0, x - 1], [y - 1, x - 1 - reduction_pixels]])
    return change_perspective(image,src_points,dst_points)
len_args = len(sys.argv)

if(len_args < 5 and len_args > 1):
    raise Exception("Not Enough args")

bbox = None if len_args == 1 else tuple(map(int,sys.argv[1:5]))

image = ImageGrab.grab(bbox=bbox)#screenshot
image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

transformed_image = full_change_perspective(image, 15)

[x,y] =transformed_image.shape[0:2]
black_pixels_mask = [[all(rgb < 25 for rgb in y) for y in x] for x in transformed_image]
transformed_image[black_pixels_mask] = [31,31,31]
cv2.imwrite('linkedin-background.png',transformed_image)