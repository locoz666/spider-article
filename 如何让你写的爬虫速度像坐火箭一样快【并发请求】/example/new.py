# coding=utf-8

import traceback
import asyncio
import random
import aiofiles
import os
from PIL import Image
import io
import re
from aiohttp_requests import requests

home_url = "http://desk.zol.com.cn"
headers1 = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
}


async def get_home_url(url, headers):
    # 请求首页url，提取分类url
    response = await requests.get(url, headers=headers)
    html_str = await response.text()
    p1 = r'<dt>壁纸分类：</dt>.*</a>.*<dl class="filter-item clearfix">'
    kind1 = re.compile(p1, re.DOTALL)
    dd_str = kind1.findall(html_str)
    p2 = r'a href="(.*?)"'
    kind2 = re.compile(p2)
    url_str = kind2.findall(dd_str[0])
    p3 = r'target="_blank">(.*?)<'
    kind3 = re.compile(p3, )
    url_name = kind3.findall(dd_str[0])
    label_url_list = []
    for i in range(len(url_str)):
        item_list = []
        url = home_url + url_str[i]
        label_name = url_name[i]
        item_list.append(label_name)
        item_list.append(url)
        print(item_list)
        label_url_list.append((item_list))
    return label_url_list


async def get_label_url(url, headers):
    # 请求分类页面，提取下一页url和当前页面图片包url地址列表
    response = await requests.get(url, headers=headers)
    html_str = await response.text()
    # 提取当前页面包含的图片url
    ###########################################################################################
    p1 = r'<ul class="pic-list2  clearfix">.*ins></li>		</ul>'
    kind1 = re.compile(p1, re.DOTALL)
    exist_img_str = kind1.findall(html_str)
    p2 = r'a class="pic" href="(.*?)"'
    kind2 = re.compile(p2)
    url_str = kind2.findall(exist_img_str[0])
    ############################################
    img_url_list = []
    for imgstr in url_str:
        img_url = home_url + imgstr
        img_url_list.append(img_url)
    # 提取下一页url地址
    try:
        page_str = r'a id="pageNext" href="(.*?)"'
        kind_page = re.compile(page_str, re.DOTALL)
        jump_page = kind_page.findall(html_str)
        nextpage_url = home_url + jump_page[0]
    except:
        nextpage_url = None
    print("下一页",nextpage_url)
    return img_url_list, nextpage_url


async def get_img_url(url, headers):
    # 提取图片地址列表
    response = await requests.get(url, headers=headers)
    html_str = await response.text()
    p1 = r'id="showImg".*</li></ul>'
    kind1 = re.compile(p1, re.DOTALL)
    img_url_str = kind1.findall(html_str)
    p2 = r'a href="(.*?)"'
    kind2 = re.compile(p2)
    url_str = kind2.findall(img_url_str[0])
    imglist = []
    for i in url_str:
        imgurl = home_url + i
        imglist.append(imgurl)
    return imglist


async def get_imgurl_imgname(url, headers):
    # 提取下载地址和图片名称
    response = await requests.get(url, headers=headers)
    html_str = await response.text()
    # 提取图片名称
    try:
        p1 = r'id="titleName".*html">(.*?)</a>'
        kind1 = re.compile(p1)
        imgname = kind1.findall(html_str)[0]
    except:
        imgname = "随机名" + str(random.randint(1, 9)) + "x"
    # 提取图片下载地址
    try:
        p2 = r'id="tagfbl".*class="laiyuan"'
        kind2 = re.compile(p2, re.DOTALL)
        imgurlstrlist = kind2.findall(html_str)
        p3 = r'href="(.*?)"'
        kind3 = re.compile(p3)
        imgurlstr = kind3.findall(imgurlstrlist[0])
        img_download_url = home_url + imgurlstr[0]
        ##############################################
        res = await requests.get(img_download_url, headers=headers)
        html = await res.text()
        rules = r'img src="(.*?)">'
        kind_rules = re.compile(rules)
        img_down_url = kind_rules.findall(html)[0]
    except:
        img_down_url = None

    return imgname, img_down_url


