# -*- coding: utf-8 -*-
'''
Created on 2016��5��17��

@author: Administrator
'''


class UrlManager(object):
    
    
    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()
        

    
    def add_new_url(self,url):
        if url is None:
            print("add_new_url None")
            return False
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)
        return True

    
    def add_new_urls(self,urls):
        if urls is None or len(urls) == 0:
            return None
        for url in urls:
            self.add_new_url(url)
        return True
    
    def has_new_url(self):
        return len(self.new_urls) != 0


    
    def get_new_url(self):
        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url
    
    
    
    
    
    
    
    
    
    
    



