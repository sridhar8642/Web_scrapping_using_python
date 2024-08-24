# Import the Packages
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
# Define Headers and Target URL
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "DNT": "1",
    "Connection": "close",
    "Upgrade-Insecure-Requests": "1"
}

base_url = 'https://www.imdb.com/chart/top/'

# Send a GET request to the Target URL
req = requests.get(base_url, headers=headers)
soup = BeautifulSoup(req.content, 'html.parser')

# You can name the variables as you like
get_html = soup.find_all('div', class_='sc-b189961a-0 iqHBGn cli-children')

movie_data = []
for html in get_html:

    movie_dic = {}
    # Movie Name
    movie_name = html.find('h3', class_='ipc-title__text')
    movie_dic['Movie Name'] = movie_name.text.strip() if movie_name else 'unknown movie name'

    # Release Date
    rel_date = html.find('span', class_='sc-b189961a-8 hCbzGp cli-title-metadata-item')
    movie_dic['Release Date'] = rel_date.text.strip() if rel_date else 'unknown release date'

    # Duration
    duration = html.find_all('span', class_='sc-b189961a-8 hCbzGp cli-title-metadata-item')[1]
    movie_dic['Duration'] = duration.text.strip() if duration else 'unknown duration'


    # Rating
    rating = html.find('span', class_='ipc-rating-star')['aria-label'].split()[-1]
    movie_dic['Rating'] = rating if rating else 'unknown rating'
    
    # Viewers
    viewers = html.find('span', class_='ipc-rating-star--voteCount')
    viewers = viewers.text.strip()
    viewers = re.match(r'\(([\d.]+[MK]?)\)', viewers) 
    movie_dic['Viewers'] = viewers.group(1) if viewers else 'unknown viewers'
    movie_data.append(movie_dic)
# Create a DataFrame
data = pd.DataFrame(movie_data)
print(data)