# coding=utf-8

# Author: Airton da Fonseca Granero

# Developed and tested with PyCharm Community Edition 2017:
#
# os:             Windows 10 64 bit
# python version: 3.5.0
# opencv version: 3.3.0.10
# numpy version:  1.13.3
#

# Notes:
#
# - I pulled this to github [here](https://github.com/afgranero/py-cv-proj) ;
# - I have other repos, but they are private because they are not finished, tell me if you want access to them;
# - as this is a test and I am doing it alone, I did not use topic branches or issues;
# - I interpreted "detect circles" in two ways:
#     -  find circles centers;
#     - highlight the circles on the original image and save it
# - I took the following liberties:
#     - I used tab as 4 spaces (the default in my environment and as PEP 8 recommends);
#     - I used virtualenv to isolate libraries;
#     - I did not committed the virtual environment to git though, I used `pip freeze` to create a `requirements.txt`;
#     - refer to `requirements.txt` for the libraries versions needed;
#     - I created the switch `-debug` on the command line, it will do this:
#         - show windows with the intermediate states of processing on screen;
#         - you can use left and right arrow keys to navigate intermediate steps;
#         - save the intermediate images with same name as the original as prefix and with suffix `_1`, `_2`, etc;
#         - on a production environment I would separate this on another class using python decorators to call it;
#         - if there were much more test cases I would not print them individually, I would just save the steps.

# Usage:
#     python pycv-proj-test.py images/image_filename
#     python3 pycv-proj-test.py images/image_filename
#     python pycv-proj-test.py images/image_filename -nodebug
#     python3 pycv-proj-test.py images/image_filename -nodebug
#     python pycv-proj-test.py -nodebug images/image_filename
#     python3 pycv-proj-test.py -nodebug images/image_filename

import sys
import os
import math

import numpy as np
import cv2


class FindCircles:

    def __init__(self, image_file, debug=True):
        self.image_file = image_file
        self.img = cv2.imread(image_file)

        if self.img is None:
            raise RuntimeError("'%s' file not found." % image_file)

        self.circles = None
        self.debug = debug
        if debug:
            self.debug_images = []
            self.debug_titles = []
            self.debug_images_count = 0
            self.debug_images_current = 0

    def execute(self):
        img = np.array(self.img, copy=True)
        self._debug_show_step(0, "original", img)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        self._debug_show_step(1, "gray scale", img)

        img = self.clean_noise(img)
        self._debug_show_step(2, "cleaned", img)

        circles = self.find_circles(img, 37)
        self.circles = circles

        clusters = self.cluster_centers(circles, 50)

        img = self.highlight_clusters(self.img, clusters)
        self._debug_show_step(3, "result", img)

        return img

    def clean_noise(self, img):
        kernel = np.ones((3, 3), np.uint8)
        img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel, iterations=4)

        return img

    def find_circles(self, img, param2=50):
        circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 20, param1=150, param2=param2, minRadius=0, maxRadius=0)

        if circles is None:
            # no circle found
            # backtrack and use smaller param2 do it j
            # to avoid too many circles and too much recursion limit param2
            min_param2 = 14
            if param2 > min_param2:
                param2 /= 2.5
                return self.find_circles(img, param2)
            else:
                return None

        return circles

    def cluster_centers(self, circles, max_distance):
        # clusters = np.array([circles[0, :][0]])
        clusters = np.array([])
        for cir in circles[0, :]:
            min_distance = math.inf
            i = 0
            for clu in clusters:
                distance = math.hypot(clu[0] - cir[0], clu[1] - cir[1])
                if min_distance > distance > 0:
                    min_distance = distance
                    i_min = i
                i += 1

            if 0 < min_distance < max_distance:
                clu = clusters[i_min]
                clusters[i_min] = [(clu[0] + cir[0])/2, (clu[1] + cir[1])/2, (clu[2] + cir[2])/2]
            elif clusters.size == 0:
                clusters = np.array([[cir[0], cir[1], cir[2]]])
            else:
                clusters = np.append(clusters, [[cir[0], cir[1], cir[2]]], axis=0)

        clusters = np.array([clusters], copy=True)
        return clusters

    def highlight_clusters(self, img, circles):
        if circles is None:
            return img

        CIRCLE_COLOR = (255, 0, 0)
        CENTER_INNER_COLOR = (255, 255, 255)
        CENTER_OUTER_COLOR = (0, 255, 0)

        original_image = np.array(img, copy=True)
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center = (i[0], i[1])
            radius = i[2]
            cv2.circle(original_image, center, radius, CIRCLE_COLOR, 2)  # show circle
            cv2.circle(original_image, center, 3, CENTER_INNER_COLOR, -1)  # show centers as a 2 pixel radius ball
            cv2.circle(original_image, center, 3, CENTER_OUTER_COLOR, 1)  # show centers as a 2 pixel radius circle

        return original_image

    def _debug_show_step(self, n, title, img):
        if self.debug:
            self.debug_images_current = n
            self.debug_images_count += 1
            self.debug_images.append(img)
            self.debug_titles.append(title)

            out_file_name, out_file_extension = os.path.splitext(self.image_file)
            out_file_name = "%s_%d%s" % (out_file_name, n, out_file_extension)
            cv2.imwrite(out_file_name, img)

            while True:
                cv2.destroyAllWindows()

                title_format = "%d - %s - right and left arrow keys navigate steps, -nodebug to suppress those windows"
                window_title = title_format % (self.debug_images_current, self.debug_titles[self.debug_images_current])

                cv2.imshow(window_title, self.debug_images[self.debug_images_current])

                key = cv2.waitKeyEx(0)
                if key == 2555904 and self.debug_images_current == self.debug_images_count - 1:
                    # if right arrow was pressed but there is no more images get out of loop to next step
                    # must come before entering self.debug_images_current as tests do not use else if
                    cv2.destroyAllWindows()
                    break
                if key == 2555904 and self.debug_images_current < self.debug_images_count - 1:
                    self.debug_images_current += 1
                if key == 2424832 and 0 < self.debug_images_current:
                    self.debug_images_current -= 1
                if key != 2555904 and key != 2424832:
                    cv2.destroyAllWindows()
                    break


