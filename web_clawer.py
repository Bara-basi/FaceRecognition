import requests  # 网络请求库
import re  # 正则表达式库

# get()网络请求方式
# http和https的区别：https协议是由SSL+HTTP协议构建的可进行加密传输、身份认证的网络协议，比http协议安全。
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Cookie':r'bid=gdh17SxNDVg; _ga=GA1.1.1502282909.1714558796; ll="108090"; _ga_Y4GN1R87RG=GS1.1.1722945459.3.1.1722945578.0.0.0; _ga_RXNMP372GL=GS1.1.1722947735.1.0.1722947904.60.0.0; viewed="34802387_2870337_35680544"; _pk_id.100001.4cf6=326b603801befb14.1733525111.; _vwo_uuid_v2=DB125C1DAC0A7018DE054C6E94011C2F7|109f3a41f50681d5f9a45ace1b419c6f; ap_v=0,6.0; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1733642565%2C%22https%3A%2F%2Fwww.google.com%2F%22%5D; _pk_ses.100001.4cf6=1; dbcl2="183275916:ORvyiwLveRw"; ck=KdID; push_noty_num=0; push_doumail_num=0'
}
url = 'https://movie.douban.com/top250'
response = requests.get(url, headers=headers)
print("响应状态码：", response.status_code)
# print("响应体：", response.text)

# 解析网页,可是使用正则表达式、BeautifulSoup、XPath等解析方式
# 获取电影标题
# pattern = r'<span class="title">(.*?)</span>'  # ()是捕获组
# titles = re.findall(pattern, response.text)
# cleaned_titles = [title for title in titles if "&nbsp;" not in title]
# for title in cleaned_titles:
#     print(title)

# # 获取电影详情页链接
# pattern2 = r'<a href="(https://movie.douban.com/subject/[0-9]+/)" class="">'
# urls = re.findall(pattern2, response.text)
# for url in urls:
#     print(url)



#使用xpath解析网页
from lxml import etree
# xpath规则如下：
# // 匹配任何元素
# / 匹配子元素
# @ 匹配属性
# [] 匹配属性值
# text() 匹配元素的文本内容
html = etree.HTML(response.text)
# 只匹配a标签下的第一个span
titles = html.xpath(r'//div[@class="hd"]/a/span[1]/text()')
for title in titles:
    print(title)
urls = html.xpath(r'//div[@class="hd"]/a/@href')
for url in urls:
    print(url)
imgs = html.xpath(r'//div[@class="pic"]/a/img/@src')
for img in imgs:
    print(img)

# 保存txt文件,w-写,r-读,a-追加
with open('douban_top250.txt', 'w', encoding='utf-8') as f:
    for title in titles:
        f.write(title + '\n')

# 保存csv文件
import csv 
with open('douban_top250.csv', 'w', encoding='utf-8-sig',newline="") as f:
    writer = csv.writer(f)
    writer.writerow(['电影名', '电影链接', '图片链接'])
    for title, url, img in zip(titles, urls, imgs):
        writer.writerow([title, url, img])

# 保存图片
for title,img in zip(titles,imgs):
    img_path = 'img/'+ title + '.jpg'
    img_response = requests.get(img,headers=headers)
    with open(img_path, 'wb') as f:
        f.write(img_response.content)

#