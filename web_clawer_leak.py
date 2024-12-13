import requests
from lxml import etree
import re
import csv
import pandas as pd


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Cookie':r'_lxsdk_cuid=193b83c2ab8c8-01e5b9c42ff0f4-26011851-144000-193b83c2ab8c8; _lxsdk=193b83c2ab8c8-01e5b9c42ff0f4-26011851-144000-193b83c2ab8c8; theme=moviepro; _lxsdk_s=193b83c2ab8-c71-c18-3be%7C%7C22'
}

df = pd.read_csv('movies.csv')
for i in range(len(df)):
    url = df.loc[i, 'movie_link']
    response = requests.get(url, headers=headers)
    html = etree.HTML(response.text)
    movie_time = html.xpath('//p[@class=".ellipsis-1"]/span/text()')
    if len(movie_time) != 0:
        
        movie_time = movie_time[0].replace(' ','').replace('\n','')
        df['movie_time'] = movie_time
        # print(movie_time)

with open('movies.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([title for title in df.columns])
    for i in range(len(df)):
        writer.writerow([df.loc[i, title] for title in df.columns])