def show_result(img1, img2):
    # create composite result image from initial and final images
    height, width, channels = img2.shape
    black_image = np.zeros((height, 1, 3), np.uint8)  # thin vertical black border
    white_image = np.full((height, 1, 3), np.uint8(255)) # thin vertical white border
    result = np.hstack((img1, black_image, white_image, img2))

    cv2.imshow("Final result - (to enable intermediate results use -debug on command line)", result)
    cv2.waitKey()

def main():
    # do all the stuff
    if  len(sys.argv) > 3:
        print("Too many parameters.")
        exit(-1)

    debug_switch = "-debug"

    if len(sys.argv) == 1:
        print("No parameter supplied.")
        print("Usage:")
        print("    python %s %s" % (sys.argv[0], "file_name"))
        print("    python3 %s %s" % (sys.argv[0], "file_name"))
        print("    python %s %s %s" % (sys.argv[0], "file_name", debug_switch))
        print("    python3 %s %s %s" % (sys.argv[0], "file_name", debug_switch))
        print("    python %s %s %s" % (sys.argv[0], debug_switch, "file_name",))
        print("    python3 %s %s %s" % (sys.argv[0], debug_switch, "file_name"))
        exit(-1)

    if debug_switch in sys.argv and len(sys.argv) == 2:
        print("File name not supplied.")
        exit(-1)

    if debug_switch in sys.argv and len(sys.argv) == 3:
        debug = True
        pos = sys.argv.index(debug_switch)
        if pos == 1:
            file_name = sys.argv[2]
        elif pos == 2:
            file_name = sys.argv[1]
        else:
            print("Parameter not recognized")
            exit(-1)
    else:
        debug = False
        file_name = sys.argv[1]

    find_circles = FindCircles(file_name, debug)
    img = find_circles.execute()

    show_result(find_circles.img, img)

    # TODO find -nodebug argument and use the others as the file

if __name__ == "__main__":
    main()
