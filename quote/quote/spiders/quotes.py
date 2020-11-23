import scrapy

class Quote(scrapy.Spider):
    name = 'quotes'
    page_number = 2
    start_urls = ['https://www.goodreads.com/quotes?page=1']

    def parse(self, response):
        quotes = response.css('div.quote')
        for quote in quotes:
            quoteSentence = quote.css('.quoteText::text').extract()
            source = quote.css('.authorOrTitle::text').extract()
            yield {
                'quote': quoteSentence,
                'source': source
            }

