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
#     - I created the switch `-nodebug` on the command line, without this switch it will do this:
#         - show windows with the intermediate states of processing on screen;
#         - you can use left and right arrow keys to navigate intermediate steps;
#         - save the intermediate images with same name as the original as prefix and with suffix `_1`, `_2`, etc;
#         - on a production environment I would separate this on another class using python decorators to call it;
#         - on a production environment I would do the opposite: to create a `-debug` switch instead


# Usage:
#
#   python pycv-proj-test.py images/image_filename
#   python3 pycv-proj-test.py images/image_filename
#   python pycv-proj-test.py images/image_filename -nodebug

import numpy as np
import cv2
import sys


class FindCircles():

    def __init__(self, image_file, debug=True):
        self.img = cv2.imread(image_file)

        if self.img is None:
            raise RuntimeError("'%s' file not found." % image_file)

        self.debug = debug
        self.circles = None
        if debug:
            self.debug_images = []
            self.debug_images_count = 0
            self.debug_images_current = 0

    def execute(self):
        img = np.array(self.img, copy=True)

        self._show_step(0, "original", img)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        self._show_step(1, "gray scale", img)

        img = self.clean(img)
        self._show_step(2, "cleaned", img)

        circles = self.find_circles(img, param2=17)
        self.circles = circles
        original_image = np.array(self.img, copy=True)
        img = self.highlight_circles(original_image, circles)
        self._show_step(3, "final result", img)

        return img

    def clean(self, img):
        kernel = np.ones((3, 3), np.uint8)
        # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
        img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel, iterations=4)
        return img

    def find_circles(self, img, param2=36):
        circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 20, param1=150, param2=param2, minRadius=10, maxRadius=500)

        if circles is None:
            # no circle found use smaller param2 do it just once to avoid find too many circles and too many recursion
            # the easiest way if to set a min value to param2
            min_param2 = 18
            if param2 > min_param2:
                param2 /= 2
                return self.highlight_circles(img, param2)
            else:
                return None

        return circles

    def highlight_circles(self, img, circles):
        if circles is None:
            return img

        CIRCLE_COLOR = (255, 0, 0)
        CENTER_COLOR = (0, 0, 255)

        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center = (i[0], i[1])
            cv2.circle(img, center, i[2], CIRCLE_COLOR, 2)  # show circle
            cv2.circle(img, center, 2, CENTER_COLOR, 3)  # show centers as a 2 pixel radius circle
        return img

    def _show_step(self, n, title, img):
        if self.debug:

            self.debug_images_current = n
            self.debug_images_count += 1
            self.debug_images.append(img)

            while True:
                cv2.destroyAllWindows()

                title_format = "%d - %s - right and left arrow keys navigate steps"
                window_title = title_format % (self.debug_images_current, title)

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

    def _save_images(self):
        # TODO save all images on self.debug_images
        pass


def main():
    # do all the stuff
    find_circles = FindCircles(sys.argv[1])
    img = find_circles.execute()

    # create composite result image from initial and final images
    height, width, channels = img.shape
    black_image = np.zeros((height, 1, 3), np.uint8) # thin vertical black border
    result = np.hstack((find_circles.img, black_image, img))

    cv2.imshow("Final result", result)
    cv2.waitKey()

    # TODO print circle coordinates from CircleFinder
    # TODO save processed image with highlighted circles and print this action so the user knows it
    # TODO find -nodebug argument aun use the others as the file
    # TODO validate file existence before passing it

if __name__ == "__main__":
    main()
