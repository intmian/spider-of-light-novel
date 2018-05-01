import scrapy
import requests
import os
import re


class NovleSpider(scrapy.Spider):
    name = "novel"
    allowed_domains = ["http://q.dmzj.com"]
    fileAddress = r'D:\文件\轻小说'

    def start_requests(self):
        urls = []
        begin = 'http://q.dmzj.com/'
        end = '/index.shtml'
        for i in range(3, 5000):
            urls.append(begin + str(i) + end)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        sel = scrapy.selector.Selector(response)
        picture = sel.xpath('//body/div[4]/div/div[1]/img/@src').extract()
        picture = ''.join(picture)
        title = sel.xpath('//body/div[4]/div/div[1]/div/h3/text()').extract()
        title = ''.join(title)
        writer = sel.xpath(
            '//body/div[4]/div/div[1]/div/p[1]/text()').extract()
        writer = ''.join(writer)
        novleType = sel.xpath(
            '//body/div[4]/div/div[1]/div/p[2]/text()').extract()
        novleType = ''.join(novleType)
        condition = sel.xpath(
            '//body/div[4]/div/div[1]/div/p[3]/text()').extract()
        condition = ''.join(condition)
        lastNew = sel.xpath(
            '//body/div[4]/div/div[1]/div/p[4]/text()').extract()
        lastNew = ''.join(lastNew)
        fileAddress_ = NovleSpider.fileAddress
        fileAddress_ = fileAddress_ + '\\' + title
        os.makedirs(fileAddress_)
        with open(fileAddress_+'\\'+'书籍信息.txt', 'w') as fp:
            fp.write('书名：'+title+'\n'+writer+'\n'+novleType +
                     '\n'+condition+'\n'+lastNew)
        fp.close()  # 详细信息打印成功
        req = requests.get(picture)
        with open(fileAddress_+'\\'+'封面.jpg', 'wb') as fp:
            fp.write(req.content)
        fp.close()  # 照片打印成功
        fileAddress_ = fileAddress_+'\\'+title
        os.makedirs(fileAddress_)  # d:\data\$title\novel
        # 遇到了javascript动态渲染的。。。。。
        namePattern = '<div class=\"chapnamesub\">.*?</div>'
        namePattern = re.compile(namePattern)
        pathPattern = '_blank\" href=\".*?\">'
        pathPattern = re.compile(pathPattern)
        body = str(response.body, encoding="utf8")
        names = namePattern.findall(body)
        paths = pathPattern.findall(body)
        names_ = []
        paths_ = []
        for name in names:
            names_.append(name[25:-6])
        for path in paths:
            paths_.append(path[14:-2])

        max = len(names_)
        for i in range(max):
            req = requests.get(paths_[i])
            with open(fileAddress_+'\\'+names_[i]+'.txt', 'wb') as fp:
                fp.write(req.content)
            fp.close()
        '''如果没有渲染的话
        articlearea = sel.xpath('//body/div[5]/div[2]')
        articles = articlearea.xpath('.//div')
        print('articlessssssssss', articles)
        for article in articles:
            print('articleeeee', article)
            name = article.xpath('/div[1]/text()').extract()
            name = ''.join(name)
            href = article.xpath('/a/@href').extract()
            href = ''.join(href)
            re = requests.get(href)
            with open(fileAddress_+'\\'+name+'.txt', 'wb') as fp:
                fp.write(re.content)
            fp.close()
        '''
