import requests
import urllib.request
import os
from bs4 import BeautifulSoup
import re


# 全メンバーの顔写真を取得
def scrapingDetails():

    ## アクセスするurl
    TOP_URL = "https://www.nogizaka46.com/member"

    # BeautifulSoupオブジェクト生成
    headers = {"User-Agent": "Mozilla/5.0"}

    soup = BeautifulSoup(requests.get(TOP_URL, headers=headers).content, 'html.parser')
    details = soup.findAll("div", class_="unit")


    # infos = []
    # names = {}
    infos = {}
    personal_info = ["生年月日", "血液型", "星座", "身長"]
    for detail in details:
        person = {}
        nameJa = detail.find("a").find(class_="main").text

        href = detail.find("a").get("href")
        nameEn = href[9:-4]

        print(f'scraping {nameEn}...')

        memberURL = href[1:]
        URL = TOP_URL + memberURL
        soup = BeautifulSoup(requests.get(URL, headers=headers).content, 'html.parser')

        profiles = soup.find("div", id="profile")
        nameJa = ' '.join(profiles.find("h2").text.split()[2:4])
        profile = profiles.findAll("dd")
        for dt, dd in zip(personal_info,profile):
            person[dt] = dd.text
        infos[nameEn] = person

    return infos


if __name__ == '__main__':
    detailedInfo = scrapingDetails()
    print(detailedInfo)
    for a, v in detailedInfo.items:
        print("{" + a + ": " + v)

    # with open('.txt', mode='w') as f:
    #     for nameEn, nameJa in names.items():
    #         # f.write('{' + nameEn + ': ' + '"' + nameJa + '"},\n')
    #         f.write('["' + nameEn + '", ' + '"' + nameJa + '"],\n')

