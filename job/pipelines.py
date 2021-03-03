# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class JobPipeline:
    def process_item(self, item, spider):
        self.f.write(
            '{},{},{},{},{},{},{}\n'.format(
                item['job_title'],
                item['job_comp'],
                item['job_salary'],
                item['job_address'],
                item['job_edu'],
                item['job_workyear'],
                item['job_detail'],
                item['job_time'],
                # item['job_language'],
            )
        )
        return item

    def open_spider(self, spider):
        self.f = open('./data.csv', 'w')
        self.f.write('岗位名称,公司名称,工资,上班地址,学历,工作年限,职位描述,发布时间\n')

    def close_spider(self, spider):
        self.f.close()

