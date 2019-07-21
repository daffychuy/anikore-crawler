import scrapy
from scrapy.http import Request

class anime(scrapy.Spider):
    name = 'anime'
    allowed_domains = ['anikore.jp']
    start_urls = ['https://www.anikore.jp/anime/1/']

    def __init__(self):
        self.num = 1
        self.upper_limit = 13000
        self.base_url = 'https://www.anikore.jp/anime/'

    def parse(self, response):
        if self.num == self.upper_limit:
            pass
        else:
            uri = self.base_url + str(self.num) + '/'

            # Process site data
            anime_id = self.num
            anime_name = response.xpath("/html/body/section[3]/div/h1/text()").extract_first().strip()
            anime_story_title = response.xpath("//*[@id='page-top']/section[5]/h2/text()").extract_first().strip()
            anime_story = response.xpath("//*[@id='page-top']/section[5]/blockquote/text()").extract_first().strip()
            anime_staff = response.xpath("//*[@id='page-top']/section[8]/section[2]/p").extract_first()
            anime_type = response.xpath("//*[@id='page-top']/section[7]/dl/div[1]/dd/text()").extract_first().strip()
            anime_broadcastedyear = response.xpath("//*[@id='page-top']/section[7]/dl/div[2]/dd/a/text()").extract_first().strip()
            anime_review_score = response.xpath("//*[@id='page-top']/section[3]/div/div[2]/div/strong/text()").extract_first().strip()

            self.num += 1
            if anime_name:
                yield {"anime_id": anime_id, "name_jp": anime_name, "title_jp": anime_story_title, "des_jp": anime_story,
                       "type_jp": anime_type, "score": anime_review_score, "staffs_jp": anime_staff, "date_jp": anime_broadcastedyear}

                next_url = self.base_url + str(self.num) + '/'
                yield Request(next_url, callback=self.parse, dont_filter=True)
            else:
                next_url = self.base_url + str(self.num) + '/'
                yield Request(next_url, callback=self.parse, dont_filter=True)