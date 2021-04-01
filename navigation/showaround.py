import time
import robot.settings as settings

class Showaround:
    def __init__(self, browser, robot):
        self.browser = browser
        self.robot = robot

    def login(self):
        self.browser.get("https://www.showaround.com/")
        connect_button = self.browser.find_element_by_xpath("//div[@class='Navigation-item Navigation-item--button']/a")
        connect_button.click()

        if not self.browser.element_exists("xpath", "//button[contains(text(),'Connect with your email')]"):
            other_options_button = self.browser.find_element_by_xpath("//button[contains(text(),'Show other options')]")
            other_options_button.click()
            time.sleep(3)
            connect_with_mail_button = self.browser.find_element_by_xpath(
                "/html/body/div[5]/div/div/div[2]/div/div/div/div/div/div[3]/div/div[2]/button")
            connect_with_mail_button.click()
            time.sleep(1)
            existing_user_button = self.browser.find_element_by_xpath(
                "/html/body/div[5]/div/div/div[2]/div/div/div[1]/span[1]")
            existing_user_button.click()
            email_box = self.browser.find_element_by_xpath(
                "/html/body/div[5]/div/div/div[2]/div/div/div[2]/form/input[1]")
            email_box.click()
            email_box.send_keys(settings.LOGIN_MAIL)
            password_box = self.browser.find_element_by_xpath(
                "//html/body/div[5]/div/div/div[2]/div/div/div[2]/form/input[2]")
            password_box.click()
            password_box.send_keys(settings.LOGIN_PASSWORD)
            login_button = self.browser.find_element_by_xpath(
                "/html/body/div[5]/div/div/div[2]/div/div/div[2]/form/div[4]/button")
            login_button.click()
            time.sleep(3)
            self.browser.find_element_by_xpath("/html/body/div[3]/div/div[2]/button[2]").click()

    def apply(self, city):
        self.browser.get("https://www.showaround.com/settings")
        time.sleep(3)
        location = self.browser.find_element_by_xpath("//*[@id='location']/a")
        location.click()
        time.sleep(1)
        location_box = self.browser.find_element_by_xpath("//*[@id='location']/div/form/input")
        location_box.click()
        location_box.clear()
        self.robot.Log.debug(f"Applying to offers in {city.value['city']}")
        location_box.send_keys(city.value['city'])
        time.sleep(1)
        if self.browser.element_exists('xpath', "/html/body/ul[2]/li[1]"):
            first_location_result = self.browser.find_element_by_xpath("/html/body/ul[2]/li[1]")
            first_location_result.click()
            time.sleep(1)
            save_button = self.browser.find_element_by_xpath("//*[@id='location']/div/form/div[2]/button")
            save_button.click()
            time.sleep(1)

            send_offers_button = self.browser.find_element_by_xpath(
                "/html/body/div[1]/header/sa-navigation/div/div[2]/div/div[2]/a")
            send_offers_button.click()
            time.sleep(3)
            if self.browser.element_exists("xpath", "//button[contains(text(),'View')]"):
                view_all_offers = self.browser.find_element_by_xpath("//button[contains(text(),'View')]")
                view_all_offers.click()
                time.sleep(3)
                send_offers = self.browser.find_elements_by_xpath("//button[contains(text(),'Send Offer')]")
                for offer in send_offers:
                    offer.click()
                    time.sleep(3)
                    send_offer = self.browser.find_element_by_xpath(
                        "//div[@class='SendOfferModal-footer']//button")
                    send_offer.click()
                    time.sleep(1)
                    if self.browser.element_exists("xpath", "//a[contains(text(),'OK, got it')]"):
                        ok_got_it = self.browser.find_element_by_xpath("//a[contains(text(),'OK, got it')]")
                        ok_got_it.click()
