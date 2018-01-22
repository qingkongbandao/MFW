# -*- coding: utf-8 -*-
import scrapy
from MFW.items import MfwItem, MfwItemMore, MfwItemTag
import os
import json
import jsonpath
import re
import requests
import time
from lxml import etree

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class MfwSpider(scrapy.Spider):
    name = "mfw"
    allowed_domains = ["www.mafengwo.cn"]
    start_urls = (
        'http://www.mafengwo.cn/wenda/',
    )

    def __init__(self):
        super(MfwSpider, self).__init__(self)
        self.baseUrl = "http://www.mafengwo.cn/wenda/"
        self.titleBaseUrl = "http://www.mafengwo.cn"

    def parse(self, response):
        # 所有的城市名
        parent_names = response.xpath("//ul[@class='_j_open_mdd_list']/li/a/text()").extract()
        # 所有的城市所属page number
        parent_pages = response.xpath("//ul[@class='_j_open_mdd_list']/li/a/@data-mddid").extract()
        city_urls = self.parse_page(parent_pages)
        # print city_urls

        parent_names = [parent_name for parent_name in parent_names if parent_name != "更多".decode("UTF-8")]
        items = []
        for i in range(0, len(parent_names)):

            # 指定大目录的路径和目录名
            parent_filename = "./Data/" + parent_names[i]

            # 新增
            tag_filename = parent_filename + "/" + "标签"

            # 如果目录不存在，则创建目录
            if not os.path.exists(parent_filename):
                os.makedirs(parent_filename)
                if not os.path.exists(tag_filename):  # 新增标签
                    os.makedirs(tag_filename)
            # print "sdfaaaaaaaaaa" * 20
            # print city_urls
            # print parent_pages
            # http: // www.mafengwo.cn // wenda / detail - 10265432.html

            for k in range(0, len(city_urls)):
                item = MfwItem()
                # 保存大类的title和urls
                item['parentNames'] = parent_names[i]
                item['parentPages'] = parent_pages[i]

                if city_urls[k].find(item['parentPages']) > -1:
                    # if city_urls[k].find("more") != -1:  # 构建更多加载页面的子目录
                        # sub_title = city_urls[k][46:-14] + "&" + city_urls[k][65:]
                    if city_urls[k].find("more") != -1:  # 构建更多加载页面的子目录
                        pattern_mddid = re.compile("mddid=\d+")
                        sub_title = pattern_mddid.search(city_urls[k]).group() + "&" + city_urls[k][58:]
                        # sub_title = city_urls[k][46:-14]
                        # more_page = (city_urls[k][70:])

                    else:
                        sub_title = city_urls[k][29:-5]
                    sub_filename = parent_filename + '/' + sub_title

                    # 如果目录不存在，则创建目录
                    if not os.path.exists(sub_filename):
                        os.makedirs(sub_filename)

                    item['subTitle'] = sub_title
                    item['cityUrl'] = city_urls[k]
                    item['subFilename'] = sub_filename
                    # item['morePage'] = str(more_page)  # 传递这个一直报错KeyError: 'morePage'

                    item['tag_filename'] = tag_filename
                    items.append(item)

        for item in items:
            if item['cityUrl'].find("more") == -1:
                yield scrapy.Request(url=item['cityUrl'], meta={"meta_1": item}, callback=self.parse_city_url)
            else:
                # 更多
                yield scrapy.Request(url=item['cityUrl'], meta={"meta_more": item}, callback=self.parse_more_city_url)

    # 更多
    def parse_more_city_url(self, response):
        meta_more = response.meta['meta_more']
        # p = re.compile("{}")
        # a = p.search(response.body).group()
        print "%%%%%%%%%%%%" * 50

        try:
            dic = json.loads(response.body)
            # print dic
            data = dic.get("data")
            # print data
            html = data.get("html")
            if html:
                tree = etree.HTML(html)
                title_link_node_list = tree.xpath("//div[@class='title']/a/@href")
                print title_link_node_list
                print len(title_link_node_list)

                items = []
                # title_link_node_list = he.xpath("//div[@class='title']/a/@href")

                for title_link in title_link_node_list:
                    item = MfwItemMore()
                    # http://www.mafengwo.cn/wenda/detail-10602513.html 点击每个城市里每个标题链接
                    title_url = self.titleBaseUrl + title_link
                    item['subTitle'] = meta_more['subTitle']
                    item['cityUrl'] = meta_more['cityUrl']
                    item['subFilename'] = meta_more['subFilename']
                    item['parentNames'] = meta_more['parentNames']
                    item['parentPages'] = meta_more['parentPages']
                    item['titleURL'] = title_url

                    item['tag_filename'] = meta_more['tag_filename']  # 标签

                    items.append(item)

                for item in items:
                    yield scrapy.Request(url=item['titleURL'], meta={"meta_more_2": item},
                                         callback=self.parse_more_detail)
        except ValueError:
            pass

    # 更多
    def parse_more_detail(self, response):
        item = response.meta['meta_more_2']
        titles = response.xpath("//div[@class='q-title']/h1/text()").extract()

        title = ''
        for t in titles:
            title += t

        print title

        # 标题下面跟着的描述信息
        pattern_desc = re.compile(r'<div class="q-desc">(.*?)<div class="q-tags.*?>', re.S)
        pattern__desc_sub = re.compile(r"&(.*?);|<(.*?)>|\s")
        content_desc = ""
        if pattern_desc:
            content_desc_list = pattern_desc.findall(response.body)
            for desc in content_desc_list:
                body_desc = pattern__desc_sub.sub("", desc)
                content_desc += body_desc

        pattern = re.compile(r'<div class="_j_answer_html">(.*?)<div class="a-operate _js_operate.*?></div>', re.S)
        pattern_sub = re.compile(r"&(.*?);|<(.*?)>|\s")
        content_list = pattern.findall(response.body)
        content = ""
        for i in range(0, len(content_list)):
            body = pattern_sub.sub("", content_list[i])
            content += body + "\n"
        item["title"] = title.strip()
        item["title_desc"] = content_desc
        item['content'] = content

        # ==============
        # 小标签标题
        self.create_tag(response, item)

        yield item

    def parse_city_url(self, response):
        print response
        meta_1 = response.meta['meta_1']
        items = []
        title_link_node_list = response.xpath("//div[@class='title']/a/@href").extract()

        for title_link in title_link_node_list:
            item = MfwItem()
            # http://www.mafengwo.cn/wenda/detail-10602513.html 点击每个城市里每个标题链接
            title_url = self.titleBaseUrl + title_link
            item['subTitle'] = meta_1['subTitle']
            item['cityUrl'] = meta_1['cityUrl']
            item['subFilename'] = meta_1['subFilename']
            item['parentNames'] = meta_1['parentNames']
            item['parentPages'] = meta_1['parentPages']
            item['titleURL'] = title_url
            item['tag_filename'] = meta_1['tag_filename']

            items.append(item)

        for item in items:
            yield scrapy.Request(url=item['titleURL'], meta={"meta_2": item}, callback=self.parse_detail)

    def parse_detail(self, response):
        item = response.meta['meta_2']
        titles = response.xpath("//div[@class='q-title']/h1/text()").extract()

        title = ''
        for t in titles:
            title += t

        # 标题下面跟着的描述信息
        pattern_desc = re.compile(r'<div class="q-desc">(.*?)<div class="q-tags.*?>', re.S)
        pattern__desc_sub = re.compile(r"&(.*?);|<(.*?)>|\s")
        content_desc = ""
        if pattern_desc:
            content_desc_list = pattern_desc.findall(response.body)
            for desc in content_desc_list:
                body_desc = pattern__desc_sub.sub("", desc)
                content_desc += body_desc

        pattern = re.compile(r'<div class="_j_answer_html">(.*?)<div class="a-operate _js_operate.*?></div>', re.S)
        pattern_sub = re.compile(r"&(.*?);|<(.*?)>|\s")
        content_list = pattern.findall(response.body)
        content = ""
        for i in range(0, len(content_list)):
            body = pattern_sub.sub("", content_list[i])
            content += body+"\n"

        item["title"] = title.strip()
        item["title_desc"] = content_desc
        item['content'] = content

        # 新增小标签链接
        # tag_link_list = response.xpath("//a[@class='a-tag']/@href").extract()  # 小标签里的数据不要
        # 小标签标题
        self.create_tag(response, item)

        yield item

    # 创建小标签
    def create_tag(self, response, item):
        tag_title_list = response.xpath("//a[@class='a-tag']/text()").extract()
        for tag_title in tag_title_list:
            tag_sub_title = item["tag_filename"] + "/" + tag_title
            if not os.path.exists(tag_sub_title):
                os.makedirs(tag_sub_title)

    def parse_page(self, parent_pages):
        city_urls = []
        for j in range(0, len(parent_pages)):
            city_url = "{0}area-{1}.html".format(self.baseUrl, str(parent_pages[j]))
            count = 0
            while True:
                url = "http://www.mafengwo.cn/qa/ajax_qa/more?type=3&mddid=%s&sort=9&page=%d" % (
                        parent_pages[j], count)
                time.sleep(3)
                response = requests.get(url)  # 热门问题
                dic = json.loads(response.content)
                # print dic
                data = dic.get("data")
                # print data
                html = data.get("html")
                if html == "":
                    break
                # tree = etree.HTML(html)
                # node_list = tree.xpath("//div[@class='title']/a/@href")
                # print len(node_list)
                # print node_list
                # for node in node_list:
                #     city_urls.append(self.titleBaseUrl + node)

                city_urls.append(url)
                count += 1
            city_urls.append(city_url)

            print parent_pages[j] + "===================热门问题%d页============================" % count

            count_new = 0
            while True:
                url = "http://www.mafengwo.cn/qa/ajax_qa/more?type=0&mddid=%s&sort=1&page=%d" % (
                        parent_pages[j], count_new)

                response = requests.get(url)  # 最新问题

                time.sleep(3)
                dic = json.loads(response.content)
                # print dic
                data = dic.get("data")
                # print data
                html = data.get("html")
                if html == "":
                    break
                # tree = etree.HTML(html)
                # node_list = tree.xpath("//div[@class='title']/a/@href")
                # print len(node_list)
                # print node_list
                # for node in node_list:
                #     city_urls.append(self.titleBaseUrl + node)
                city_urls.append(url)
                count_new += 1
            print parent_pages[j] + "==============================最新问题%d页===============" % count_new
            city_urls.append(city_url)
        return city_urls
