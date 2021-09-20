import numpy as np
import cv2 as cv




# 顔検出対象の画像をロードし、白黒画像にしておく。
imgS = cv.imread('kid.jpg')
imgG = cv.cvtColor(imgS, cv.COLOR_BGR2GRAY)

# 学習済みデータをロード
face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade  = cv.CascadeClassifier('haarcascade_eye.xml')

# 顔検出を実行
faces = face_cascade.detectMultiScale(imgG, 1.3, 5)

# 顔検出箇所を矩形で囲む。
for (x,y,w,h) in faces:
    cv.rectangle(imgS,(x,y),(x+w,y+h),(0,255,255),4)
    # 目を検出
    imgG_face = imgG[y:y+h, x:x+w]
    imgC_face = imgS[y:y+h, x:x+w]
    eyes = eye_cascade.detectMultiScale(imgG_face)
    for (ex,ey,ew,eh) in eyes:
        cv.rectangle(imgC_face,(ex,ey),(ex+ew,ey+eh),(0,128,255),4)

# 表示
cv.imshow('image',imgS)
cv.waitKey(0)

# 表示消去
cv.destroyAllWindows()
