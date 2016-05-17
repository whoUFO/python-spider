'''
Created on 2016Äê5ÔÂ17ÈÕ

@author: huyufeng
'''



import UrlManager
import UrlSpider
import HtmlPaser
import InfoManager


if __name__ == '__main__':
    rootUrl = 'http://www.100ppi.com/price/plist-993-1.html'
    urlManager = UrlManager.UrlManager()
    urlSpider = UrlSpider.UrlSpider()
    htmlPaser = HtmlPaser.HtmlPaser()
    infoManager = InfoManager.InfoManager()
    
    urlManager.AddUrl(rootUrl)
    while(not urlManager.HasNew()):
        url = urlManager.GetOne()
        response = urlSpider.Claw(url)
        newUrls = htmlPaser.GetUrls(response)
        urlManager.AddNew(newUrls)
        htmlInfo = htmlPaser.GetInfo(response)
        infoManager.AddInfo(htmlInfo)
    pass