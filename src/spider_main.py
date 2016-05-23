# -*- coding: utf-8 -*-
'''
Created on 2016��5��17��

@author: Administrator
'''
from baike_spider import html_outputer, url_manager, html_downloader,\
    html_parser



class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()

    
    def crawl(self, root_url):
        count = 0
        self.urls.add_new_url(root_url)
        while self.urls.has_new_url():
            try:
                count += 1
                if count>=100:
                    break
                new_url = self.urls.get_new_url()
                html_cont = self.downloader.claw(new_url)
                
                new_urls,new_data = self.parser.parse(new_url,html_cont)

                self.urls.add_new_urls(new_urls)

                self.outputer.collect_data(new_data)
                
                print("crawl worm %d\t%s"%(count,new_url))
            except:
                print("claw failed!")
        self.outputer.output_html()
    
    

        


if __name__=="__main__":
    root_url = "http://baike.baidu.com/view/21087.htm"
    obj_spider = SpiderMain()
    obj_spider.crawl(root_url)
    