# Test for Python + OpenCV developers


**Problem:**

Detect circles with diameter greater than 10 pixels.

**Comments on my solution:**

- I pulled this to github [here](https://github.com/afgranero/py-cv-proj) 
- I have other repos but they are private because they are not finished, tell me if you want access to them
- As this is a test and I am doing it alone I will not use topic branches or issues
- I interpreted "detect circles" in two ways:
    -  find circles centers;
    - highlight the circles on the original image and save it
- I took the following liberties:
    - I used tab as 4 spaces (the default in my environment and PEP 8 recommends);
 - I used virtualenv to isolate libraries;
 - I did not committed the virtual environment to git though, I used `pip freeze` to create a `requirements.txt`.
 - refer to `requirements.txt` for the libraries versions needed;
 - I created the switch `-debug` on the command line, will do two things:
         - show the intermediate states of processing on screen
         - save the intermediate images with same name as the original as prefix and with suffix `_1`, `_2`, etc
         - on a production environment I would separate this on another class using python decorators to call it
         - if there were more test cases I would not print them individually, I would just save the steps on disk

**Usage:**
```
python pycv-proj-test.py images/image_filename
python3 pycv-proj-test.py images/image_filename
python pycv-proj-test.py images/image_filename -nodebug
```