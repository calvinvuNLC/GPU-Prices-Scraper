from email import header
from bs4 import BeautifulSoup
import requests

def pull_links_newegg(url):
    links = []
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    
    for l in soup.find_all('a'):
        links.append(str(l.get('href')))
        
    parse1 = [i for i in links if 'rtx' in i or 'rx' in i]
    parse2 = [i for i in parse1 if '?' not in i or '=' not in i]
    parse3 = [*set(parse2)]
    
    amd = []
    nvidia = []
    
    for l in parse3:
        r = requests.get(l)
        soup = BeautifulSoup(r.text, "html.parser")
        price = soup.find("span", attrs={"class": "price-current-label"})
        name = str(soup.find("h1", class_='product-title').text)
        pricesymbol = '$' + price.next_sibling.next_sibling.text + price.next_sibling.next_sibling.next_sibling.text
    
        if "RTX" in name[:50]:
            nvidia.append((name[:60]+"...",pricesymbol,l))
        else:
            amd.append((name[:60]+"...",pricesymbol,l))
    
    amd.sort(key = lambda x: x[1])
    nvidia.sort(key = lambda x: x[1])
    for x in amd:
        print(x[1], x[0])
        print(x[2])
        print()
    
    for x in nvidia:
        print(x[1], x[0])
        print(x[2])
        print()

def pull_links_bh(url):
    links = []
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    
    for l in soup.find_all('a'):
        links.append(str(l.get('href')))
    for l in links:
        print(l)

# pull_links_newegg("https://www.newegg.com/Desktop-Graphics-Cards/SubCategory/ID-48?Tid=7709")
pull_links_bh("https://www.bhphotovideo.com/c/buy/Graphic-Cards/ci/6567")
