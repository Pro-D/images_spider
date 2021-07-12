# requests_imagesV2.py - 爬取知乎单个页面图片.
import requests
import os
from bs4 import BeautifulSoup


#防止爬取被阻挡，修改头文件中用户为浏览器
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36",
    'Accept-Encoding': 'gzip, deflate'
}

#获取目标链接网页内容
def getHTML(url):
    try:
        response = requests.get(url,headers=headers)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response.text
    except:
        return "Error"

#解析网页内容得到图片链接
def getImage(data):
    soup = BeautifulSoup(data,'lxml')
    content_list = soup.find('div',attrs={'class':'RichContent-inner'})
    imageList = []
    for item in content_list.find_all('figure'):
        img = item.find('img')['src'].split('?')[0]
        imageList.append(img)
    #print(imageList)
    #将获取到的图片链接写入文件
    with open('demo.txt','a',encoding='utf-8') as f:
        for url in imageList:
            f.write(str(url)+'\n')
        f.close()
 
#根据图片链接下载图片并保存
def downloadImage(image_link):
    root = 'E://images//'
    path = root + image_link.split('/')[-1]
    try:
        if not os.path.exists(root):
            os.mkdir(root)
        if not os.path.exists(path):
            r = requests.get(image_link)
            with open(path,'wb') as f:
                f.write(r.content)
                f.close()
                print("图片已存入本地")
        else:
            print("文件已存在")
    except:
        print("图片下载失败")

    

if __name__ == '__main__':
    html = getHTML('https://www.zhihu.com/question/299384976/answer/516996409')
    getImage(html)
    with open('demo.txt') as f:
        for line in f.readlines():
            downloadImage(line.strip('\n'))
        f.close()
    print('Done')
    





