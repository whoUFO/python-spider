# -*- coding: utf-8 -*-
'''
Created on 2016��5��17��

@author: Administrator
'''

from urllib.request import urlopen

class HtmlDownloader(object):
    
    
    def __init__(self):
        pass
        
    
    def claw(self,url):
        if url is None:
            return None
        response = urlopen(url)
        
        if response.getcode() != 200:
            return None
        
        return response.read()
    
    


    





