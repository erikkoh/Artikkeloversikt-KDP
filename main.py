from bs4 import BeautifulSoup
import urllib.request
import matplotlib.pyplot as plt

# Link til artikeloversikt på snl
link = urllib.request.Request("https://snl.no/.taxonomy/56")

with urllib.request.urlopen(link) as raw:
    soup = BeautifulSoup(raw)

articles = soup.find_all("a", class_ = 'link-list__link')
article_names = [(x.string).lower() for x in articles]
kdp_articles = []
non_kdp_artilces = []

#   Dead end could be attempted but not all writers have a "fagmedarbeider", could potensially crawl Timini.no and look for KDP-member 
article_links = [x.get('href') for x in articles]
for i in range(0,len(article_links)):
    with urllib.request.urlopen(article_links[i]) as raw:
        soup = BeautifulSoup(raw)
    # Each article can have multiple authors its considered written by kdp if atleas one of the co-athors are from kdp
    athour_links = soup.find_all('li', class_ = 'author-list__author')  
    writer_class = []
    for items in athour_links:
        profile_link = items.a.get('href')
        with urllib.request.urlopen(profile_link) as raw:
            soup = BeautifulSoup(raw)

        #this takes into consideration if the profile lacks a p-tag
        try: 
            writer_class.append(str(soup.find(id = 'profileName').p.string))
        except:
            writer_class.append("classless")
        
    #makes it easier to identify "fagmedarbeider"
    writer_class = ''.join(writer_class)
    #The athor of gray goo does not have the fagmederbeider title but is in the total overview in the drive
    if ('fagmedarbeider' in writer_class) or article_names[i] == "gray goo": 
        kdp_articles.append(article_names[i])
    else:
        non_kdp_artilces.append(article_names[i])

labels = "KDP", "SNL"
sizes = [len(kdp_articles), len(non_kdp_artilces)]
print(kdp_articles)

fig, ax = plt.subplots()
ax.pie(sizes, labels=labels, autopct='%1.1f%%')
ax.set_title("Nanoteknologi skrevet av KDP vs SNL")
plt.savefig("overview.jpeg")



