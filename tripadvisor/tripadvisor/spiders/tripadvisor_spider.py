## Tripadvisor spider

## Import Statements
from scrapy import Spider, Request
from tripadvisor.items import TripadvisorItem
from scrapy.utils.markup import remove_tags
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import re

## Inputs
specified_year = '2018'

## URL maker
# List of Airlines with >10k reviews on tripadvisor (TA)
airline_list = [# Airlines with >10k reviews on tripadvisor
                #Fields: ['airline_name', 'url_nbr', 'nbr_pages_scrape', 'country', 'airline_counter', 'alliance']
                ['Air Canada', 8728998, 1, 'Canada',1,'Star Alliance'], 
                ['United Airlines', 8729177, 860, 'United States',2,'Star Alliance'], 
                ['American Airlines', 8729020, 1175, 'United States',3,'OneWorld'], 
                ['Delta Air Lines', 8729060, 995, 'United States',4,'Skyteam'],
                ['Southwest Airlines',8729156,895, 'United States',5,''],
                ['Ryanair', 8729141, 1, 'Ireland',6,''],
                ['Transavia',8729171,1, 'Netherlands',7,''], # KLM's Budget
                ['Emirates',8729069,1, 'United Arab Emirates',8,''],
                ['British Airways',8729039,1, 'England',9,'OneWorld'],
                ['EasyJet',8729066,1, 'England',10,''], # British Budget
                ['LATAM',10290698,1, 'Chile',11,'OneWorld'],
                ['Lufthansa',8729113,1, 'Germany',12,'Star Alliance'],
                ['Air France',8729003,1, 'France',13,'Skyteam'],
                ['KLM Royal Dutch Airlines',8729104,1, 'Netherlands',14,'Skyteam'],
                ['Qatar Airways',8729134,1, 'Qatar',15,'OneWorld'],
                ['Turkish Airlines',8729174,1, 'Turkey',16,'Star Alliance'],
                ['Vueling Airlines',8729185,1, 'Spain',17,''],
                ['Norwegian',8729125,1, 'Norway',17,''],
                ['Singapore Airlines',8729151,1, 'Singapore',19,'Star Alliance'],
                ['Jet2.com',8729098,1, 'England',20,''],
                ['GOL Airlines',8729083,1, 'Brazil',21,''],
                ['Alitalia',8729018,1, 'Italy',22,'Skyteam'],
                ['Qantas',8729133,1, 'Australia',23,'OneWorld'],
                ['Iberia',8729089,1, 'Spain',24,'OneWorld'],
                ['TAP Portugal',8729164,1, 'Portugal',25,'Star Alliance'],
                ['Azul',8728972,1, 'Brazil',26,''],
                ['Etihad Airways',8729074,1, 'United Arab Emirates',27,''],
                ['JetBlue',8729099,1, 'United States',28,''],
                ['Cathay Pacific',8729046,1, 'China',29,'OneWorld']
               ]
# United end: 860, American end: 1175, Delta end: 995, Southwest end: 895

# Function to make tripadvisor URL from airline nbr, # pages, and name
def url_airline_input(airline_nbr, page_end, airline_name):
    return ['https://www.tripadvisor.com/Airline_Review-d' + str(airline_nbr) + '-Reviews-or' + str(i) + '0-' + str(airline_name).replace(' ', '-') for i in range(page_end)]

# Create a list of urls to scrape
url_list = []
for i in range(len(airline_list)):
    url_list.append(url_airline_input(int(airline_list[i][1]), int(airline_list[i][2]), str(airline_list[i][0])))
    #records_estimator *= int(airline_list[i][2])

# Flatten list
start_url_list = [elem for sublist in url_list for elem in sublist]
#print('Records estimator: ' + str(records_estimator))

