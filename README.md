# request_images
初学Python一段时间，在夯实基础的同时尝试做一些小的项目增加趣味。
以Python爬取网络数据方向进行简单的知乎回答图片爬取，把从零到最后实现的每个过程进行记录如下。
代码存在的问题和可以改善的地方还希望大家多多指正，共同进步。
### 项目流程分析
**执行思路：**
1. 获取目标网页信息
2. 解析HTML内容并提取图像链接提取
3. 根据链接获取对应图片，写入本地并保存
   
**需要使用到的库：requests、beautifulsoup、os、re库等**

### 版本一：获得单个网页下的单张图片
该版本下首先实现对一张图片的获取存储，通过对网页图片点击可以看到图片自身链接地址，则仅依靠requests库的get方法即可获得该链接下的图片，随后使用os库进行图片存储路径的设置。
```python
#Request_imagesV1.py 
import requests
import os

#控制台获取目标网页的单张图片链接
#直接复制的图片链接由于浏览器刷新在后缀后会补充信息，直接使用get()进行获取时会出现获取失败的现象。
#原始图片链接：https://pic1.zhimg.com/v2-72d66e54ad01534f455dead6826d279b_r.jpg?source=1940ef5c
#因此以问号为分隔符获取前面必需链接内容
url = input("请输入目标图片链接：").split('?')[0]
#url：https://pic1.zhimg.com/v2-72d66e54ad01534f455dead6826d279b_r.jpg

# 为该图片设定本地存储路径及存储名称
root = "E://images//"
path = root + url.split('/')[-1]
# 判断文件是否已存在、文件路径是否存在，避免重复爬取
try:
    if not os.path.exists(root):
        os.mkdir(root)
    if not os.path.exists(path):
        r = requests.get(url)
        with open(path,'wb') as f:
            f.write(r.content)
            f.close()
            print("文件保存成功")
    else:
        print("文件已存在")
except:
    print("爬取失败")
```

版本一实现了单张图片获取和存储，但需要提前获得目标图片的链接，然后利用requests库进行获得，**对包含多个图片的网页进行图片获取存在局限**。
因此思考一次性获得网页内全部图片链接后进行获取，开始尝试解析网页源代码获得所有图片的链接，即**beautifulsoup库**的使用。


### 版本二：批量获取一个网页内的图片内容
该版本中尝试将网页内容获取、解析、图片链接提取和图片下载存储分别写成函数进行调用，提高代码的可用性和易读性。

```python
# requests_imagesV2.py - 爬取单个页面下多张图片.
import requests
import os
from bs4 import BeautifulSoup

#防止爬取被阻挡，修改头文件相关参数
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
#对网页源代码进行分析，图片保存在RichContent-inner类下的figure标签
#标签下img属性后的src内容即为需要提取的图片链接。
def getImage(data):
    soup = BeautifulSoup(data,'lxml')
    content_list = soup.find('div',attrs={'class':'RichContent-inner'})
    imageList = []
    for item in content_list.find_all('figure'):
        img = item.find('img')['src'].split('?')[0]
        imageList.append(img)
    #将获取到的图片链接写入本地文件
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

    
#测试代码
if __name__ == '__main__':
    html = getHTML('https://www.zhihu.com/question/299384976/answer/516996409')
    getImage(html)
    with open('demo.txt') as f:
        for line in f.readlines():
            downloadImage(line.strip('\n'))
        f.close()
    print('Done')
```
版本二实现了回答页面下多张图片的获取，但仍然存在如下问题：
1. HTML内容解析部分不完善，获取到的图片中有一部分不能打开。考虑是不是因为爬取到了多余的src链接。
2. 对写入本地的链接没有进行重复性审查，导致多次运行过程中文本文件内出现了重复的图片链接，尽管在图片下载阶段可以规避，但仍需要优化。
3. 最重要的是，**由于知乎回答数量多，并不会一次性将所有回答的内容放在原网页，否则会造成加载内容的缓慢，因此采用的是Ajax进行批量式加载**。版本二的代码仅能获取当前加载图片，要爬取全部回答中的内容就需要依次对每个回答进行解析。
4. 此外，文件的存储和命名方面还可以优化，比如加入回答人的ID进行识别和进度条反应当前获取图片及存储的进度，增强用户体验。

