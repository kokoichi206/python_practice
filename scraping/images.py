import requests
import urllib.request
import os
from bs4 import BeautifulSoup
import re


HEADERS = {"User-Agent": "Mozilla/5.0"}
BASEURL = "http://blog.nogizaka46.com/"

# あるメンバーのブログ中の写真すべてを保存する、さかのぼれるだけ戻る
def scraping_allpic():
    # メンバーURL
    ## 名前の指定、'_'で区切る
    # member_name = "ayame_tsutsui"
    # member_name = "minami_hoshino"
    member_name = "renka_iwamoto"
    ## urlでのアクセスは.で名前を区切るので変換している
    name_for_url = member_name.replace('_','.')
    url = "http://blog.nogizaka46.com/" + name_for_url + "/"

    # フォルダ作成
    if not os.path.isdir(member_name):  # ”member_name”のフォルダがない場合
        print("creating folder")
        os.mkdir(member_name)

    # 保存枚数カウント用
    cnt = 0

    # BeautifulSoupオブジェクト生成
    ## これでurllib.error.HTTPErrorを解決できるかと思ったけど、無理でした。
    # headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0"}
    # soup = BeautifulSoup(requests.get(
    #     url, headers=HEADERS).content, 'html.parser')

    # print(type(soup))
    # print(soup)

    # page1の処理
    # 画像が置かれているhtmlを見つける
    # for entry in soup.find_all("div", class_="entrybody"):  # 全てのentrybodyを取得
    #     for img in entry.find_all("img"):  # 全てのimgを取得
    #         cnt += 1
    #         urllib.request.urlretrieve(
    #             img.attrs["src"], "./" + member_name + "/" + member_name + "-" + str(cnt) + ".jpeg")

    page_list = check_page_list(name_for_url)

    page_list.insert(0, '1')
    # page2以降の処理
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
                        img.attrs["src"], "./" + member_name + "/" + member_name + "-" + str(cnt).zfill(3) + ".jpeg")
                except urllib.error.HTTPError as err:
                    print(err)
                except KeyError as err:
                    print(err)
    
    print(str(cnt) + " pictures was saved")

# 人によってさかのぼれるページが違うので、それをチェックする
def check_page_list(member_name):
    url = BASEURL + member_name + "/"
    soup = BeautifulSoup(requests.get(
        url, headers=HEADERS).content, 'html.parser')
    a = soup.find_all("div", class_="paginate")
    
    str_html = str(a[0])
    result = re.findall(r'p=([\d]+)', str_html)
    return result[:-1]


if __name__ == '__main__':
    scraping_allpic()

