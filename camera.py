import cv2
from model import ERModel
import numpy as np

facec = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
model = ERModel("model.json", "model_weights.h5")
font = cv2.FONT_HERSHEY_SIMPLEX

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        _, fr = self.video.read()
        gray_fr = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
        faces = facec.detectMultiScale(gray_fr, 1.3, 5)

        for (x, y, w, h) in faces:
            fc = gray_fr[y:y+h, x:x+w]

            roi = cv2.resize(fc, (48, 48))
            pred = model.predict_emotion(roi[np.newaxis, :, :, np.newaxis])
            cv2.rectangle(fr, (0, y), (x-5,y+h), (255, 110, 99), 2)
            # cv2.putText(fr, "x:{0}, y:{1}, w:{2}, y:{3}".format(x, y, w, h), (0, y-15), font, 1, (55, 55, 55), 1)
            cv2.putText(fr, "x: {0}".format(x), (0, y+25), font, 1, (55, 55, 55), 1)
            cv2.putText(fr, "y: {0}".format(y), (0, y+50), font, 1, (55, 55, 55), 1)
            cv2.putText(fr, "w: {0}".format(w), (0, y+75), font, 1, (55, 55, 55), 1)
            cv2.putText(fr, "h: {0}".format(h), (0, y+100), font, 1, (55, 55, 55), 1)
            cv2.putText(fr, pred, (x, y), font, 2, (255, 255, 55), 2)
            # cv2.putText(fr, pred, (x, y), font, 1, (255, 255, 0), 2)
            cv2.rectangle(fr,(x,y),(x+w,y+h),(255,0,0),2)

        _, jpeg = cv2.imencode('.jpg', fr)
        return jpeg.tobytes()
