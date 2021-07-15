"""
Класс для детектирования QR кодов с изображений
"""

import cv2
import math
import numpy as np

class QR_detector():
    def __init__(self):
        #self.image = image
        self.qrCodeDetector = cv2.QRCodeDetector()
    def main_detect(self,image):

        close = self.detect_QR(image)
        code = self.QR_detecton_in_images(close)
        return code

    def QR_detecton_in_images(self, image):
        decodedText, points, _ = self.qrCodeDetector.detectAndDecode(image)
        qr_data = decodedText.split(',')

        if points is not None:
            pts = len(points)
            print(pts)
            for i in range(pts):
                nextPointIndex = (i+1) % pts
                cv2.line(image, tuple(points[i][0]), tuple(points[nextPointIndex][0]), (255,0,0), 5)
                print(points[i][0])

            print(decodedText)
            return int(decodedText)
        else:
            print("QR code not detected")
            return None


    def detect_QR(self,image):
        # Grayscale, Gaussian blur, Otsu's threshold
        original = image.copy()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (9, 9), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        # Morph close
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

        # Find contours and filter for QR code
        cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.04 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
            area = cv2.contourArea(c)
            ar = w / float(h)
            if len(approx) == 4 and area > 1000 and (ar > .85 and ar < 1.3):
                cv2.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 3)
                ROI = original[y:y + h, x:x + w]
                #cv2.imwrite('ROI.png', ROI)

        #cv2.imshow('thresh', thresh)
        if (1==0):
            imS = cv2.resize(close, (300, 300))
            cv2.imshow('close', imS)
            #cv2.imshow('image', image)
            #cv2.imshow('ROI', ROI)
            cv2.waitKey()
        #Черный в белый и обратно
        id=np.where(close==0)
        id1 = np.where(close==255)
        close[id]=255
        close[id1] = 0
        close1 = np.zeros((close.shape[0],close.shape[1],3)).astype('int32')
        close1[:,:,0], close1[:,:,1], close1[:,:,2] = close, close, close
        return close