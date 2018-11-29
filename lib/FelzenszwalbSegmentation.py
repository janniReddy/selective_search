import numpy as np
# import cv2
from Graph import Graph

def felzenswalb_seg(bgr_im, k=1.0, sigma=0.8, min_size=50):
    # bgr_im = cv2.GaussianBlur(bgr_im, (5, 5), sigma)
    graph = Graph(bgr_im.shape[0], bgr_im.shape[1])
    # k = 500
    # min_size = 20
    bgr_im = graph.segment_image(bgr_im, k, min_size)
    return bgr_im




# imgFile = './data/shore.ppm'
# bgr_im = cv2.imread(imgFile)
# bgr_im = cv2.GaussianBlur(bgr_im, (11, 11), 0)
# graph = Graph(bgr_im.shape[0], bgr_im.shape[1])
# k = 500
# min_size = 20
# bgr_im = graph.segment_image(bgr_im, k, min_size)
# cv2.imwrite('./data/shore_output.ppm', bgr_im)