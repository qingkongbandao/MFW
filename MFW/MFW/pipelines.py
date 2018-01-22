# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


# import json

#
# class MfwPipeline(object):
#     def __init__(self):
#         self.f = open("fh.json", "w")
#
#     def process_item(self, item, spider):
#         content = json.dumps(dict(item), ensure_ascii=False) + ",\n"
#         self.f.write(content)
#         return item
#
#     def close_spider(self, spider):
#         self.f.close()

# import re
import sys
from items import MfwItem, MfwItemMore
reload(sys)
sys.setdefaultencoding("utf-8")


class MfwPipeline(object):

    # def __init__(self):
    #     self.fp = None
    #     print "@@@@@@@@@@@@@   管道对象初始化@@@@@@@@@@@"

    def process_item(self, item, spider):
        if isinstance(item, MfwItem):
            print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@管道文件在处理item数据@@@@@@@@@@@@@@@@@@@@@@"
            filename = item['titleURL'][29: -5]
            filename += '.txt'
            # count = 1
            # if item['titleURL'].find('more') != -1:
            #     p = re.compile("mddid=\d+")
            #     file_title = p.search(item['titleURL']).group()
            #     # filename = item['titleURL'][46: -15]+"-" + str(self.count) + ".txt"
            #     filename = file_title + ".txt"
                # count += 1

            # # == == == == == ==./ Data / 嘉兴 / area - 10128
            # # == == == == == == == == == detail - 10584519.txt
            print '================'+item['subFilename']  # ./Data/香港/mddid=10189-page=1
            print '=================='+filename  # detail-9183871.txt
            #

            print "@@@@@@@@@@@@@@@@@@@@@@@@@@  @@@@@@@@@@                 管道文件 打开文件写数据"
            # fp = open(item['subFilename'] + '/' + filename, 'w')
            # fp.write(item['title']+"\n")
            # fp.write(item['content'])
            # fp.close()
            sub_file_name = item['subFilename'] + "/" + filename
            print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~文件名" + sub_file_name  #文件名./Data/香港/mddid=10189-page=1/detail-9183871.txt


            with open(sub_file_name, 'w') as f:
                f.write(item['title'] + "\n")
                f.write(item['title_desc'] + "\n")
                f.write(item['content'])
                f.flush()

            print "@@@@@@@@@@@@@@@@@@@@@@@@@@  @@@@@@@@@@                 管道文件 写数据完毕关闭文件"

            print "=============================="+item["title"]
        return item

            # print "============================="+item["content"]

    # def close_spider(self, spider):
    #     print "@@@@@@@@@@@@@@      管道文件关闭@@@@@@@@@@@@@@"
    #     self.fp.close()


class MfwPipelineMore(object):
    # def __init__(self):
    #     self.fp = None
    #     print "$$$$$$$$$$$$$$$$$$$$$     more 管道 初始化完成"

    def process_item(self, item, spider):
        if isinstance(item, MfwItemMore):
            print "$$$$$$$$$$$$$$$$$$$$$$$$more item数据$$$$$$$$$$$$$$$$$$$$$$$$$"
            # filename = item['subFilename']
            # filename += '.txt'
            # fp = open(filename, 'w')
            # fp.write(item['content'])
            # fp.close()

            filename = item['titleURL'][29: -5]
            filename += '.txt'

            # # == == == == == ==./ Data / 嘉兴 / area - 10128
            # # == == == == == == == == == detail - 10584519.txt
            print '================' + item['subFilename']
            print '==================' + filename
            #

            print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$  more 管道 打开文件写数据"
            # fp = open(item['subFilename'] + '/' + filename, 'w')
            # fp.write(item['title'] + "\n")
            # fp.write(item['content'])
            # fp.close()
            #
            sub_file_name = item['subFilename'] + "/" + filename
            print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~文件名"+sub_file_name



            with open(sub_file_name, 'w') as f:
                f.write(item['title'] + "\n")
                f.write(item['content'])
                f.flush()

            print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$  more 管道 写数据结束关闭文件"
        return item

    # def close_spider(self, spider):
    #     print "$$$$$$$$$$$$$$$$$$$$$$$$    more 管道关闭"
    #     self.fp.close()
