import re
import requests
from bs4 import BeautifulSoup
import csv
import json

url_dict={}

url="http://www.shicimingju.com/chaxun/zuozhe/1.html"
response=requests.get(url)
content=BeautifulSoup(response.content,"lxml")

head=[]
urls=[]
h=content.find_all('div',class_="www-shadow-card www-main-container")
for k in h:
    a=k.find_all('h3')
    for j in a:
        b = re.match(r'.*?、<a href=".*?">(.*?)</a></h3>', str(j))
        head.append(b.group(1))
        c= re.match(r'.*?、<a href="(.*?)">.*?</a></h3>', str(j))
        urls.append(c.group(1))

for i in range(2,26):
    url = "http://www.shicimingju.com/chaxun/zuozhe/1"+'_'+str(i)+".html"
    response=requests.get(url)
    content = BeautifulSoup(response.content, "lxml")
    h = content.find_all('div', class_="www-shadow-card www-main-container")
    for k in h:
        a = k.find_all('h3')
        for j in a:
            b = re.match(r'.*?、<a href=".*?">(.*?)</a></h3>', str(j))
            head.append(b.group(1))
            c = re.match(r'.*?、<a href="(.*?)">.*?</a></h3>', str(j))
            urls.append(c.group(1))
#print(urls)
poet=[]
explain=[]
sign=[]
for i in urls:
    url="http://www.shicimingju.com"+i
    response = requests.get(url)
    content = BeautifulSoup(response.content, "lxml")
    h = content.find_all('div', class_="shici-content")
    for j in h:
        a = j.find_all(text=True)
        poet.append(a)

    h = content.find_all('div', class_="shici-mark")
    if(len(h)>0):
        for j in h:
            a = j.find_all('a')
            a_list = []
            for j in range(len(a)):
                b = re.match(r'<a href=.*?>(.*?)</a>', str(a[j]))
                a_list.append(b.group(1))
            sign.append(a_list)
    else:
        sign.append('None')

    h = content.find_all('div', class_="shangxi-container")
    if(len(h)>0):
        for j in h:
            a = j.find_all(text=True)
            c=list(a)
            a_list=[]
            for sentence in c:
                a_list.append(sentence)
            explain.append(a_list)
    else:
        explain.append('None')

data=[]
for item in range(len(head)):
    a_item={}
    a_item['title']=head[item]
    a_item['paragraphs']=poet[item]
    a_item['category']=sign[item]
    a_item['explain']=explain[item]
    data.append(a_item)

with open('LiBaiPoet.json','w') as f:
    json.dump(data,f,ensure_ascii=False,indent=4)
print('done')