import requests
import glob
import re

import config


class LINENotifyBot:
    API_URL = 'https://notify-api.line.me/api/notify'
    def __init__(self, access_token):
        self.__headers = {'Authorization': 'Bearer ' + access_token}

    def send(
            self, message,
            image=None, sticker_package_id=None, sticker_id=None,
            ):
        payload = {
            'message': message,
            'stickerPackageId': sticker_package_id,
            'stickerId': sticker_id,
            }
        files = {}
        if image != None:
            files = {'imageFile': open(image, 'rb')}
        r = requests.post(
            LINENotifyBot.API_URL,
            headers=self.__headers,
            data=payload,
            files=files,
            )

# 写真をLineに送信する（すでに写真はある前提）
def main(name):
    # weight 用のaccess_token
    TOKEN = config.TOKEN
    bot = LINENotifyBot(access_token=TOKEN)

    member_name = name
    files = glob.glob(f"./{member_name}/*.jpeg")
    for file in files:
        print(file)
        number = re.findall(r'([\d]+)', file)
        print(number[0])
        bot.send(message=number[0],image=file,)

if __name__ == '__main__':
    main(name)
