# Detect the face box and save it.
import numpy as np
import cv2 as cv
import glob
from PIL import Image
import re
import os


# あとから使うように、えいごと日本語の対応を表から取ってくる
nameFile = './names.txt'
with open(nameFile) as f:
    names = f.readlines()

namesDict = {}
for i, name in enumerate(names):
    name = name.rstrip(',\n').split('"')
    namesDict[name[1]] = name[3]

# print(namesDict)

files = glob.glob("./Picture/*")

# フォルダ作成
FolderName = 'EyePicture'
if not os.path.isdir(FolderName):  # ”member_name”のフォルダがない場合
    print(f"creating folder {FolderName}...")
    os.mkdir(FolderName)




def detectAndSaveEyes(img):
    global saveFailed, canDetectMember

    memberName = re.search('([a-z]+).jpe?g', img).group(1)

    imgS = cv.imread(img)
    imgG = cv.cvtColor(imgS, cv.COLOR_BGR2GRAY)

    # 学習済みデータをロード
    face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
    eye_cascade  = cv.CascadeClassifier('haarcascade_eye.xml')

    # 顔検出を実行
    faces = face_cascade.detectMultiScale(imgG, 1.3, 5)
    if len(faces) == 1:
        (x,y,w,h) = faces[0]

        # 顔全体だと、歯も間違って検知してしまう確率あがる
        imgG_face = imgG[y:y+h, x:x+w] # 16枚Failed
        # imgG_face = imgG[y:y+int(h/1.5), x:x+int(w/1.5)]# 43枚Failed
        eyes = eye_cascade.detectMultiScale(imgG_face)
        if len(eyes) == 2:
            x1, y1, w1, h1 = eyes[0]
            x2, y2, w2, h2 = eyes[1]
            x_start = min(x1, x2) + x
            x_end = max(x1+h1, x2+h2) + x
            y_start = min(y1, y2) + y
            y_end = max(y1+w1, y2+w2) + y
            # return (x_start, y_start, x_end, y_end)

            from PIL import Image
            Image = Image.open(img)

            # 切り取り
            croppedIm = Image.crop((x_start, y_start, x_end, y_end))
            # サイズ変更
            Xsize, Ysize = croppedIm.size
            croppedIm = croppedIm.resize((3*Xsize, 3*Ysize))
            croppedIm.save(f'{FolderName}/{memberName}.png')
            canDetectMember.append(memberName)
        else:
            saveFailed += 1
            print(eyes)
            print(f'Could not detect 2 eyes: {memberName}')
    else:
        saveFailed += 1
        print(f"Could not detect {memberName}'s face")


def detectFace(image):
    # 顔検出対象の画像をロードし、白黒画像にしておく。
    imgS = cv.imread(image)
    imgG = cv.cvtColor(imgS, cv.COLOR_BGR2GRAY)

    # 学習済みデータをロード
    face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
    eye_cascade  = cv.CascadeClassifier('haarcascade_eye.xml')

    # 顔検出を実行
    faces = face_cascade.detectMultiScale(imgG, 1.3, 5)

    return faces

def cropAndSave(img, faces):
    memberName = re.search('([a-z]+).jpe?g', img).group(0)
    # facesはnumpyの形式で却って来てた....

    if len(faces) > 0:
        listFace = list(faces[0])
        from PIL import Image
        Image = Image.open(img)


        x,y,w,h = listFace
        croppedIm = Image.crop((x, y, x+w, y+h))
        croppedIm.save(f'{FolderName}/{memberName}.png')

    else:
        print(f"Could not detect {memberName}'s face")


saveFailed = 0
canDetectMember = []
for img in files:
    # faces = detectFace(img)
    # cropAndSave(img, faces)
    eyes = detectAndSaveEyes(img)

print(f'Failed {saveFailed} pictures')

with open('eyeNames.txt', mode='w') as f:
    for nameEn in canDetectMember:
        sentence = '["' + nameEn + '", "' + namesDict[nameEn] + '"],\n'
        f.write(sentence)
