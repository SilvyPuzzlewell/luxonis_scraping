from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from spiders.srealityspider import SRealityFlatsForSaleSpider

settings = get_project_settings()
process = CrawlerProcess(get_project_settings())
process.crawl(SRealityFlatsForSaleSpider)
process.start()