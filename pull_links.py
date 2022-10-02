from distutils import file_util
from bs4 import BeautifulSoup
import webbrowser
import requests
import os

def pull_links():
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15'}

    links = []
    amd = []
    nvidia = []
    
    for x in range(1,5):
        r = requests.get('https://www.newegg.com/Desktop-Graphics-Cards/SubCategory/ID-48/Page-{x}?Tid=7709', headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        
        for l in soup.find_all('a'):
            links.append(str(l.get('href')))
            
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
    
    file = open('prices.txt', 'w')
    html = open('links.html', 'w')
    html.write("<!DOCTYPE html>\n")
    html.write("<html>\n")
    
    for x in amd:
        print(x[1], x[0])
        file.write(x[1] + " ")
        file.write(x[0] + "\n")
        print(x[2])
        file.write(x[2] + "\n\n")
        print()
        html.write(x[1] + " ")
        html.write(x[0] + "\n")
        hyperlink_format = '<p><a href="{link}">{text}</a></p>\n'
        html.write(hyperlink_format.format(link=x[2], text='LINK'))
    
    for x in nvidia:
        print(x[1], x[0])
        file.write(x[1] + " ")
        file.write(x[0] + "\n")
        print(x[2])
        file.write(x[2] + "\n\n")
        print()
        html.write(x[1] + " ")
        html.write(x[0] + "\n")
        hyperlink_format = '<p><a href="{link}">{text}</a></p>\n'
        html.write(hyperlink_format.format(link=x[2], text='LINK'))
    
    html.write("<html>")
    file.close()
    html.close()
    os.popen("open prices.txt")
    
def html_test():
    filename = 'file:///'+os.getcwd()+'/' + 'links.html'
    webbrowser.open(filename)
    
def main():
   pull_links()
   html_test()

if __name__ == "__main__":
    main()
