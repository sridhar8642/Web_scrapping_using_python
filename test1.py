from bs4 import BeautifulSoup
import requests,pandas as pd

# Define Headers and Target URL
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "DNT": "1",
    "Connection": "close",
    "Upgrade-Insecure-Requests": "1"
}

res = requests.get("https://ahrefs.com/top",headers=headers)
soup = BeautifulSoup(res.text,'html.parser')

webs = soup.find('tbody').find_all('tr',class_="css-6ypmas-tableRow")
web_list=[]
for web in webs:
    web_dict={}
    rank = web.find('td',class_="css-7f3fpx-cell css-s2uf1z").text
    title = web.findNext('a', class_="css-1eydlj5").text
    web_dict["Rank"] = rank
    web_dict["Title"] = title
    web_list.append(web_dict)
df = pd.DataFrame(web_list)
df.to_csv('top_100_websites.csv',index=False)

    