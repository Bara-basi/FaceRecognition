import requests
from lxml import etree
import re
import csv


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Cookie':r'bid=gdh17SxNDVg; _ga=GA1.1.1502282909.1714558796; ll="108090"; _ga_Y4GN1R87RG=GS1.1.1722945459.3.1.1722945578.0.0.0; _ga_RXNMP372GL=GS1.1.1722947735.1.0.1722947904.60.0.0; viewed="34802387_2870337_35680544"; _pk_id.100001.4cf6=326b603801befb14.1733525111.; _vwo_uuid_v2=DB125C1DAC0A7018DE054C6E94011C2F7|109f3a41f50681d5f9a45ace1b419c6f; ap_v=0,6.0; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1733642565%2C%22https%3A%2F%2Fwww.google.com%2F%22%5D; _pk_ses.100001.4cf6=1; dbcl2="183275916:ORvyiwLveRw"; ck=KdID; push_noty_num=0; push_doumail_num=0'
}
page_count = 1
movies =[]
for i in range(page_count):
    url = 'https://movie.douban.com/top250?start='+str(i*25)+'&filter='
    response = requests.get(url, headers=headers)
    print("响应状态码：",response.status_code)
    html = etree.HTML(response.text)
    urls = html.xpath(r'//div[@class="hd"]/a/@href')
    for url in urls:
        movie = {}
        inner_content = requests.get(url, headers=headers).text
        inner_html = etree.HTML(inner_content)

        #电影名称
        title = inner_html.xpath('//span[@property="v:itemreviewed"]/text()')
        movie['电影名称'] = title[0]

        # 电影类型
        classification = inner_html.xpath('//span[@property="v:genre"]/text()')
        classifications = ("|").join(classification)
        movie['电影类型'] = classifications

        # 制片国家'
        nation = inner_html.xpath('//span[@class="pl" and contains(text(), "制片国家/地区:")]/following-sibling::text()[1]')
        # pattern = r'制片国家/地区:</span>(.*)<br/>'
        # nation = re.search(pattern, inner_content)[1]
        movie['制片国家'] = nation[0]

        #上映时间
        release = inner_html.xpath('//span[@property="v:initialReleaseDate"]/text()')
        release_times = ("|").join(release)
        movie['上映时间'] = release_times

        #片长
        runtime = inner_html.xpath('//span[@property="v:runtime"]/text()')
        if runtime:
            movie['片长'] = runtime[0]

        #豆瓣评分
        score = inner_html.xpath('//strong[@property="v:average"]/text()')
        if score:
            movie['豆瓣评分'] = score[0]

        #剧情简介
        summary = inner_html.xpath('//span[@property="v:summary"]/text()')
        if summary:
            movie['剧情简介'] = summary[0].replace('\n', '').replace('\t', '').replace(' ', '').replace('\u3000', '')

        #电影链接
            movie['电影链接'] = url
        movies.append(movie)

# for movie in movies:
#     for key, value in movie.items():
#         print(key + ':' + value)
#     print('----------------------------------------------------------------------------------------------------------------------------')

with open('douban_top250.csv','w',encoding='utf-8-sig',newline='') as f:
    writer = csv.writer(f)
    writer.writerow(movies[0].keys())
    for movie in movies:
        writer.writerow(movie.values())