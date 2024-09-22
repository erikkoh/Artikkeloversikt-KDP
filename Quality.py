from bs4 import BeautifulSoup
import urllib.request
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd

# Link til artikeloversikt på snl
link = urllib.request.Request("https://snl.no/.taxonomy/56",)

with urllib.request.urlopen(link) as raw:
    soup = BeautifulSoup(raw.read().decode('utf-8'), 'html.parser')

articles = soup.find_all("a", class_ = 'link-list__link')
article_names = [(x.string).lower() for x in articles]
article_dic = {}

#getting all articles
article_links = [x.get('href') for x in articles]
for i in range(0, len(article_names)):
    with urllib.request.urlopen(article_links[i]) as raw:
        soup = BeautifulSoup(raw.read().decode('utf-8'), 'html.parser')
    article_info= soup.find(
        class_ = "l-article__meta")
    #It works but looks awful
    multiple_timeformat = article_info.find(
        'time', {'datetime' : True})
    article_dic[article_names[i]] = [multiple_timeformat['datetime'], (multiple_timeformat.string).lstrip()]
print(article_dic)


article_dic = dict(sorted(article_dic.items(), key=lambda item: datetime.strptime(item[1][0], "%Y-%m-%dT%H:%M:%S%z")))
article_dic = {k: v[1] for k, v in article_dic.items()}
print(article_dic)

df = pd.DataFrame(article_dic.items(), columns=["Artikkel", "Sist oppdatert"])

df.to_excel('data/Siste_oppdatert_artikler.xlsx', index=False)