## Class for TripadvisorSpider, with parsing
class TripadvisorSpider(Spider):
    name = 'tripadvisor_spider'
    allowed_urls = ['https://www.tripadvisor.com/']
    start_urls = start_url_list
    #start_urls = ['https://www.tripadvisor.com/Airline_Review-d8728998-Reviews-or00-Air-Canada']
    #start_urls = ['https://www.tripadvisor.ca/Airline_Review-d8728998-Reviews-Cheap-Flights-Air-Canada']
    #start_urls = ['https://www.tripadvisor.com/Airline_Review-d8729020-Reviews-or00-American-Airlines#REVIEWS']

    def parse(self, response):
        record_nbr = 0

    	## Get total reviews shown (those in English) and then get nbr. of pages
        total_text = response.xpath('//div[@id="taplc_airline_detail_review_results_description_0"]/form/b').extract()
        total = list(map(lambda x: int(x), re.findall('\d+', total_text[0].replace(',', ''))))[0]
        items_per_page = 10
        pages = total // items_per_page + 1

        ## Get airline information (aggregate)
        airline_name = remove_tags(response.xpath('//*[@id="taplc_airline_detail_header_0"]/div/div/h1/div')\
            .extract()[0]).strip()
        print('=' * 50)
        print(airline_name)

        airline_stars = float(response.xpath('//*[@id="taplc_airline_detail_header_0"]/div/div/div[2]/div/div/span//@class')\
            .extract()[0][-2:])/10

        airline_nbr_reviews = int(response.xpath('//*[@class="numRatings"]//@content').extract()[0])

        airline_stars_legroom = float(response.xpath('//*[@id="AIRLINE_DETAIL_MAIN_WRAPPER"]/div[1]/div/div/div/ul/li[1]/div[1]/div[1]/span//@class')\
            .extract()[0][-2:])/10

        airline_stars_seat_comfort = float(response.xpath('//*[@id="AIRLINE_DETAIL_MAIN_WRAPPER"]/div[1]/div/div/div/ul/li[1]/div[2]/div[1]/span//@class')\
            .extract()[0][-2:])/10

        airline_stars_customer_service = float(response.xpath('//*[@id="AIRLINE_DETAIL_MAIN_WRAPPER"]/div[1]/div/div/div/ul/li[2]/div[1]/div[1]/span//@class')\
            .extract()[0][-2:])/10

        airline_stars_value_for_money = float(response.xpath('//*[@id="AIRLINE_DETAIL_MAIN_WRAPPER"]/div[1]/div/div/div/ul/li[2]/div[2]/div[1]/span//@class')\
            .extract()[0][-2:])/10

        airline_stars_cleanliness = float(response.xpath('//*[@id="AIRLINE_DETAIL_MAIN_WRAPPER"]/div[1]/div/div/div/ul/li[3]/div[1]/div[1]/span//@class')\
            .extract()[0][-2:])/10

        airline_stars_checkin_and_boarding = float(response.xpath('//*[@id="AIRLINE_DETAIL_MAIN_WRAPPER"]/div[1]/div/div/div/ul/li[3]/div[2]/div[1]/span//@class')\
            .extract()[0][-2:])/10

        airline_stars_food_beverage = float(response.xpath('//*[@id="AIRLINE_DETAIL_MAIN_WRAPPER"]/div[1]/div/div/div/ul/li[4]/div[1]/div[1]/span//@class')\
            .extract()[0][-2:])/10

        airline_stars_inflight_entertain = float(response.xpath('//*[@id="AIRLINE_DETAIL_MAIN_WRAPPER"]/div[1]/div/div/div/ul/li[4]/div[2]/div[1]/span//@class')\
            .extract()[0][-2:])/10


        ## Click the more button under review section using Selenium
        #try: 
        #print("attempting")
#        driver = webdriver.Chrome()
        #print("Driver variable: gotten")
#        driver.get("https://www.tripadvisor.ca/Airline_Review-d8728998-Reviews-Cheap-Flights-Air-Canada")
        #print("Driver.get: gotten")
#        more_button = driver.find_element_by_xpath('//span[starts-with(@class, "taLnk hvrIE6")]')
        #print("More button: gotten")
        #ActionChains(browser).move_to_element(more_button).perform()
#        more_button.click()
        #print('Click: gotten')
        #except:
        #    print('-' * 50)
        #    print("WARNING: not able to click more button")

        ## Reviews pulled with Selenium (seem to need selenium variables to come from Selenium)
