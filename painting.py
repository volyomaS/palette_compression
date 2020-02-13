import matplotlib.pyplot as plt
import cv2
import numpy as np


# function draws or saves picture
def draw_picture(image, save=False, filename=""):
    b, g, r = cv2.split(image)
    new_image = cv2.merge([r, g, b])
    plt.figure(figsize=(7, 5))
    plt.axis('off')
    if save:
        plt.imsave(filename, new_image)
    else:
        plt.imshow(new_image)
        plt.show()


# function changes colors to their average in their cluster
def fill_color(X, clusters, dbscan=False):
    n = max(clusters) + 1
    if dbscan:
        bias = 1
        n += 1
    else:
        bias = 0
    rsum = np.array([0]*n)
    gsum = np.array([0]*n)
    bsum = np.array([0]*n)
    count = np.array([0]*n)
    for i in range(len(X)):
        r, g, b = X[i][:]
        rsum[clusters[i]+bias] += r
        gsum[clusters[i]+bias] += g
        bsum[clusters[i]+bias] += b
        count[clusters[i]+bias] += 1
    rsum = rsum / count
    gsum = gsum / count
    bsum = bsum / count
    for i in range(len(X)):
        X[i] = [rsum[clusters[i]+bias], gsum[clusters[i]+bias], bsum[clusters[i]+bias]]
    return X
