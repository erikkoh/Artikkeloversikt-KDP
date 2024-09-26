from bs4 import BeautifulSoup
import urllib.request
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd

# Link til artikeloversikt på snl
link = urllib.request.Request(
    "https://snl.no/.taxonomy/56",
)


session_cookie = "__session_id=" + str(input("Provide a session cookie: "))


with urllib.request.urlopen(link) as raw:
    soup = BeautifulSoup(raw.read().decode("utf-8"), "html.parser")

articles = soup.find_all("a", class_="link-list__link")
article_names = [(x.string).lower() for x in articles]
article_dic = {}


#getting all articles
article_links = [article.get("href") for article in articles]
for i in range(0, len(article_names)):
    article_request = urllib.request.Request(article_links[i])
    article_request.add_header("Cookie", session_cookie)
    with urllib.request.urlopen(article_request) as raw:
        soup = BeautifulSoup(raw.read().decode("utf-8"), "html.parser")
    article_info = soup.find(class_="l-article__meta")  # info box where time is found
    article_quality = (
        (soup.find(class_="quality-assessment__existing-heading")).find("span").string
    )

    # It works but looks awful
    multiple_timeformat = article_info.find("time", {"datetime": True})
    article_dic[article_names[i]] = {
        "Raw time": multiple_timeformat["datetime"],
        "Norwegian time": (multiple_timeformat.string).lstrip(),
        "Quality": article_quality.lstrip(),
    }


article_dic = dict(
    sorted(
        article_dic.items(),
        key=lambda item: datetime.strptime(item[1]["Raw time"], "%Y-%m-%dT%H:%M:%S%z"),
    )
)
for v in article_dic.values():
    v.pop("Raw time", None)

article_names = list(article_dic.keys())
norwegian_times = [v["Norwegian time"] for v in article_dic.values()]
qualities = [v["Quality"] for v in article_dic.values()]

df = pd.DataFrame(
    {
        "Artikkel": article_names,
        "Sist oppdatert": norwegian_times,
        "Kvalitet": qualities,
    }
)
df.to_excel("data/Siste_oppdatert_artikler.xlsx", index=False)
