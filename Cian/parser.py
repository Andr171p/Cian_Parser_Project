from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from fake_useragent import UserAgent
from Cian.config import URL
import time
from Cian.project_Lib.ads_datetime import current_date


class CianParser:
    def __init__(self, url, ads_number=10, driver_version="122.0.6261.95"):
        # URL:
        self.url = url
        # web-driver options:
        self.options = webdriver.ChromeOptions()
        # fake-user agent:
        self.User_Agent = UserAgent()
        self.user_agent = UserAgent.random
        # add options:
        self.options.add_argument(f"user-agent={self.user_agent}")
        # Chrome web-driver:
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager(driver_version=driver_version).install()),
                                       options=self.options)
        # init pages of sites:
        self.site_pages = []
        # number of ads:
        self.ads_number = ads_number

    # this method push get requests on the site page:
    def get_requests(self):
        self.driver.get(self.url)
        self.driver.implicitly_wait(10)

    # this method open ads page window:
    def click_ads_window(self, iterator):
        items = self.driver.find_elements(By.CLASS_NAME, "_93444fe79c--link--VtWj6")
        items[iterator].click()
        self.driver.implicitly_wait(10)

        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.implicitly_wait(10)

    # this method return info of ads (--> str):
    def get_sector_info(self, ads):
        info = self.driver.find_elements(By.CLASS_NAME, "a10a3f92e9--title--vlZwT")
        self.driver.implicitly_wait(10)
        ads.append(info[0].text)

    # this method return sale per m^2 of ads (--> int):
    def get_sale(self, ads):
        sale = self.driver.find_elements(By.XPATH, "//div[@data-name='OfferFactItem']")
        ads.append(int(sale[0].text[13:-6].replace(' ', '')))
        self.driver.implicitly_wait(10)

    # this method return area of sector (--> float):
    def get_area(self, ads):
        area = self.driver.find_elements(By.XPATH, "//p[@class='a10a3f92e9--color_black_100--Ephi7 a10a3f92e9--lineHeight_6u--cedXD a10a3f92e9--fontWeight_normal--JEG_c a10a3f92e9--fontSize_16px--QNYmt a10a3f92e9--display_block--KYb25 a10a3f92e9--text--e4SBY a10a3f92e9--text_letterSpacing__0--cQxU5']")
        ads.append(float(area[0].text[:-5].replace(',', '.')))
        self.driver.implicitly_wait(10)

    # this method return location of sector (--> str):
    def get_location(self, ads):
        location = self.driver.find_elements(By.XPATH, "//div[@data-name='AddressContainer']")
        ads.append(location[0].text[:-8].replace(',', ''))
        self.driver.implicitly_wait(10)

    # this method return datetime of ads (--> str):
    def get_datetime(self, ads):
        date_time = self.driver.find_elements(By.XPATH, "//div[@class='a10a3f92e9--added--Xx8oJ']")
        ads.append(current_date(date_time[0].text))
        self.driver.implicitly_wait(10)

    # this method return url of ads page:
    def get_url(self, ads):
        ads.append(self.driver.current_url)

    # this method close window of sector ads:
    def close_window(self):
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        time.sleep(10)

    # this method parse web-site (--> 2D array):
    def get_parse(self):
        try:
            for i in range(10):
                # ads array:
                ads = []
                self.get_requests()
                self.click_ads_window(i)
                self.get_sector_info(ads=ads)
                self.get_sale(ads=ads)
                self.get_area(ads=ads)
                self.get_location(ads=ads)
                self.get_datetime(ads=ads)
                self.get_url(ads=ads)
                self.close_window()
                self.site_pages.append(ads)
        except Exception as _ex:
            print(_ex)
        finally:
            self.driver.close()
            self.driver.quit()

        return self.site_pages


cian = CianParser(url=URL).get_parse()
print(cian)