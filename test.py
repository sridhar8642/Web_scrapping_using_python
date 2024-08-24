import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "DNT": "1",
    "Connection": "close",
    "Upgrade-Insecure-Requests": "1"
}

res = requests.get("https://sea.ign.com/portal-2/180409/feature/the-top-100-video-games-of-all-time",headers=headers)
soup = BeautifulSoup(res.text,"html.parser")

games = soup.find('article',class_="article-section").find_all('h2')
games_list =[]
for game in games:
    games_dict ={}
    rank = game.text.split('.')[0]
    title = game.text.split('.')[1].strip()
    summary = game.find_next_sibling('p').text.strip()
    games_dict["Rank"] = rank
    games_dict["Title"]= title
    games_dict["summary"]= summary
    games_list.append(games_dict)

df = pd.DataFrame(games_list)
print(df)

conn = sqlite3.Connection("test.db")
cursor = conn.cursor()

qry = "create table if not exists games(Rank int,Title varchar(200),summary varchar(2000));"
cursor.execute(qry)

for i in range(len(df)):
    cursor.execute("insert into games values(?,?,?)",df.iloc[i])

conn.commit()
conn.close()




    
    



