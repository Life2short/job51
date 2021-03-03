import scrapy
import json
import re
from ..items import JobItem
from scrapy import logformatter
from scrapy.http import Request


class Job51Spider(scrapy.Spider):
    name = 'job51'
    # jobType = 'Python语言'
    page = 1
    uri = 'https://search.51job.com/list/040000,000000,0000,00,9,99,Python,2,{}.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='
    start_urls = [uri.format(page)]
    custom_settings = {
        'DOWNLOAD_DELAY':6
    }

    def parse(self, response):
        # 爬取51job的职位信息
        # 1.分析51job职位信息页面的html的代码特点 看一下页面的规律
        jobDivItems = response.xpath("//script[@type='text/javascript']").extract()
        job_str = None
        for item in jobDivItems:
            if 'window.__SEARCH_RESULT__' in item:
                job_str = item
                break
        if not job_str:
            raise RuntimeError('无搜索结果')
        job_str = job_str.replace('<script type="text/javascript">\r\nwindow.__SEARCH_RESULT__ = ', '')
        job_str = job_str.replace('</script>', '')
        job_dict = json.loads(job_str)
        job_page = int(job_dict['total_page'])
        # print(job_page)

        for jobDivItem in job_dict['engine_search_result']:
            p_item = JobItem()
            # p_item['job_language'] = Job51Spider.jobType

            job_title = jobDivItem.get('job_title')
            if job_title:
                p_item['job_title'] = job_title.strip()

            job_comp = jobDivItem.get('company_name')
            if job_comp:
                p_item['job_comp'] = job_comp.strip()

            job_address = jobDivItem.get('workarea_text')
            if job_address:
                p_item['job_address'] = job_address.strip()

            job_salary = jobDivItem.get('providesalary_text', "面议")
            if not job_salary:
                job_salary = "面议"
            p_item['job_salary'] = job_salary.strip()

            job_time = jobDivItem.get('issuedate')
            if job_time:
                p_item['job_time'] = job_time.strip()

            job_workyear = jobDivItem.get('attribute_text')[1]
            p_item['job_workyear'] = job_workyear.strip()

            job_edu = jobDivItem.get('attribute_text')[2]
            p_item['job_edu'] = job_edu.strip()

            link = jobDivItem.get('job_href')

            yield scrapy.Request(url=link, callback=self.parse_detail, meta={'item': p_item})

        if self.page <= 2:
            self.page += 1
            next_page_url = self.uri.format(self.page)

            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_detail(self, response):
        job_detail_list = response.xpath('//div[@class="bmsg job_msg inbox"]//text()').extract()
        job_detail_str = "".join(job_detail_list)
        job_detail = re.findall('[\u4e00-\u9fa5a-zA-Z0-9]+', job_detail_str, re.S)
        job_detail = ' '.join(job_detail)
        item = response.meta['item']
        item['job_detail'] = job_detail
        yield item

