from telegram import ParseMode, Update, Bot, Chat
from telegram.ext import CommandHandler, MessageHandler, BaseFilter, run_async

from tg_bot import dispatcher

import scrapy
from scrapy.crawler import CrawlerProcess

selected = ''
country = ''
confirmed = 0
deceased = 0
recovered = 0

class CovSpider(scrapy.Spider):
    name = 'cov_spider'
    start_urls = ['https://ncov2019.live/']
    def parse(self, response):
        global selected, country, confirmed, deceased, recovered
        table = response.css('#sortable_table_Global')
        rows = table.css('tr')
        for row in rows:
            country = row.css('.text--gray::text').getall()[0].strip()
            if country.lower() == selected.lower():
                confirmed = row.css('.text--green::text').getall()[0].strip()
                deceased = row.css('.text--red::text').getall()[0].strip()
                recovered = row.css('.text--blue::text').getall()[0].strip()
                break

cov_spider = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

def cov(bot: Bot, update: Update):
    global selected, country, confirmed, deceased, recovered
    message = update.effective_message
    selected = message.text.split(' ')[1]
    cov_spider.crawl(CovSpider)
    cov_spider.start()
    bot.send_message(
        message.chat.id,
        'Number of confirmed cases in %s: %s\nDeceased: %s\nRecovered: %s' % (country, confirmed, deceased, recovered),
        parse_mode = ParseMode.MARKDOWN
    )

__mod_name__ = 'COVID-19 Tracker'

COV_HANDLER = CommandHandler('cov', cov)

dispatcher.add_handler(COV_HANDLER)