def if_type_name(name, types_url_list):
    # 判断要下载的分类，如果存在，就返回分类url地址，如果没有，提示分类不存在
    # name:输入的分类名称
    # types_url_list：所有分类的名称和url地址列表
    for types in types_url_list:
        if name in types[0]:
            print("你输入的是[%s]类，已经找到[%s]类" % (name, types[0]))
            print(types)
            print("马上开始下载[%s]类图片" % name)
            return types[1]

    else:
        print("未找到[%s]类" % name)


def mkdir(path):
    # 判断路径是否存在，存在则返回路径；不存在就创建路径
    is_exist = os.path.exists(path)
    if not is_exist:
        os.makedirs(path)
        print(path + "\t目录创建成功")
        return path
    else:
        print(path + "\t目录已存在")
    return path


async def img_width_height(url, headers):
    # 提取图片的长宽信息
    try:
        response = await requests.get(url, headers=headers)
        f = await response.read()
        imgs = io.BytesIO(f)
        img_file = Image.open(imgs)
        img_w_h = img_file.size
        img_w = img_w_h[0]
        img_h = img_w_h[1]
    except:
        img_w = 0
        img_h = 0
    return img_w, img_h


async def save_img(img_name, img_download_url, path):
    random_word = chr(random.randint(97, 122))
    filenametype = os.path.basename(img_download_url)[-3:]
    response = await requests.get(img_download_url)
    imgname = img_name + random_word + "." + filenametype
    imgname = imgname.replace("?", "").replace("/", "").replace("\\", "").replace(":", "").replace("*", "")
    imgname = imgname.replace('"', "").replace("<", "").replace(">", "").replace("|", "").replace(" ", "")
    imgname = imgname.replace("\n", "")
    if len(imgname) > 255:
        imgname = imgname[-251:]
    async with aiofiles.open(f"./{path}/{imgname}".strip(), "wb") as f:
        await f.write(await response.read())
        print("[%s]保存成功......" % imgname)


async def save(imgurl, num, path):
    try:
        imgname, img_download_url = await get_imgurl_imgname(imgurl, headers1)
        imgname = imgname + str(num)
        img_w, img_h = await img_width_height(img_download_url, headers1)
        if img_w >= 1440 or img_h >= 900:
            try:
                await save_img(imgname, img_download_url, path)
                print("第[%s]下载完成......" % imgname)
            except:
                traceback.print_exc()
                print("[%s]下载失败......" % imgname)
        else:
            print("[%s]像素过低，取消下载......" % imgname)
    except:
        print("[%s]请求失败......" % imgurl)


async def run():
    # 1.请求首页获取图片分类
    label_url_list = await get_home_url(home_url, headers1)
    # 2.选择需要下载的分类
    print("*" * 80)
    print("*" * 80)
    for label_str in label_url_list:
        print(label_str[0], end="\t")
    print("")
    print("*" * 80)
    print("*" * 80)
    print("以上是可以选择下载的分类!")
    kind_name = input("请输入要下载的分类:")
    type_url = if_type_name(kind_name, label_url_list)
    print(type_url)
    # 根据选择的分类开始下载图片
    # 创建目录
    path = mkdir(f"./zol图库/{kind_name}")
    x = 0
    while True:
        img_url_list, nextpage_url = await get_label_url(type_url, headers1)
        for img_url in img_url_list:
            try:
                imglist = await get_img_url(img_url, headers1)
                num = 0
                tasks = []
                for imgurl in imglist:
                    num += 1
                    tasks.append(save(imgurl, num, path))
                await asyncio.gather(*tasks)
            except:
                print("[%s]请求失败......" % img_url)
                continue

        if len(nextpage_url) > 0:
            type_url = nextpage_url
        else:
            print("[%s]图片下载完成，下载结束......" % kind_name)
            break

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
