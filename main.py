from bs4 import BeautifulSoup

with open("./data/Nanoteknologi – Store norske leksikon.htm") as raw:
    soup = BeautifulSoup(raw)

articles = soup.find_all("a", class_ = 'link-list__link')
article_names = [x.string for x in articles]
print(article_names)
