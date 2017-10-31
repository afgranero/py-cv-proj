# coding=utf-8

# Author; Airton da Fonseca Granero

# Developed and tested with PyCharm Community Edition 2017:
#
# os:             Windows 10 64 bit
# python version: 3.5.0
# opencv version: 3.3.0.10
# numpy version:  1.13.3
#

# Notes:
#   - As this is a test and I am doing it alone I will not use topic branches or issues
#   - I interpreted "detect circles" in two ways:
#       - find circles centers
#       - highlight the circles on the original image and save it
#   - I took the following liberties:
#       - I used tab as 4 spaces (the default in my environment and PEP 8 recommended)
#       - the switch -debug on the command line, will do two things:
#           - show the intermediate states of processing on screen
#           - save the intermediate images with same name as the original as prefix and with  sufix _1, _2, etc
#           - on a production environment I would separate this on another class using python decorators to call it
##   -
# Use:
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
        self._show_step(0)

        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        self._show_step(1)

        self.img = self.clean()
        self._show_step(2)

    def clean(self):
        kernel = np.ones((3, 3), np.uint8)
        # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
        img = cv2.morphologyEx(self.img, cv2.MORPH_OPEN, kernel, iterations = 3)
        return img

    def _show_step(self, n):
        if self.debug:
            self.debug_images_current = n
            self.debug_images_count += 1
            self.debug_images.append(self.img)
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
