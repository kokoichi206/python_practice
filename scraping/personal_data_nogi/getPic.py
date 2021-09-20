import requests
import urllib.request
import os
from bs4 import BeautifulSoup
import re


# 全メンバーの顔写真を取得
def scraping_allpic():

    ## アクセスするurl
    TOP_URL = "https://www.nogizaka46.com/member"

    # フォルダ作成
    if not os.path.isdir('Picture'):  # ”member_name”のフォルダがない場合
        print("creating folder")
        os.mkdir('Picture')


    # BeautifulSoupオブジェクト生成
    headers = {"User-Agent": "Mozilla/5.0"}

    soup = BeautifulSoup(requests.get(TOP_URL, headers=headers).content, 'html.parser')
    details = soup.findAll("div", class_="unit")

    aho = []
    for detail in details:
        href = detail.find("a").get("href")
        memberURL = href[1:]
        name = href[9:-4]

        accessURL = TOP_URL + memberURL

        soup = BeautifulSoup(requests.get(accessURL, headers=headers).content, 'html.parser')
        content = soup.find(id="profile")
        img = content.find("img")
        print(content)

        urllib.request.urlretrieve(
            img.attrs["src"], "./Picture/" + name + ".jpeg")


if __name__ == '__main__':
    scraping_allpic()
