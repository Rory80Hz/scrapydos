import scrapy

class DosOpsSpider(scrapy.Spider):
    name = "dosops"

    def start_requests(self):
        baseurl = 'https://www.digitalmarketplace.service.gov.uk/digital-outcomes-and-specialists/opportunities/'
        for x in range(0,3000):
            yield scrapy.Request(url=baseurl + str(x), callback=self.parse)

    def parse(self, response):
        # page = response.url.split("/")[-1]
        datapoints = ['Organisation the work is for','Published','Deadline for asking questions','Closing date for applications','Summary of the work','Location','Budget range','Current phase','Security clearance']
        filename = 'dosops.csv'
        title = response.css('h1::text').extract_first()
        entry = title
        for datapoint in datapoints:
            path = '//span[text()="' + datapoint + '"]/parent::*/following-sibling::*/span/text()'
            if response.selector.xpath(path).extract_first() is not None:
                entry = entry + '|' + response.selector.xpath(path).extract_first().replace('\n', ' ').replace('\r', '')
            else:
                entry = entry + '|'
        entry = entry + '|' + response.url  + '\n'
        with open(filename, 'a') as f:
            f.write(entry.encode('utf-8'))
        self.log('Saved file %s' % filename)
