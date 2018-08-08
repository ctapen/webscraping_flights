# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TripadvisorItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    record_nbr = scrapy.Field()
    alliance = scrapy.Field()
    airline_name = scrapy.Field()
    airline_stars = scrapy.Field()
    airline_nbr_reviews = scrapy.Field()
    airline_stars_legroom = scrapy.Field()
    airline_stars_customer_service = scrapy.Field()
    airline_stars_cleanliness = scrapy.Field()
    airline_stars_food_beverage = scrapy.Field()
    airline_stars_seat_comfort = scrapy.Field()
    airline_stars_value_for_money = scrapy.Field()
    airline_stars_checkin_and_boarding = scrapy.Field()
    airline_stars_inflight_entertain = scrapy.Field()

    reviewer_name = scrapy.Field()
    reviewer_city = scrapy.Field()
    reviewer_country = scrapy.Field()
    reviewer_city = scrapy.Field()
    reviewer_level = scrapy.Field()
    reviewer_nbr_reviews = scrapy.Field()
    reviewer_helpful_votes = scrapy.Field()

    review_ID = scrapy.Field()
    review_title = scrapy.Field()
    review_stars = scrapy.Field()
    review_date = scrapy.Field()
    review_text = scrapy.Field()
    review_travel_tip = scrapy.Field()
    #review_stars_legroom = scrapy.Field()
    #review_stars_cust_serv = scrapy.Field()
    #review_stars_cleanliness = scrapy.Field()
    #review_stars_food_beverage = scrapy.Field()
    #review_stars_seat_comfort = scrapy.Field()
    #review_stars_value_for_money = scrapy.Field()
    #review_stars_checkin_and_boarding = scrapy.Field()
    #review_stars_inflight_entertain = scrapy.Field()
    review_domestic_intl = scrapy.Field()
    review_cabin_class = scrapy.Field()
    review_origin = scrapy.Field()
    review_destination = scrapy.Field()
    review_via_mobile = scrapy.Field()
    review_helpful_votes = scrapy.Field()

