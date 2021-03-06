import scrapy
from ..items import QuoteItem
import re

# cd quote
# scrapy crawl quotes
# scrapy crawl -o quotes.json

class Quote(scrapy.Spider):
    name = 'quotes'
    page_number = 2
    search = 'humor'
    start_urls = ['https://www.goodreads.com/quotes/tag/' + search + '?page=1']

    def parse(self, response):

        items = QuoteItem()

        quotes = response.css('div.quote')
        for quote in quotes:
            quote_sentence = str(quote.css('.quoteText::text').extract_first()).strip()
            quote_sentence = quote_sentence.replace('\u201c', '')
            quote_sentence = quote_sentence.replace('\u201d', '')
            source = str(quote.css('.authorOrTitle::text').extract_first()).strip()

            if len(re.findall(r'\w+', quote_sentence)) < 10:
                items['quote_sentence'] = quote_sentence
                items['source'] = source
                yield items

        next_page = 'https://www.goodreads.com/quotes/tag/' + Quote.search + '?page=' + str(Quote.page_number)
        if Quote.page_number <= 50:
            Quote.page_number += 1
            yield response.follow(next_page, callback=self.parse)

