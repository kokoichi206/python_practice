import requests
import urllib.request
import os
from bs4 import BeautifulSoup
import re


url_tmp = "http://blog.nogizaka46.com/renka.iwamoto/?p=6"

headers = {"User-Agent": "Mozilla/5.0"}
soup = BeautifulSoup(requests.get(url_tmp, headers=headers).content, 'html.parser')

urllib.request.urlretrieve("https://img.nogizaka46.com/blog/renka.iwamoto/img/2020/01/14/6236230/0003.jpg", "./aho.jpeg")