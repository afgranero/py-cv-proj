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
#   - I pulled this to https://github.com/afgranero/py-cv-proj
#   - I have other repos but they are private tell me if you want access to them
#   - As this is a test and I am doing it alone I will not use topic branches or issues
#   - I interpreted "detect circles" in two ways:
#       - find circles centers
#       - highlight the circles on the original image and save it
#   - I took the following liberties:
#       - I used tab as 4 spaces (the default in my environment and PEP 8 recommended)
#       - I used virtualenv to isolate libraries
#       - I did not committed the virtual environment to git though, I used pip freeze to create a requiremtns.txt
#       - the switch -debug on the command line, will do two things:
#           - show the intermediate states of processing on screen
#           - save the intermediate images with same name as the original as prefix and with suffix _1, _2, etc
#           - on a production environment I would separate this on another class using python decorators to call it
#           - if there were more test cases I would not print them individually but just save the steps on disk

# Usage:
#
#   python pycv-proj-test.py images/image_filename
#   python3 pycv-proj-test.py images/image_filename
#   python pycv-proj-test.py images/image_filename -nodebug


import numpy as np
import cv2
import sys


class Finder():

    def __init__(self, imageFile, debug = True):
        self.img = cv2.imread(imageFile)
        self.debug = debug
        if debug:
            self.debug_images = []
            self.debug_images_count = 0
            self.debug_images_current = 0

    def find_circle(self):

        img = np.array(self.img, copy=True)

        self._show_step(0, img)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        self._show_step(1, img)

        img = self.clean(img)
        self._show_step(2, img)

        img = self.highlight_circles(img)
        self._show_step(3, img)

    def clean(self, img):
        kernel = np.ones((3, 3), np.uint8)
        # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
        img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel, iterations = 4)
        return img

    def highlight_circles(self, img, param2=36):
        # TO DO separate detect and highlight
        min_param2 = 18

        circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 20, param1=150, param2=param2, minRadius=10, maxRadius=500)

        if circles is not None:
            circles = np.uint16(np.around(circles))
            blue = (255, 0, 0)
            red = (0, 0, 255)
            for i in circles[0, :]:
                cv2.circle(self.img, (i[0], i[1]), i[2], blue, 2) # show circle as a green circle
                cv2.circle(self.img, (i[0], i[1]), 2, red, 3) # show centers as a red 2 pixel diameter circle
            return self.img
        else:
            # no circle found use smaller param2 do it just once to avoid find too many circles and too many recursion
            # the easiest way if to set a min value to param2
            if param2 > min_param2:
                param2 /= 2
                return self.highlight_circles(img, param2)
            else:
                return self.img


    def _show_step(self, n, img):
        if self.debug:
            self.debug_images_current = n
            self.debug_images_count += 1
            self.debug_images.append(img)
            key = 0
            while True:
                cv2.destroyAllWindows()
                cv2.imshow(str(self.debug_images_current), self.debug_images[self.debug_images_current])
                key = cv2.waitKeyEx(0) # & 0xFF
                if key == 2555904 and self.debug_images_current == self.debug_images_count - 1:
                    # if right arrow was pressed but there is no more images get out of loop to next step
                    # must come before antering self.debug_images_current as tests do not use else if
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
    finder = Finder(sys.argv[1])
    finder.find_circle()

    # TODO print circle coordinates from CircleFinder
    # TODO save processed image with highlighted circles and print this action so the user knows it
    # TODO find -nodebug argument aun use the others as the file
    # TODO validate file existence before passing it

if __name__=="__main__":
    main()
