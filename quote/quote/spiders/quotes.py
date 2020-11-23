import scrapy

class Quote(scrapy.Spider):
    name = 'quotes'
    page_number = 2
    start_urls = ['https://www.goodreads.com/quotes?page=1']

    def parse(self, response):
        quotes = response.css('div.quote')
        for quote in quotes:
            quote_sentence = quote.css('.quoteText::text').extract()
            source = quote.css('.authorOrTitle::text').extract()
            yield {
                'quote': quote_sentence,
                'source': source
            }
        next_page = 'https://www.goodreads.com/quotes?page=' + str(Quote.page_number)
        if Quote.page_number <= 10:
            Quote.page_number += 1
            yield response.follow(next_page, callback=self.parse)

