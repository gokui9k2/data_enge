import scrapy
from scrapy.crawler import CrawlerProcess
from datetime import datetime
from geopy.geocoders import Nominatim
import pymongo

class DCSpider(scrapy.Spider):
    name = 'dc_spider'

    def __init__(self, *args, **kwargs):
        super(DCSpider, self).__init__(*args, **kwargs)
        self.ufc_stats_htmls = []
        self.items_ = {}
        self.link_uf = []
        self.mongo_client = pymongo.MongoClient("mongodb://mongodb:27017/")
        self.db = self.mongo_client["ufc_database"]
        self.collection_ufc_fight = self.db["ufc_fight"]

    def start_requests(self):
        urls = ["http://ufcstats.com/statistics/events/completed?page=all"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_events)

    def parse_events(self, response):
        fighter_links = response.css("tr.b-statistics__table-row td.b-statistics__table-col a::attr(href)").getall()
        for url in fighter_links:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        fighter_links = response.css('tr.b-fight-details__table-row.b-fight-details__table-row__hover.js-fight-details-click p.b-fight-details__table-text a.b-flag.b-flag_style_green::attr(href)').getall()
        self.link_uf = fighter_links
        date = response.css('li:contains("Date:")::text').getall()
        location = response.css('li:contains("Location:")::text').getall()
        date.pop(0)
        location.pop(0)
        for url in fighter_links:
            yield scrapy.Request(url=url, callback=self.parse_fight, meta={'date': date, 'location': location})

    def parse_fight(self, response):
        items = {
            "R_figther": response.css("div.b-fight-details__person:nth-of-type(1) h3.b-fight-details__person-name a.b-link.b-fight-details__person-link::text").getall(),
        "B_figther": response.css("div.b-fight-details__person:nth-of-type(2) h3.b-fight-details__person-name a.b-link.b-fight-details__person-link::text").getall(),
        "R_figther_W_or_L": response.xpath('//div[@class="b-fight-details__person"][1]//i[contains(@class, "b-fight-details__person-status_style_")]/text()').getall(),
        "B_figther_W_or_L": response.xpath('//div[@class="b-fight-details__person"][2]//i[contains(@class, "b-fight-details__person-status_style_")]/text()').getall(),
        "R_KD": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(2)  tr.b-fight-details__table-row:nth-of-type(1) td.b-fight-details__table-col:nth-of-type(2) p.b-fight-details__table-text:nth-of-type(1)::text").getall(),
        "B_KD": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(2)  tr.b-fight-details__table-row:nth-of-type(1) td.b-fight-details__table-col:nth-of-type(2) p.b-fight-details__table-text:nth-of-type(2)::text").getall(),
        "R_SIG_STR" : response.css("section.b-fight-details__section.js-fight-section:nth-of-type(2)  tr.b-fight-details__table-row:nth-of-type(1) td.b-fight-details__table-col:nth-of-type(3) p.b-fight-details__table-text:nth-of-type(1)::text").getall(),
        "B_SIG_STR": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(2)  tr.b-fight-details__table-row:nth-of-type(1) td.b-fight-details__table-col:nth-of-type(3) p.b-fight-details__table-text:nth-of-type(2)::text").getall(),
        "R_SIG_STR_%" : response.css("section.b-fight-details__section.js-fight-section:nth-of-type(2)  tr.b-fight-details__table-row:nth-of-type(1) td.b-fight-details__table-col:nth-of-type(4) p.b-fight-details__table-text:nth-of-type(1)::text").getall(),
        "B_SIG_STR_%": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(2)  tr.b-fight-details__table-row:nth-of-type(1) td.b-fight-details__table-col:nth-of-type(4) p.b-fight-details__table-text:nth-of-type(2)::text").getall(),
        "R_Total_STR" : response.css("section.b-fight-details__section.js-fight-section:nth-of-type(2)  tr.b-fight-details__table-row:nth-of-type(1) td.b-fight-details__table-col:nth-of-type(5) p.b-fight-details__table-text:nth-of-type(1)::text").getall(),
        "B_Total_STR": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(2)  tr.b-fight-details__table-row:nth-of-type(1) td.b-fight-details__table-col:nth-of-type(5) p.b-fight-details__table-text:nth-of-type(2)::text").getall(),
        "R_TD" : response.css("section.b-fight-details__section.js-fight-section:nth-of-type(2)  tr.b-fight-details__table-row:nth-of-type(1) td.b-fight-details__table-col:nth-of-type(6) p.b-fight-details__table-text:nth-of-type(1)::text").getall(),
        "B_TD": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(2)  tr.b-fight-details__table-row:nth-of-type(1) td.b-fight-details__table-col:nth-of-type(6) p.b-fight-details__table-text:nth-of-type(2)::text").getall(),
        "R_TD_%" : response.css("section.b-fight-details__section.js-fight-section:nth-of-type(2)  tr.b-fight-details__table-row:nth-of-type(1) td.b-fight-details__table-col:nth-of-type(7) p.b-fight-details__table-text:nth-of-type(1)::text").getall(),
        "B_TD_%": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(2)  tr.b-fight-details__table-row:nth-of-type(1) td.b-fight-details__table-col:nth-of-type(7) p.b-fight-details__table-text:nth-of-type(2)::text").getall(),
        "R_SUB_ATT" : response.css("section.b-fight-details__section.js-fight-section:nth-of-type(2)  tr.b-fight-details__table-row:nth-of-type(1) td.b-fight-details__table-col:nth-of-type(8) p.b-fight-details__table-text:nth-of-type(1)::text").getall(),
        "B_SUB_ATT": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(2)  tr.b-fight-details__table-row:nth-of-type(1) td.b-fight-details__table-col:nth-of-type(8) p.b-fight-details__table-text:nth-of-type(2)::text").getall(),
        "R_REV" : response.css("section.b-fight-details__section.js-fight-section:nth-of-type(2)  tr.b-fight-details__table-row:nth-of-type(1) td.b-fight-details__table-col:nth-of-type(9) p.b-fight-details__table-text:nth-of-type(1)::text").getall(),
        "B_REV": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(2)  tr.b-fight-details__table-row:nth-of-type(1) td.b-fight-details__table-col:nth-of-type(9) p.b-fight-details__table-text:nth-of-type(2)::text").getall(),
        "R_CTRL_TIME" : response.css("section.b-fight-details__section.js-fight-section:nth-of-type(2)  tr.b-fight-details__table-row:nth-of-type(1) td.b-fight-details__table-col:nth-of-type(10) p.b-fight-details__table-text:nth-of-type(1)::text").getall(),
        "B_CTRL_TIME": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(2)  tr.b-fight-details__table-row:nth-of-type(1) td.b-fight-details__table-col:nth-of-type(10) p.b-fight-details__table-text:nth-of-type(2)::text").getall(),
        "R_STR_HEAD": response.xpath("//section/div/div/table/tbody/tr/td[4]/p[1]/text()").getall(),
        "B_STR_HEAD": response.xpath("//section/div/div/table/tbody/tr/td[4]/p[2]/text()").getall(),
        "R_STR_BODY": response.xpath("//section/div/div/table/tbody/tr/td[5]/p[1]/text()").getall(),
        "B_STR_BODY": response.xpath("//section/div/div/table/tbody/tr/td[5]/p[2]/text()").getall(),
        "R_STR_LEG": response.xpath("//section/div/div/table/tbody/tr/td[6]/p[1]/text()").getall(),
        "B_STR_LEG": response.xpath("//section/div/div/table/tbody/tr/td[6]/p[2]/text()").getall(),
        "R_DISTANCE": response.xpath("//section/div/div/table/tbody/tr/td[7]/p[1]/text()").getall(),
        "B_DISTANCE": response.xpath("//section/div/div/table/tbody/tr/td[7]/p[2]/text()").getall(),
        "R_CLINCH": response.xpath("//section/div/div/table/tbody/tr/td[8]/p[1]/text()").getall(),
        "B_CLINCH": response.xpath("//section/div/div/table/tbody/tr/td[8]/p[2]/text()").getall(),
        "R_GROUND": response.xpath("//section/div/div/table/tbody/tr/td[9]/p[1]/text()").getall(),
        "B_GROUND": response.xpath("//section/div/div/table/tbody/tr/td[9]/p[2]/text()").getall(),
        "R_SIG_STR_R1": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(5) tr.b-fight-details__table-row:nth-of-type(1) td.b-fight-details__table-col:nth-of-type(2) p.b-fight-details__table-text:nth-of-type(1)::text").getall(),
        "B_SIG_STR_R1": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(5) tr.b-fight-details__table-row:nth-of-type(1) td.b-fight-details__table-col:nth-of-type(2) p.b-fight-details__table-text:nth-of-type(2)::text").getall(),
        "R_SIG_STR_R1_%": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(5) tr.b-fight-details__table-row:nth-of-type(1) td.b-fight-details__table-col:nth-of-type(3) p.b-fight-details__table-text:nth-of-type(1)::text").getall(),
        "B_SIG_STR_R1_%": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(5) tr.b-fight-details__table-row:nth-of-type(1) td.b-fight-details__table-col:nth-of-type(3) p.b-fight-details__table-text:nth-of-type(2)::text").getall(),
        "R_HEAD_R1": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(5) tr.b-fight-details__table-row:nth-of-type(1) td.b-fight-details__table-col:nth-of-type(4) p.b-fight-details__table-text:nth-of-type(1)::text").getall(),
        "B_HEAD_R1": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(5) tr.b-fight-details__table-row:nth-of-type(1) td.b-fight-details__table-col:nth-of-type(4) p.b-fight-details__table-text:nth-of-type(2)::text").getall(),
        "R_BODY_R1": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(5) tr.b-fight-details__table-row:nth-of-type(1) td.b-fight-details__table-col:nth-of-type(5) p.b-fight-details__table-text:nth-of-type(1)::text").getall(),
        "B_BODY_R1": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(5) tr.b-fight-details__table-row:nth-of-type(1) td.b-fight-details__table-col:nth-of-type(5) p.b-fight-details__table-text:nth-of-type(2)::text").getall(),
        "R_LEG_R1": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(5) tr.b-fight-details__table-row:nth-of-type(1) td.b-fight-details__table-col:nth-of-type(6) p.b-fight-details__table-text:nth-of-type(1)::text").getall(),
        "B_LEG_R1": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(5) tr.b-fight-details__table-row:nth-of-type(1) td.b-fight-details__table-col:nth-of-type(6) p.b-fight-details__table-text:nth-of-type(2)::text").getall(),
        "R_DISTANCE_R1": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(5) tr.b-fight-details__table-row:nth-of-type(1) td.b-fight-details__table-col:nth-of-type(7) p.b-fight-details__table-text:nth-of-type(1)::text").getall(),
        "B_DISTANCE_R1": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(5) tr.b-fight-details__table-row:nth-of-type(1) td.b-fight-details__table-col:nth-of-type(7) p.b-fight-details__table-text:nth-of-type(2)::text").getall(),
        "R_CLINCH_R1": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(5) tr.b-fight-details__table-row:nth-of-type(1) td.b-fight-details__table-col:nth-of-type(8) p.b-fight-details__table-text:nth-of-type(1)::text").getall(),
        "B_CLINCH_R1": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(5) tr.b-fight-details__table-row:nth-of-type(1) td.b-fight-details__table-col:nth-of-type(8) p.b-fight-details__table-text:nth-of-type(2)::text").getall(),
        "R_GROUND_R1": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(5) tr.b-fight-details__table-row:nth-of-type(1) td.b-fight-details__table-col:nth-of-type(9) p.b-fight-details__table-text:nth-of-type(1)::text").getall(),
        "B_GROUND_R1": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(5) tr.b-fight-details__table-row:nth-of-type(1) td.b-fight-details__table-col:nth-of-type(9) p.b-fight-details__table-text:nth-of-type(2)::text").getall(),
        "R_SIG_STR_R2": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(5) tr.b-fight-details__table-row:nth-of-type(2) td.b-fight-details__table-col:nth-of-type(2) p.b-fight-details__table-text:nth-of-type(1)::text").getall(),
        "B_SIG_STR_R2": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(5) tr.b-fight-details__table-row:nth-of-type(2) td.b-fight-details__table-col:nth-of-type(2) p.b-fight-details__table-text:nth-of-type(2)::text").getall(),
        "R_SIG_STR_R2_%": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(5) tr.b-fight-details__table-row:nth-of-type(2) td.b-fight-details__table-col:nth-of-type(3) p.b-fight-details__table-text:nth-of-type(1)::text").getall(),
        "B_SIG_STR_R2_%": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(5) tr.b-fight-details__table-row:nth-of-type(2) td.b-fight-details__table-col:nth-of-type(3) p.b-fight-details__table-text:nth-of-type(2)::text").getall(),
        "R_HEAD_R2": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(5) tr.b-fight-details__table-row:nth-of-type(2) td.b-fight-details__table-col:nth-of-type(4) p.b-fight-details__table-text:nth-of-type(1)::text").getall(),
        "B_HEAD_R2": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(5) tr.b-fight-details__table-row:nth-of-type(2) td.b-fight-details__table-col:nth-of-type(4) p.b-fight-details__table-text:nth-of-type(2)::text").getall(),
        "R_BODY_R2": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(5) tr.b-fight-details__table-row:nth-of-type(2) td.b-fight-details__table-col:nth-of-type(5) p.b-fight-details__table-text:nth-of-type(1)::text").getall(),
        "B_BODY_R2": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(5) tr.b-fight-details__table-row:nth-of-type(2) td.b-fight-details__table-col:nth-of-type(5) p.b-fight-details__table-text:nth-of-type(2)::text").getall(),
        "R_LEG_R2": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(5) tr.b-fight-details__table-row:nth-of-type(2) td.b-fight-details__table-col:nth-of-type(6) p.b-fight-details__table-text:nth-of-type(1)::text").getall(),
        "B_LEG_R2": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(5) tr.b-fight-details__table-row:nth-of-type(2) td.b-fight-details__table-col:nth-of-type(6) p.b-fight-details__table-text:nth-of-type(2)::text").getall(),
        "R_DISTANCE_R2": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(5) tr.b-fight-details__table-row:nth-of-type(2) td.b-fight-details__table-col:nth-of-type(7) p.b-fight-details__table-text:nth-of-type(1)::text").getall(),
        "B_DISTANCE_R2": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(5) tr.b-fight-details__table-row:nth-of-type(2) td.b-fight-details__table-col:nth-of-type(7) p.b-fight-details__table-text:nth-of-type(2)::text").getall(),
        "R_CLINCH_R2": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(5) tr.b-fight-details__table-row:nth-of-type(2) td.b-fight-details__table-col:nth-of-type(8) p.b-fight-details__table-text:nth-of-type(1)::text").getall(),
        "B_CLINCH_R2": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(5) tr.b-fight-details__table-row:nth-of-type(2) td.b-fight-details__table-col:nth-of-type(8) p.b-fight-details__table-text:nth-of-type(2)::text").getall(),
        "R_GROUND_R2": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(5) tr.b-fight-details__table-row:nth-of-type(2) td.b-fight-details__table-col:nth-of-type(9) p.b-fight-details__table-text:nth-of-type(1)::text").getall(),
        "B_GROUND_R2": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(5) tr.b-fight-details__table-row:nth-of-type(2) td.b-fight-details__table-col:nth-of-type(9) p.b-fight-details__table-text:nth-of-type(2)::text").getall(),
        "R_SIG_STR_R3": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(5) tr.b-fight-details__table-row:nth-of-type(3) td.b-fight-details__table-col:nth-of-type(2) p.b-fight-details__table-text:nth-of-type(1)::text").getall(),
        "B_SIG_STR_R3": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(5) tr.b-fight-details__table-row:nth-of-type(3) td.b-fight-details__table-col:nth-of-type(2) p.b-fight-details__table-text:nth-of-type(2)::text").getall(),
        "R_SIG_STR_R3_%": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(5) tr.b-fight-details__table-row:nth-of-type(3) td.b-fight-details__table-col:nth-of-type(3) p.b-fight-details__table-text:nth-of-type(1)::text").getall(),
        "B_SIG_STR_R3_%": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(5) tr.b-fight-details__table-row:nth-of-type(3) td.b-fight-details__table-col:nth-of-type(3) p.b-fight-details__table-text:nth-of-type(2)::text").getall(),
        "R_HEAD_R3": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(5) tr.b-fight-details__table-row:nth-of-type(3) td.b-fight-details__table-col:nth-of-type(4) p.b-fight-details__table-text:nth-of-type(1)::text").getall(),
        "B_HEAD_R3": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(5) tr.b-fight-details__table-row:nth-of-type(3) td.b-fight-details__table-col:nth-of-type(4) p.b-fight-details__table-text:nth-of-type(2)::text").getall(),
        "R_BODY_R3": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(5) tr.b-fight-details__table-row:nth-of-type(3) td.b-fight-details__table-col:nth-of-type(5) p.b-fight-details__table-text:nth-of-type(1)::text").getall(),
        "B_BODY_R3": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(5) tr.b-fight-details__table-row:nth-of-type(3) td.b-fight-details__table-col:nth-of-type(5) p.b-fight-details__table-text:nth-of-type(2)::text").getall(),
        "R_LEG_R3": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(5) tr.b-fight-details__table-row:nth-of-type(3) td.b-fight-details__table-col:nth-of-type(6) p.b-fight-details__table-text:nth-of-type(1)::text").getall(),
        "B_LEG_R3": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(5) tr.b-fight-details__table-row:nth-of-type(3) td.b-fight-details__table-col:nth-of-type(6) p.b-fight-details__table-text:nth-of-type(2)::text").getall(),
        "R_DISTANCE_R3": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(5) tr.b-fight-details__table-row:nth-of-type(3) td.b-fight-details__table-col:nth-of-type(7) p.b-fight-details__table-text:nth-of-type(1)::text").getall(),
        "B_DISTANCE_R3": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(5) tr.b-fight-details__table-row:nth-of-type(3) td.b-fight-details__table-col:nth-of-type(7) p.b-fight-details__table-text:nth-of-type(2)::text").getall(),
        "R_CLINCH_R3": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(5) tr.b-fight-details__table-row:nth-of-type(3) td.b-fight-details__table-col:nth-of-type(8) p.b-fight-details__table-text:nth-of-type(1)::text").getall(),
        "B_CLINCH_R3": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(5) tr.b-fight-details__table-row:nth-of-type(3) td.b-fight-details__table-col:nth-of-type(8) p.b-fight-details__table-text:nth-of-type(2)::text").getall(),
        "R_GROUND_R3": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(5) tr.b-fight-details__table-row:nth-of-type(3) td.b-fight-details__table-col:nth-of-type(9) p.b-fight-details__table-text:nth-of-type(1)::text").getall(),
        "B_GROUND_R3": response.css("section.b-fight-details__section.js-fight-section:nth-of-type(5) tr.b-fight-details__table-row:nth-of-type(3) td.b-fight-details__table-col:nth-of-type(9) p.b-fight-details__table-text:nth-of-type(2)::text").getall(),
        "R_SIG_STR_R4": response.css("section:nth-of-type(5) tr:nth-of-type(4) td:nth-of-type(2) p:nth-of-type(1)::text").getall(),
        "B_SIG_STR_R4": response.css("section:nth-of-type(5) tr:nth-of-type(4) td:nth-of-type(2) p:nth-of-type(2)::text").getall(),
        "R_SIG_STR_R4_%": response.css("section:nth-of-type(5) tr:nth-of-type(4) td:nth-of-type(3) p:nth-of-type(1)::text").getall(),
        "B_SIG_STR_R4_%": response.css("section:nth-of-type(5) tr:nth-of-type(4) td:nth-of-type(3) p:nth-of-type(2)::text").getall(),
        "R_HEAD_R4": response.css("section:nth-of-type(5) tr:nth-of-type(4) td:nth-of-type(4) p:nth-of-type(1)::text").getall(),
        "B_HEAD_R4": response.css("section:nth-of-type(5) tr:nth-of-type(4) td:nth-of-type(4) p:nth-of-type(2)::text").getall(),
        "R_BODY_R4": response.css("section:nth-of-type(5) tr:nth-of-type(4) td:nth-of-type(5) p:nth-of-type(1)::text").getall(),
        "B_BODY_R4": response.css("section:nth-of-type(5) tr:nth-of-type(4) td:nth-of-type(5) p:nth-of-type(2)::text").getall(),
        "R_LEG_R4": response.css("section:nth-of-type(5) tr:nth-of-type(4) td:nth-of-type(6) p:nth-of-type(1)::text").getall(),
        "B_LEG_R4": response.css("section:nth-of-type(5) tr:nth-of-type(4) td:nth-of-type(6) p:nth-of-type(2)::text").getall(),
        "R_DISTANCE_R4": response.css("section:nth-of-type(5) tr:nth-of-type(4) td:nth-of-type(7) p:nth-of-type(1)::text").getall(),
        "B_DISTANCE_R4": response.css("section:nth-of-type(5) tr:nth-of-type(4) td:nth-of-type(7) p:nth-of-type(2)::text").getall(),
        "R_CLINCH_R4": response.css("section:nth-of-type(5) tr:nth-of-type(4) td:nth-of-type(8) p:nth-of-type(1)::text").getall(),
        "B_CLINCH_R4": response.css("section:nth-of-type(5) tr:nth-of-type(4) td:nth-of-type(8) p:nth-of-type(2)::text").getall(),
        "R_GROUND_R4": response.css("section:nth-of-type(5) tr:nth-of-type(4) td:nth-of-type(9) p:nth-of-type(1)::text").getall(),
        "B_GROUND_R4": response.css("section:nth-of-type(5) tr:nth-of-type(4) td:nth-of-type(9) p:nth-of-type(2)::text").getall(),
        "R_SIG_STR_R5": response.css("section:nth-of-type(5) tr:nth-of-type(5) td:nth-of-type(2) p:nth-of-type(1)::text").getall(),
        "B_SIG_STR_R5": response.css("section:nth-of-type(5) tr:nth-of-type(5) td:nth-of-type(2) p:nth-of-type(2)::text").getall(),
        "R_SIG_STR_R5_%": response.css("section:nth-of-type(5) tr:nth-of-type(5) td:nth-of-type(3) p:nth-of-type(1)::text").getall(),
        "B_SIG_STR_R5_%": response.css("section:nth-of-type(5) tr:nth-of-type(5) td:nth-of-type(3) p:nth-of-type(2)::text").getall(),
        "R_HEAD_R5": response.css("section:nth-of-type(5) tr:nth-of-type(5) td:nth-of-type(4) p:nth-of-type(1)::text").getall(),
        "B_HEAD_R5": response.css("section:nth-of-type(5) tr:nth-of-type(5) td:nth-of-type(4) p:nth-of-type(2)::text").getall(),
        "R_BODY_R5": response.css("section:nth-of-type(5) tr:nth-of-type(5) td:nth-of-type(5) p:nth-of-type(1)::text").getall(),
        "B_BODY_R5": response.css("section:nth-of-type(5) tr:nth-of-type(5) td:nth-of-type(5) p:nth-of-type(2)::text").getall(),
        "R_LEG_R5": response.css("section:nth-of-type(5) tr:nth-of-type(5) td:nth-of-type(6) p:nth-of-type(1)::text").getall(),
        "B_LEG_R5": response.css("section:nth-of-type(5) tr:nth-of-type(5) td:nth-of-type(6) p:nth-of-type(2)::text").getall(),
        "R_DISTANCE_R5": response.css("section:nth-of-type(5) tr:nth-of-type(5) td:nth-of-type(7) p:nth-of-type(1)::text").getall(),
        "B_DISTANCE_R5": response.css("section:nth-of-type(5) tr:nth-of-type(5) td:nth-of-type(7) p:nth-of-type(2)::text").getall(),
        "R_CLINCH_R5": response.css("section:nth-of-type(5) tr:nth-of-type(5) td:nth-of-type(8) p:nth-of-type(1)::text").getall(),
        "B_CLINCH_R5": response.css("section:nth-of-type(5) tr:nth-of-type(5) td:nth-of-type(8) p:nth-of-type(2)::text").getall(),
        "R_GROUND_R5": response.css("section:nth-of-type(5) tr:nth-of-type(5) td:nth-of-type(9) p:nth-of-type(1)::text").getall(),
        "B_GROUND_R5": response.css("section:nth-of-type(5) tr:nth-of-type(5) td:nth-of-type(9) p:nth-of-type(2)::text").getall(),
        "R_SIG_STK_HEAD": response.css("div.b-fight-details__charts-col-row.clearfix:nth-of-type(1) i.b-fight-details__charts-num.b-fight-details__charts-num_style_red.b-fight-details__charts-num_pos_left.js-red:nth-of-type(1)::text").getall(),
        "B_SIG_STK_HEAD": response.css("section.b-fight-details__section:nth-of-type(6) div.b-fight-details__charts-col-row.clearfix:nth-of-type(1) i.b-fight-details__charts-num.b-fight-details__charts-num_style_blue.b-fight-details__charts-num_pos_right.js-blue::text").getall(),
        "R_SIG_STK_BODY": response.css("div.b-fight-details__charts-col-row.clearfix:nth-of-type(1) i.b-fight-details__charts-num.b-fight-details__charts-num_style_dark-red.b-fight-details__charts-num_pos_left.js-red:nth-of-type(1)::text").getall(),
        "B_SIG_STK_BODY": response.css("section.b-fight-details__section:nth-of-type(6) div.b-fight-details__charts-col-row.clearfix:nth-of-type(1) i.b-fight-details__charts-num.b-fight-details__charts-num_style_dark-blue.b-fight-details__charts-num_pos_right.js-blue::text").getall(),
        "R_SIG_STK_LEG": response.css("section.b-fight-details__section:nth-of-type(6) div.b-fight-details__charts-col-row.clearfix:nth-of-type(1) i.b-fight-details__charts-num.b-fight-details__charts-num_style_light-red.b-fight-details__charts-num_pos_left.js-red::text").getall(),
        "B_SIG_STK_LEG": response.css("div.b-fight-details__charts-col-row.clearfix:nth-of-type(1) i.b-fight-details__charts-num.b-fight-details__charts-num_style_dark-blue.b-fight-details__charts-num_pos_right.js-blue:nth-of-type(3)::text").getall(),
        "R_SIG_POS_DIS": response.css("div.b-fight-details__charts-col-row.clearfix:nth-of-type(2) i.b-fight-details__charts-num.b-fight-details__charts-num_style_red.b-fight-details__charts-num_pos_left.js-red:nth-of-type(1)::text").getall(),
        "B_SIG_POS_DIS": response.css("section.b-fight-details__section:nth-of-type(6) div.b-fight-details__charts-col-row.clearfix:nth-of-type(2) i.b-fight-details__charts-num.b-fight-details__charts-num_style_blue.b-fight-details__charts-num_pos_right.js-blue::text").getall(),
        "R_SIG_POS_CLIN": response.css("div.b-fight-details__charts-col-row.clearfix:nth-of-type(2) i.b-fight-details__charts-num.b-fight-details__charts-num_style_dark-red.b-fight-details__charts-num_pos_left.js-red:nth-of-type(1)::text").getall(),
        "B_SIG_POS_CLIN": response.css("section.b-fight-details__section:nth-of-type(6) div.b-fight-details__charts-col-row.clearfix:nth-of-type(2) i.b-fight-details__charts-num.b-fight-details__charts-num_style_dark-blue.b-fight-details__charts-num_pos_right.js-blue::text").getall(),
        "R_SIG_POS_GROUND": response.css("section.b-fight-details__section:nth-of-type(6) div.b-fight-details__charts-col-row.clearfix:nth-of-type(2) i.b-fight-details__charts-num.b-fight-details__charts-num_style_light-red.b-fight-details__charts-num_pos_left.js-red::text").getall(),
        "B_SIG_POS_GROUND": response.css("div.b-fight-details__charts-col-row.clearfix:nth-of-type(2) i.b-fight-details__charts-num.b-fight-details__charts-num_style_dark-blue.b-fight-details__charts-num_pos_right.js-blue:nth-of-type(3)::text").getall(),
        "METHOD" : response.css("section.b-statistics__section_details div.b-fight-details__fight p.b-fight-details__text:nth-of-type(1) i.b-fight-details__text-item_first i:nth-of-type(2)::text").getall(),
        "METHOD_DETAILS" :response.css("section.b-statistics__section_details div.b-fight-details__fight p.b-fight-details__text:nth-of-type(2)::text").getall(),
        "ROUND" : response.css("section.b-statistics__section_details div.b-fight-details__fight p.b-fight-details__text:nth-of-type(1) i.b-fight-details__text-item:nth-of-type(2)::text").getall(),
        "TIME" : response.css("section.b-statistics__section_details div.b-fight-details__fight p.b-fight-details__text:nth-of-type(1) i.b-fight-details__text-item:nth-of-type(3)::text").getall(),
        "FORMAT" : response.xpath("//section[1]/div[1]/div/div[2]/div[2]/p[1]/i[4]/text()").getall(),
        "CLASS"  : response.css("section div.b-fight-details__fight-head i::text").getall(),
        "Date": response.meta['date'],
        "Location": response.meta['location']
        }
        keys_to_pop = ["METHOD_DETAILS", "ROUND", "TIME", "FORMAT"]
        for key in keys_to_pop:
            if key in items and items[key]:
                items[key].pop(0)

        for key, value in items.items():
            if value:
                value[0] = value[0].strip()
                if "%" in value[0]:
                    value[0] = int(value[0].replace("%", "")) / 100
                if issubclass(type(value[0]), str) and "of" in value[0]:
                    split_value = value[0].split()
                    value[0] = int(split_value[0])
                if "CLASS" in key and value[0] == "":
                    value.pop(0)
                    if value:
                        value[0] = value[0].strip()
            else:
                value.append("Knockout")
            print(f"Contents of {key}: {value}")

        self.collection_ufc_fight.insert_many([items])

        yield items

if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(DCSpider)
    process.start()