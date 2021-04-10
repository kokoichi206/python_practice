import datetime
import urllib.request   # これは組み込みモジュール
from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag


class Scraper(object):
    def __init__(self, site):
        self.site = site

    def scrape(self):
        r = urllib.request.urlopen(self.site)
        html = r.read()
        parser = "html.parser"
        sp = BeautifulSoup(html, parser)

        titles = []
        for tag in sp.find_all("a"):
            url = tag.get("href")
#            title = tag.contents
#            print(url)
            if url is None:
                continue
            # if "html" in url:
            if "articles" in url:
            #    print("\n" + url)
                title = tag.contents
                if len(title) == 1:
                    if type(title[0]) == NavigableString:
             #           print(title[0])
                        print(type(title[0]))
                        titles.append(title[0])
            # なぜかtitleがリストで帰ってくる
            # len == 1のものはタイトルと決め打ち
            #if len(title) == 1:
            #    print(title[0])
        return titles

news = "https://news.google.com"
titles = Scraper(news).scrape()
print("-"*60)
print(titles)

with open('./articles.txt', 'a') as f:
    dt_now = datetime.datetime.now()
    # 日付とタイトルは tab 区切り、タイトル間は , 区切り
    stringTitles = ','.join(titles)
    f.write(f"{dt_now}\t{stringTitles}\n")


