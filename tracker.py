from process import Process
import numpy as np
import serial
import cv2


arduino = serial.Serial('COM7', 9600)

cap = cv2.VideoCapture(0)
capWidth = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

processer = Process(cap)


while 1:
    _, frame = cap.read()
    mask = processer.getMask(frame)

    # Find all contours in mask
    p, conts, __ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_NONE)

    if len(conts) > 0:
        # Getting biggest contour group in found contours
        biggestConts = max(conts, key=len)

        # Create rectangle found biggest contour
        x, y, w, h = cv2.boundingRect(biggestConts)

        # and draw it in frame
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Calculate center of the rectangle
        center = (x + int(w / 2), y + int(h / 2))

        # Draw circle in center
        cv2.circle(frame, center, 4, [0, 0, 255], -1)

        # If object is on the center
        if int(capWidth / 2) + 75 > center[0] > int(capWidth / 2) - 75:
            pass

        # If object is on the right
        elif center[0] > int(capWidth / 2):
            arduino.write(b'0')

        # If object is on the left
        elif center[0] < int(capWidth / 2):
            arduino.write(b'1')

    cv2.imshow("frame", frame)
    cv2.imshow("MASK", mask)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