#        reviews_selenium = driver.find_elements_by_xpath('//div[starts-with(@class, "reviewSelector")]')

        # Reviews
        # ref: https://github.com/mkorogluNYC/NYC_Data_ScienceAcademy/blob/master/Web_scraping_project/tripadvisor/tripadvisor/spiders/tripadvisor_spider.py
        reviews = response.xpath('//div[starts-with(@class, "reviewSelector")]')
        counter_1 = 0

        for review in reviews:           
            # Tripadvisor changed the format of its date html paths
            try:
                review_date = review.xpath('.//span[starts-with(@class, "ratingDate")]/@title').extract()[0]
            except:
                try:
                    review_date = review.xpath('.//span[starts-with(@class, "ratingDate")]/text()').extract_first().replace('\n','')[9:]
                except:
                    pass # without this except/pass it threw error about indending next line

            # Only get data for specified year
            if review_date[-4:] == specified_year:

                print(counter_1)

                ## Reviewer information
                # try/excepts are because not every review has that content
                try:
                    reviewer_name = review.xpath('.//div[@class="username mo"]/span/text()').extract_first().strip()
                except: 
                    reviewer_name = ''
                try:
                    reviewer_nbr_reviews = int(re.findall('\d+',review.xpath('.//span[@class="badgeText"]/text()').extract_first())[0])
                except:
                    reviewer_nbr_reviews = ''
                try:
                    reviewer_city = review.xpath('.//div[@class="location"]/text()').extract_first().replace('\n','').split(',')[0]
                except:
                    reviewer_city = ''
                try:
                    reviewer_country = review.xpath('.//div[@class="location"]/text()').extract_first().replace('\n','').split(',')[1].strip()
                except:
                    reviewer_country = ''
                try:
                    reviewer_level = int(review.xpath('.//span[@class="contribution-count"]/text()').extract_first())
                except:
                    reviewer_level = '' #or perhaps: np.NaN
                try:
                    reviewer_helpful_votes = int(re.findall('\d+',review.xpath('.//div[@class="helpfulVotesBadge badge no_cpu"]/span/text()').extract_first())[0])
                except: 
                    reviewer_helpful_votes = ''

                ## Review information:
                review_ID = int(re.findall('\d+',review.xpath('./@id').extract_first())[0])
                review_title = review.xpath('.//span[@class="noQuotes"]/text()').extract_first()
                #print(review_title)
                review_stars = float(review.xpath('.//div[@class="rating reviewItemInline"]/span/@class').extract_first()[-2:])/10
                review_text = review.xpath('.//div[@class="entry"]/p/text()').extract_first().replace('\n','')
                # ^ revisit: this only gets first part of review, until ...
                # all the more button stuff...
                # add try/except
                #review_seat_comfort = reviews_selenium[counter_1].find_element_by_xpath('.//span/[starts-with(@class, "ui_bubble_rating")]').text
                #review_seat_comfort = reviews_selenium[counter_1].find_element_by_xpath('.//span/[class="ui_bubble_rating bubble_4"]')          
                #...
                review_domestic_intl = review.xpath('.//div[@class="allLabels"]/span[1]/text()').extract_first()
                review_cabin_class = review.xpath('.//div[@class="allLabels"]/span[2]/text()').extract_first()
                review_origin = review.xpath('.//div[@class="allLabels"]/span[3]/text()').extract_first().split('-')[0].strip()
                review_destination = review.xpath('.//div[@class="allLabels"]/span[3]/text()').extract_first().split('-')[1].strip()
                review_via_mobile = review.xpath('.//a[@class="viaMobile"]/@class').extract_first()
                try:
                    review_helpful_votes = review.xpath('.//span[@class="numHlpIn"]/text()').extract()
                except:
                    review_helpful_votes = ''

                ## Return variable information to item to be passed to class/csv
                ## Airline items
                item = TripadvisorItem()
                item['airline_name'] = airline_name
                item['airline_stars'] = airline_stars
                item['airline_nbr_reviews'] = airline_nbr_reviews
                item['airline_stars_legroom'] = airline_stars_legroom
                item['airline_stars_seat_comfort'] = airline_stars_seat_comfort
                item['airline_stars_customer_service'] = airline_stars_customer_service
                item['airline_stars_value_for_money'] = airline_stars_value_for_money
                item['airline_stars_cleanliness'] = airline_stars_cleanliness
                item['airline_stars_checkin_and_boarding'] = airline_stars_checkin_and_boarding
                item['airline_stars_food_beverage'] = airline_stars_food_beverage
                item['airline_stars_inflight_entertain'] = airline_stars_inflight_entertain

                ## Reviewer items
                item['review_ID'] = review_ID
                item['reviewer_name'] = reviewer_name
                item['reviewer_nbr_reviews'] = reviewer_nbr_reviews
                item['reviewer_level'] = reviewer_level
                item['reviewer_helpful_votes'] = reviewer_helpful_votes
                item['reviewer_city'] = reviewer_city
                item['reviewer_country'] = reviewer_country

                ## Review items
                item['review_title'] = review_title
                item['review_stars'] = review_stars
                item['review_date'] = review_date
                item['review_text'] = review_text
                item['review_domestic_intl'] = review_domestic_intl
                item['review_cabin_class'] = review_cabin_class
                item['review_origin'] = review_origin
                item['review_destination'] = review_destination
                item['review_via_mobile'] = review_via_mobile
                item['review_helpful_votes'] = review_helpful_votes
                #item['review_seat_comfort'] = review_seat_comfort

                counter_1 += 1
                record_nbr += 1
                yield item

