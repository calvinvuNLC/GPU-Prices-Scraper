from email import header
from bs4 import BeautifulSoup
import requests

def pull_links(url):
    links = []
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    
    for l in soup.find_all('a'):
        links.append(str(l.get('href')))
    parse1 = [i for i in links if 'rtx' in i or 'rx' in i]
    parse2 = [i for i in parse1 if '?' not in i or '=' not in i]
    parse3 = [*set(parse2)]
    for l in parse3:
        # print(l)
        r = requests.get(l)
        soup = BeautifulSoup(r.text, "html.parser")
        price = soup.find("span", attrs={"class": "price-current-label"})
        name = soup.find("h1", class_='product-title').text
        pricesymbol = '$' + price.next_sibling.next_sibling.text + price.next_sibling.next_sibling.next_sibling.text
        print(name)
        print(pricesymbol)
        
    # testlink = 'https://www.newegg.com/gigabyte-geforce-rtx-3090-gv-n3090gaming-oc-24gd/p/N82E16814932327'
    # r = requests.get(testlink)
    # soup = BeautifulSoup(r.text, "html.parser")
    # price = soup.find("span", attrs={"class": "price-current-label"})
    # name = soup.find("h1", class_='product-title').text
    # pricesymbol = '$' + price.next_sibling.next_sibling.text + price.next_sibling.next_sibling.next_sibling.text
    # print(name)
    # print(pricesymbol)

pull_links("https://www.newegg.com/Desktop-Graphics-Cards/SubCategory/ID-48?Tid=7709")
