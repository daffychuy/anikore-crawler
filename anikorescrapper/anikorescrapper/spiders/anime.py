import scrapy
from scrapy.http import Request
from datetime import datetime

class anime(scrapy.Spider):
    name = 'anime'
    allowed_domains = ['anikore.jp']
    start_urls = ['https://www.anikore.jp/anime/1/']

    def __init__(self):
        self.num = 1
        self.upper_limit = 13000
        self.base_url = 'https://www.anikore.jp/anime/'
        # self.uri = self.base_url + str(self.num) + '/'

    def parse(self, response):
        if self.num == self.upper_limit:
            pass
        else:

            # Process site data
            anime_id = self.num
            anime_name = response.css("html body#page-top section.l-animeDetailHeader div.l-wrapper h1 ::text").extract_first().strip()[1:-1]
            anime_story_title = response.css("html body#page-top section.l-wrapper.l-animeDetailStory h2 ::text").extract_first().strip()
            anime_story = response.css("html body#page-top section.l-wrapper.l-animeDetailStory blockquote ::text").extract_first().strip()
            anime_type = response.css("html body#page-top section.l-wrapper.l-animeDetailBasicInfo dl div dd ::text").extract_first().strip()
            anime_broadcastedyear = response.css("html body#page-top section.l-wrapper.l-animeDetailBasicInfo dl div dd a ::text").extract_first().strip()
            anime_staff = None
            if response.css("html body#page-top section.l-wrapper.l-animeDetailStaffInfo section.l-animeDetailStaffInfo_box p").extract_first():
                anime_staff = response.css("html body#page-top section.l-wrapper.l-animeDetailStaffInfo section.l-animeDetailStaffInfo_box p ::text").extract_first().strip()
            anime_review_score = response.css("html body#page-top section.l-animeDetailHeader div.l-wrapper div.l-animeDetailHeader_pointAndButtonBlock div.l-animeDetailHeader_pointAndButtonBlock_starBlock strong ::text").extract_first().strip()
            anime_review_num = response.css("html body#page-top section.l-animeDetailHeader div.l-wrapper div.l-animeDetailHeader_pointAndButtonBlock div.l-animeDetailHeader_pointAndButtonBlock_starBlock span.l-animeDetailHeader_pointAndButtonBlock_starBlock_count a ::text").extract_first().strip()

            updated = datetime.today().strftime('%Y-%m-%d')

            self.num += 1
            if anime_name:
                yield {"anime_id": anime_id, "name_jp": anime_name, "title_jp": anime_story_title, "des_jp": anime_story,
                       "type_jp": anime_type, "score": anime_review_score, "staffs_jp": anime_staff,
                       "date_jp": anime_broadcastedyear, "date_updated": updated, "reviewed_num": anime_review_num}

                next_url = self.base_url + str(self.num) + '/'
                yield Request(next_url, callback=self.parse, dont_filter=True)
            else:
                next_url = self.base_url + str(self.num) + '/'
                yield Request(next_url, callback=self.parse, dont_filter=True)