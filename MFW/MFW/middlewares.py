# -*- coding:utf-8 -*-

import scrapy
import time
from selenium import webdriver
from settings import USER_AGENT_LIST
import random


# class SeleniumMiddleware(object):
#     def process_request(self, request, spider):
#         if request.meta.has_key("selenium"):
#             url = request.url
#
#             driver = webdriver.Chrome()
#             driver.get(url)
#             time.sleep(1)
#
#             html = driver.page_source
#
#             driver.quit()
#             return scrapy.http.HtmlResponse(url, body=html, encoding="utf-8", request=request)


class UserAgentMiddleware(object):
    def process_request(self, request, spider):
        user_agent = random.choice(USER_AGENT_LIST)
        request.headers.setdefault("User-Agent", user_agent)














