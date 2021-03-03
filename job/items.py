# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobItem(scrapy.Item):
    job_title = scrapy.Field()
    job_comp = scrapy.Field()
    job_address = scrapy.Field()
    job_salary = scrapy.Field()
    job_time = scrapy.Field()
    job_detail = scrapy.Field()
    # job_language = scrapy.Field()
    job_workyear = scrapy.Field()
    job_edu = scrapy.Field()

