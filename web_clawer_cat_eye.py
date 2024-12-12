import requests
from lxml import etree
import re
import csv


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Cookie':r'_lxsdk_cuid=193b83c2ab8c8-01e5b9c42ff0f4-26011851-144000-193b83c2ab8c8; _lxsdk=193b83c2ab8c8-01e5b9c42ff0f4-26011851-144000-193b83c2ab8c8; theme=moviepro; _lxsdk_s=193b83c2ab8-c71-c18-3be%7C%7C22'
}
page_count = 1
movies =[]
for i in range(8,15):
    url = f'https://piaofang.maoyan.com/rankings/year?year={2025-i}&limit=100&tab={i}'
    response = requests.get(url, headers=headers)
    print(f"第{i}页,响应状态码：{response.status_code}" )
    html = etree.HTML(response.text)
    # movie_name
    movie_name = html.xpath('//p[@class="first-line"]/text()')
    # release
    release = html.xpath('//p[@class="second-line"]/text()')
  
    # 票房(万元)
    box_office = html.xpath('//li[@class="col2 tr"]/text()')
    
    # 平均票价
    avg_price = html.xpath('//li[@class="col3 tr"]/text()')
   
    # 场均人数
    avg_people = html.xpath('//li[@class="col4 tr"]/text()')
    # 电影ID ->评分、类型、地区
    movie_id = html.xpath('//ul[@class="row"]/@data-com')
    for id,name,release_time,office,price,people in zip(movie_id,movie_name,release,box_office[1:],avg_price[1:],avg_people[1:]):
        movie = {} 
        movie['movie_id'] = id.split('/')[-1].replace("'","")
        inner_url = f'https://piaofang.maoyan.com/movie/{movie['movie_id']}'
        movie['movie_link'] = inner_url
        response = requests.get(inner_url, headers=headers)
        cur_url = response.url
        
        # 反爬
        while inner_url != cur_url:
            print(inner_url)
            input("程序异常,按任意键继续…")
            response = requests.get(inner_url, headers=headers)
            cur_url = response.url
        inner_html = etree.HTML(response.text)
        # 评分
        movies_score = inner_html.xpath('//span[@class="rating-num"]/text()')
        if len(movies_score) == 0:
            movie['movie_score'] = '暂无评分'
        else:
            movie['movie_score'] = inner_html.xpath('//span[@class="rating-num"]/text()')[0].replace(' ','').replace('\n','')
        # 类型
        movie_category = inner_html.xpath('//p[@class="info-category"]/text()')
        if len(movie_category) == 0:
            movie['movie_category'] = '暂无类型'
        else:
            movie['movie_category'] = movie_category[0].replace(' ','').replace('\n','').replace('/','')
        # 片长
        movie_time = inner_html.xpath('//p[@class=".ellipsis-1"]/span/text()')
        if len(movie_time) == 0:
            movie['movie_time'] = '暂无片长'
        else:
            movie['movie_length'] = movie_time[0].replace(' ','').replace('\n','')
        # 国家
        country = inner_html.xpath('//p[@class=".ellipsis-1"]/text()')
        if len(country) == 0:
            movie['country'] = '暂无'
        else:
            movie['country'] = country[0].split('<')[0].replace(' ','').replace('\n','').replace('/','')
        movie['movie_name'] = name
        movie['release'] = release_time
        movie['box_office'] = office
        movie['avg_price'] = price
        movie['avg_people'] = people
        movies.append(movie)

    with open('movies.csv', 'a', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        if i == 1:
            writer.writerow(['movie_id','movie_name','release','box_office','avg_price','avg_people','movie_score','movie_category','country','movie_link'])
        for movie in movies:
            writer.writerow([movie['movie_id'],movie['movie_name'],movie['release'],movie['box_office'],movie['avg_price'],movie['avg_people'],movie['movie_score'],movie['movie_category'],movie['country'],movie['movie_link']])
        movies = []
