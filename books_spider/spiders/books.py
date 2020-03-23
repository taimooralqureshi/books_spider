# -*- coding: utf-8 -*-
from time import sleep
from scrapy import Spider
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from scrapy.selector import Selector
from  scrapy.http import Request
class BooksSpider(Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
        
    def start_requests(self):
        self.driver = webdriver.Firefox()
        self.driver.get('http://books.toscrape.com')
        
        sel = Selector(text=self.driver.page_source)
        books = sel.xpath('//h3/a/@href').extract()

        for book in books:
            url = 'http://books.toscrape.com/' + book
            yield Request(url, callback=self.parse_book)

        while True:
            try:
                next_page = self.driver.find_element_by_xpath('//a[text()="next"]')
                sleep(3)
                self.logger.info('Sleeping for 3 sec...')
                next_page.click()

                # self.driver.get('http://books.toscrape.com')
        
                sel = Selector(text=self.driver.page_source)
                books = sel.xpath('//h3/a/@href').extract()

                for book in books:
                    url = 'http://books.toscrape.com/catalogue/' + book
                    yield Request(url, callback=self.parse_book)
            
            except NoSuchElementException:
                self.logger.info('No more pages to load. ')
                self.driver.quit()
                break

    def parse_book(self, response):
        pass