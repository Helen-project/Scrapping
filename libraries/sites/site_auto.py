"""AutoRia site module."""
from datetime import datetime
from libraries.models import Car
from libraries.sites.main_browser import Sites
from libraries import logger


class AutoRia(Sites):
    """AutoRia site class."""

    def __init__(self):
        """Functions initialise the class."""
        super().__init__("https://auto.ria.com/car/used/")
        self.setup_browser()
        self._open_site()

    def _open_site(self):
        """Function to open site AutoRia."""
        logger.info("Open site AutoRia.")
        self.browser.go_to(self.url)
        self.browser.wait_until_element_is_visible('//button[@class="button-primary"]', 15)
        self.browser.click_element('//button[@class="button-primary"]')
        if self.browser.is_element_visible('//div[@class="c-notifier-btns"]//label[@class="js-close c-notifier-btn"]'):
            self.browser.click_element('//div[@class="c-notifier-btns"]//label[@class="js-close c-notifier-btn"]')

    def get_cars_data(self):
        """Functions for getting cars data for site."""
        logger.info(f"Start getting cars data - {datetime.now()}")
        cars_data_list = []
        processed_cars_count = 0
        while True:
            self.browser.wait_until_element_is_visible('//section[contains(@class,"ticket-item")]', 10)
            cars_count = self.browser.get_element_count('//section[contains(@class,"ticket-item")]')
            logger.info(f"Cars count on the page - {cars_count}")
            for index in range(cars_count):
                car_obj = Car()
                try:
                    self.switch_to_auto_page(index)
                    car_obj.url = self.browser.driver.current_url
                    car_obj.title = self.browser.get_text('//h1[@class="head" or contains(@class, "title")]')
                    if self.browser.is_element_visible(
                        '//section[contains(@class,"price")]//descendant::span[@data-currency="USD"]'
                    ):
                        car_obj.currency_check(
                            self.browser.get_text(
                                '//section[contains(@class,"price")]//descendant::span[@data-currency="USD"]'
                            )
                        )
                    elif self.browser.is_element_visible('//div[@class="price_value"]//strong'):
                        car_obj.currency_check(self.browser.get_text('//div[@class="price_value"]//strong'))
                    car_obj.check_and_convert_odometer(
                        self.browser.get_text('//div[@class="base-information bold"]//span')
                    )
                    if self.browser.is_element_visible('//div[@class="seller_info_name bold"]'):
                        car_obj.user_name = self.browser.get_text('//div[@class="seller_info_name bold"]')
                    car_obj.check_phone_number = self.browser.get_text("")
                    car_obj.image_url = self.browser.get_element_attribute(
                        '//*[contains(@class,"photo") and contains(@class,"loaded")]//picture//img', "src"
                    )
                    car_obj.get_image_count(str(self.browser.get_element_count('//div[@photocontainer="photo"]//a')))
                    if self.browser.is_element_visible('//span[@class="state-num ua"]'):
                        car_obj.car_number = self.browser.get_text('//span[@class="state-num ua"]')
                    try:
                        if self.browser.is_element_visible('//span[@class="vin-code"]'):
                            car_obj.car_vin = self.browser.get_text('//span[@class="vin-code"]')
                        else:
                            car_obj.car_vin = self.browser.get_text('//span[@class="label-vin"]')
                    except Exception:
                        car_obj.car_vin = ""
                    cars_data_list.append(car_obj)
                    self.close_and_switch_back()
                except Exception as e:
                    logger.error(f"Unexpected error - {str(e)}. For car - {car_obj.url}")
                    continue
                processed_cars_count += cars_count
            if self.browser.is_element_visible("page-link js-next disabled"):
                break
            else:
                self.browser.scroll_element_into_view(
                    '//div[@id="searchPagination"]//descendant::span[contains(@class,"page-item next")]'
                    '//a[@class="page-link js-next"]'
                )
                self.browser.click_element_when_visible(
                    '//div[@id="searchPagination"]//descendant::span[contains(@class,"page-item next")]'
                    '//a[@class="page-link js-next"]'
                )
        logger.info(f"Finish getting cars data for {processed_cars_count} cars - {datetime.now()}")
        return cars_data_list

    def switch_to_auto_page(self, index):
        """Functions for open new tab in browser and switch to that window."""
        item_url = self.browser.get_element_attribute(
            f'//section[contains(@class,"ticket-item")][{index + 1}]//div[@class="head-ticket"]//a', "href"
        )
        self.browser.execute_javascript("window.open('about:blank','secondtab');")
        self.browser.switch_window(self.browser.get_window_handles()[-1])
        self.browser.go_to(item_url)
        self.browser.wait_until_element_is_visible('//h1[@class="head"]')

    def close_and_switch_back(self):
        """Functions for close tab in browser."""
        self.browser.close_window()
        self.browser.switch_window(self.browser.get_window_handles()[-1])
        self.browser.wait_until_element_is_visible('//section[contains(@class,"ticket-item")]', 10)
