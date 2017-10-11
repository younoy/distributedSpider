import scrapy
import os
import io

from scrapy import Request

from movieData.items import MovieDataLoader, MoviedataItem
from movieData.utils.Movies import Movies


class douban(scrapy.Spider):

    name = 'douban'
    # allowed_domains = ['douban.com']
    start_urls = []

    headers = {
        'host': 'www.douban.com',
        'refer': 'https://www.douban.com/search?cat=1002&q=',
        'user-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36'
    }

    m = Movies()
    movies,rid_to_name,name_to_rid,rid_to_movie = m.movieNames()
    name_to_genre = m.read_item_genre()

    for movie in movies:
        movieUrls = 'https://www.douban.com/search?cat=1002&q='+movie
        start_urls.append(movieUrls)

    def start_requests(self):
        for url in self.start_urls:
            movie_title = url.split('&')[1].split('=')[1]
            yield Request(url, meta={"movie_title":movie_title},dont_filter=True)

    def parse(self, response):
        movie_title = response.meta.get('movie_title', '')
        next_url = response.xpath('//div[@class="result-list"]/div[1]/div[@class="content"]/div/h3/a/@href').extract()[0]
        if next_url:
            yield Request(next_url, meta={"movie_title":movie_title},callback=self.parseMovie)

    def parseMovie(self,response):

        movie_title = response.meta.get('movie_title', '')
        title = self.rid_to_movie[self.name_to_rid[movie_title]]
        tags = self.name_to_genre[title]

        item_loader = MovieDataLoader(item=MoviedataItem(), response=response)
        print('正在获取%s的信息......'%(title))
        item_loader.add_value('etitle',title)
        # item_loader.add_xpath('ctitle', '//div[@id="mainpic"]/a/img/@src') //中文名称
        item_loader.add_xpath('image_url', '//div[@id="mainpic"]/a/img/@src')
        item_loader.add_value('tags',tags)
        item_loader.add_xpath('plot', '//div[@id="link-report"]/span[1]/text()')
        item_loader.add_xpath('rating', '//div[@id="interest_sectl"]/div/div[2]/strong/text()')
        item_loader.add_value('url', response.url)
        item_loader.add_xpath('recoMovies','//div[@id="recommendations"]/div/dl/dd/a/text()')

        article = item_loader.load_item()

        yield article

