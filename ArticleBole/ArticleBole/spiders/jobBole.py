import re

import scrapy
from scrapy.http import Request
from urllib import parse
import datetime
from scrapy.loader import ItemLoader

from ArticleBole.items import JobBoleArticleItem,ArticleItemLoader
from ArticleBole.utils.common import get_md5

class JobBoleSpider(scrapy.Spider):

    name = 'jobBole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):

        """ 
         1.获取文章的url     2.获取下一页的url        
        """
        # article_urls = response.xpath('//a[@class="archive-title"]/@href').extract()
        post_nodes = response.xpath('//div[@class="post floated-thumb"]/div[@class="post-thumb"]/a')
        for post_node in post_nodes:
            image_url = post_node.xpath('./img/@src').extract()[0]
            article_url = post_node.xpath('./@href').extract()[0]
            yield Request(article_url,meta={"front_image":image_url},callback=self.parseArticle)

        
        next_url = response.xpath('//a[@class="next page-numbers"]/@href').extract()[0]
        if next_url:
            yield Request(next_url,callback=self.parse)


    def parseArticle(self,response):

        front_image = response.meta.get('front_image','')

        '''
        article = JobBoleArticleItem()
        
        title = response.xpath('//div[@class="entry-header"]/h1/text()').extract()[0]
        time = response.xpath('//div[@class="entry-meta"]/p/text()').extract()[0].strip().replace('·','').strip()
        agree_num = int(response.xpath('//span[contains(@class,"vote-post-up")]/h10/text()').extract()[0])
        fav = response.xpath('//span[contains(@class,"bookmark-btn")]/text()').extract()[0]
        match_re = re.match(r".*?(\d+).*",fav)
        if match_re:
            fav_num = int(match_re.group(1))
        else:
            fav_num = 0
        comment = response.xpath('//a[@href="#article-comment"]/span/text()').extract()[0]
        match_re2 = re.match(r".*?(\d+).*", comment)
        if match_re2:
            comment_num = int(match_re2.group(1))
        else:
            comment_num = 0
        content = response.xpath('//div[@class="entry"]').extract()[0]

        article['title'] = title
        article['url'] = response.url
        article['url_object_id'] = get_md5(response.url)
        try:
            time = datetime.datetime.strptime(time,'%Y/%m/%d').date()
        except Exception as e:
            time = datetime.datetime.now().date()
        article['time'] = time
        article['agree_num'] = agree_num
        article['fav_num'] = fav_num
        article['comment_num'] = comment_num
        article['front_image_url'] = [front_image]
        article['content'] = content
        '''

        item_loader = ArticleItemLoader(item=JobBoleArticleItem(),response=response)

        item_loader.add_xpath('title','//div[@class="entry-header"]/h1/text()')
        item_loader.add_xpath('time','//div[@class="entry-meta"]/p/text()')
        item_loader.add_xpath('agree_num','//span[contains(@class,"vote-post-up")]/h10/text()')
        item_loader.add_xpath('fav_num','//span[contains(@class,"bookmark-btn")]/text()')
        item_loader.add_xpath('comment_num','//a[@href="#article-comment"]/span/text()')
        item_loader.add_xpath('content','//div[@class="entry"]')
        item_loader.add_value('url',response.url)
        item_loader.add_value('url_object_id',get_md5(response.url))
        item_loader.add_value('front_image_url',[front_image])

        article = item_loader.load_item()

        yield article


