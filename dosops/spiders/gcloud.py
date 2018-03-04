import scrapy

class GcloudSpider(scrapy.Spider):
    name = "gcloud"

    def start_requests(self):
        baseurl = 'https://www.digitalmarketplace.service.gov.uk/g-cloud/search?q=&page='
        for x in range(1,252):
            yield scrapy.Request(url=baseurl + str(x), callback=self.parse)

    def parse(self, response):
        # page = response.url.split("/")[-1]
        filename = 'gcloud.csv'
        companies = response.selector.xpath('//div[@class="search-result"]//p[1]/text()').extract()
        offerings = response.selector.xpath('//div[@class="search-result"]/h2[@class="search-result-title"]/a/text()').extract()
        descriptions = response.selector.xpath('//div[@class="search-result"]//p[2]/text()').extract()
        categories = response.selector.xpath('//div[@class="search-result"]/ul[@aria-label="tags"]//li[1]/text()').extract()
        gclouds = response.selector.xpath('//div[@class="search-result"]/ul[@aria-label="tags"]//li[2]/text()').extract()
        entry = ''
        for y in range(0,len(companies)):
            entry = entry + companies[y].strip().replace('\n',' ').replace('\r','') + '|' + offerings[y].strip().replace('\n',' ').replace('\r','') + '|' + descriptions[y].strip().replace('\n',' ').replace('\r','').replace('|','') + '|' + categories[y].strip().replace('\n',' ').replace('\r','')  + '|' + gclouds [y].strip().replace('\n',' ').replace('\r','') + '\n'

        with open(filename, 'a') as f:
            f.write(entry.encode('utf-8'))
        self.log('Saved file %s' % filename)
