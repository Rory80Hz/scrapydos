import scrapy

class GcloudSpider(scrapy.Spider):
    name = "gcloud"

    def start_requests(self):
        baseurl = 'https://www.digitalmarketplace.service.gov.uk/g-cloud/search?page='
        for x in range(1,50):
            yield scrapy.Request(url=baseurl + str(x) + '&q=data+analytics', callback=self.parse)

    def parse(self, response):
        # page = response.url.split("/")[-1]
        self.logger.warning(response.url)
        filename = 'gcloud.csv'
        for section in response.selector.xpath('//div[@class="search-result"]'):
            company = section.xpath('p[1]/text()').extract_first()
            offering = section.xpath('h2/a/text()').extract_first()
            link = 'https://www.digitalmarketplace.service.gov.uk' + section.xpath('h2/a/@href').extract_first()
            description = section.xpath('p[2]/text()').extract_first()
            category = section.xpath('ul/li[1]/text()').extract_first()
            gcloud = section.xpath('ul/li[2]/text()').extract_first()
            entry = company.strip().replace('\n', ' ').replace('\r', '') + '|' + offering.strip().replace('\n', ' ').replace('\r', '') + '|' + description.strip().replace(
                '\n', ' ').replace('\r', '').replace('|', '') + '|' + category.strip().replace('\n', ' ').replace('\r', '') + '|' + gcloud.strip().replace('\n', ' ').replace('\r', '') + '|' + link.strip().replace('\n', ' ').replace('\r', '') + '\n'
            self.logger.warning(entry)            
            with open(filename, 'ab') as f:
                f.write(entry.encode('utf-8'))
        self.log('Saved file %s' % filename)
