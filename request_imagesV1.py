#This program get images from webpage
import requests
import os

#获得知乎图片链接地址（手动输入版本）
#直接复制的图片链接由于浏览器刷新在后缀后会补充信息
#以问号为分隔符获取前面必须链接内容即可
#比如：原始图片链接：https://pic1.zhimg.com/80/v2-dfc81f0b3303003954bd6fc2438deec7_1440w.jpg?source=1940ef5c
#处理方法
url = input("请输入目标图片链接：").split('?')[0]
#处理后：
#url = "https://pic1.zhimg.com/80/v2-dfc81f0b3303003954bd6fc2438deec7_1440w.jpg"

#设置本地存储路径和图片命名
root = "E://images//"
path = root + url.split('/')[-1]
#开始获取图片
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


