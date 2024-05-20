from bs4 import BeautifulSoup
import urllib.request

# Link til artikeloversikt på snl
link = urllib.request.Request("https://snl.no/.taxonomy/56")

with urllib.request.urlopen(link) as raw:
    soup = BeautifulSoup(raw)

articles = soup.find_all("a", class_ = 'link-list__link')
article_names = [x.string for x in articles]
print(article_names)
