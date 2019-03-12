import asyncio
import base64
import os
import re

import execjs
from aiohttp_requests import requests
from lxml import etree

HOST = "http://shaoq.com:7777/"
MAIN_PAGE_URL = f"{HOST}exam"


async def req():
    # 跳转页请求
    resp = await requests.get(MAIN_PAGE_URL)
    resp_text = await resp.text()
    # 取出图片URL并且并发请求
    image_urls = [f"{HOST}{image.get('src')}" for image in etree.HTML(resp_text).xpath('//img')]
    await asyncio.gather(*[requests.get(image_url) for image_url in image_urls])

    # 拿到内容页
    resp1 = await requests.get(MAIN_PAGE_URL)
    resp1_text = await resp1.text()
    # print(resp1_text)
    doc = etree.HTML(resp1_text)

    # 调用JS生成CSS
    # os.path.dirname(__file__)是取当前py文件的相对路径
    js = execjs.compile(open(f"{os.path.dirname(__file__)}/js/exam1.js", encoding="utf-8").read())
    css = base64.b64decode(js.call("get_css", resp1_text)).decode()
    print(css)

    # 解析CSS并覆盖到span标签的text中
    css_dict = css2dict(css)
    spans = doc.xpath('//span')
    for span in spans:
        span.text = css_dict.get(span.get("class"))

    # 移除p和script标签，来源：https://stackoverflow.com/questions/7981840/how-to-remove-an-element-in-lxml
    for bad in doc.xpath("//body/p|//body/script"):
        bad.getparent().remove(bad)

    # 用xpath直接取出body下的所有text，在清除前后空格和换行符之后合并到同一个字符串
    exam_text = "".join([text.strip() for text in doc.xpath('//body//text()')])
    print(exam_text)


def css2dict(css: str) -> dict:
    return dict(re.findall(r'\.(.+)::before {content: "(.+)";}', css))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(req())
