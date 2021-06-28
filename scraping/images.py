import requests
import urllib.request
import os
from bs4 import BeautifulSoup
import re


HEADERS = {"User-Agent": "Mozilla/5.0"}
BASE_URL = "http://blog.nogizaka46.com/"
IMG_FOLDER = "./imgs/"

# あるメンバーのブログ中の写真すべてを保存する、さかのぼれるだけ戻る
def scraping_allpic(member_name):
    # メンバーURL
    ## urlでのアクセスは.で名前を区切るので変換している
    name_for_url = member_name.replace('_','.')
    url = BASE_URL + name_for_url + "/"

    # フォルダ作成
    member_path = IMG_FOLDER + member_name
    if not os.path.isdir(member_path):  # ”member_name”のフォルダがない場合
        print("creating folder")
        os.makedirs(member_path)

    # 保存枚数カウント用
    cnt = 0

    page_list = check_page_list(name_for_url)

    # page1のみ例外で扱わなくてもいいようにする
    page_list.insert(0, '1')
    for i in page_list:
        ## このpのマックスが12っぽい、それ以上はみれない
        url_tmp = url + f'?p={i}'
        # print(type(requests.get(url_tmp).status_code))
        print(f"now I'm searching page {i}")
        if requests.get(url_tmp).status_code == 404:
            break
        soup = BeautifulSoup(requests.get(url_tmp, headers=HEADERS).content, 'html.parser')
        for entry in soup.find_all("div", class_="entrybody"):  # 全てのentrybodyを取得
            for img in entry.find_all("img"):  # 全てのimgを取得
                cnt += 1
                try:
                    urllib.request.urlretrieve(
                        img.attrs["src"], member_path + "/" + member_name + "-" + str(cnt).zfill(3) + ".jpeg")
                except urllib.error.HTTPError as err:
                    print(err)
                except KeyError as err:
                    print(err)

    print(str(cnt) + " pictures was saved")

# 人によってさかのぼれるページが違うので、それをチェックする
def check_page_list(member_name):
    url = BASE_URL + member_name + "/"
    soup = BeautifulSoup(requests.get(
        url, headers=HEADERS).content, 'html.parser')
    a = soup.find_all("div", class_="paginate")

    str_html = str(a[0])
    result = re.findall(r'p=([\d]+)', str_html)
    return result[:-1]


if __name__ == '__main__':
	## 名前の指定、'_'で区切る
    scraping_allpic("minami_hoshino")

