import cv2
import numpy as np

windowName = "frame"


def nothing(x):
    pass


cv2.namedWindow(windowName)

# Create trackbars
cv2.createTrackbar("Lower h", windowName, 0, 179, nothing)
cv2.createTrackbar("Lower s", windowName, 0, 255, nothing)
cv2.createTrackbar("Lower v", windowName, 0, 255, nothing)
cv2.createTrackbar("Upper h", windowName, 179, 179, nothing)
cv2.createTrackbar("Upper s", windowName, 255, 255, nothing)
cv2.createTrackbar("Upper v", windowName, 255, 255, nothing)


class Process(object):
    def __init__(self, cap):
        self.lowerColor = None
        self.upperColor = None
        self.cap = cap
        self.main()

    def getMask(self, frame):
        # BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lowerColor, self.upperColor)
        return cv2.GaussianBlur(mask, (3, 3), cv2.BORDER_DEFAULT)

    def main(self):
        while(1):
            _, frame = self.cap.read()

            # Get current positions of four trackbars
            lh = cv2.getTrackbarPos("Lower h", windowName)
            ls = cv2.getTrackbarPos("Lower s", windowName)
            lv = cv2.getTrackbarPos("Lower v", windowName)
            uh = cv2.getTrackbarPos("Upper h", windowName)
            us = cv2.getTrackbarPos("Upper s", windowName)
            uv = cv2.getTrackbarPos("Upper v", windowName)

            self.lowerColor = np.array([lh, ls, lv])
            self.upperColor = np.array([uh, us, uv])

            mask = self.getMask(frame)

            result = cv2.bitwise_and(frame, frame, mask=mask)

            cv2.imshow(windowName, result)

            # When press "ESC" key, terminate process and
            # go to tracker
            if cv2.waitKey(1) & 0xFF == 27:
                break

        cv2.destroyAllWindows()
