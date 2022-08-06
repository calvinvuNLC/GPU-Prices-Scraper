from bs4 import BeautifulSoup
import requests
import os

def pull_links_newegg():
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15'}

    links = []
    amd = []
    nvidia = []
    
    for x in range(1,4):
        r = requests.get('https://www.newegg.com/Desktop-Graphics-Cards/SubCategory/ID-48/Page-{x}?Tid=7709', headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        
        for l in soup.find_all('a'):
            links.append(str(l.get('href')))
        # print(links)
            
        parse1 = [i for i in links if 'rtx' in i or 'rx' in i]
        parse2 = [i for i in parse1 if '?' not in i or '=' not in i]
        parse3 = [*set(parse2)]
        
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
    
    file1 = open('prices.txt', 'w')
    
    for x in amd:
        print(x[1], x[0])
        file1.write(x[1] + " ")
        file1.write(x[0] + "\n")
        print(x[2])
        file1.write(x[2] + "\n\n")
        print()
    
    for x in nvidia:
        print(x[1], x[0])
        file1.write(x[1] + " ")
        file1.write(x[0] + "\n")
        print(x[2])
        file1.write(x[2] + "\n\n")
        print()
    
    file1.close()
    
    os.popen("open prices.txt")
    
pull_links_newegg()
