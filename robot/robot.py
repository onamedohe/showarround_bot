import os
import time
import random
import pandas as pd
from iBott.robot_activities import Robot, RobotException, Robotmethod, get_all_Methods, get_instances, Queue
from iBott.browser_activities import ChromeBrowser
import robot.settings as settings


class Main(Robot):
    def __init__(self, args):
        self.methods = get_all_Methods(self)
        if args is not None:
            self.robotId = args['RobotId']
            self.ExecutionId = args['ExecutionId']
            self.url = args['url']
            self.username = args['username']
            self.password = args['password']
            self.robotParameters = args['params']
            super().__init__(robotId=self.robotId, ExecutionId=self.ExecutionId, url=self.url,
                             username=self.username, password=self.password,
                             params=self.robotParameters)
        else:
            super().__init__()

    @Robotmethod
    def cleanup(self):
        """Clean system before executing the robot"""

        pass

    @Robotmethod
    def start(self):
        """Init variables, instance objects and start the applications you are going to work with"""

        self.browser = ChromeBrowser()
        self.browser.open()
        self.browser.maximize_window()

        # init QueueId

        city_list = pd.read_excel(os.path.join(settings.ROBOT_FOLDER, "city_list.xlsx"), header=0)
        city_list = city_list["Cities"].tolist()
        city_list = random.sample(city_list, len(city_list))

        self.queue = Queue(robotId=self.robotId, url=self.url, token=self.token, queueName="Showaround Bot")

        for city in city_list:
            self.queue.createItem({"city": city})

    @Robotmethod
    def process(self):
        """Run robot process"""
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

            while True:
                city = self.queue.getNextItem()
                if city is None:
                    break
                self.browser.get("https://www.showaround.com/settings")
                time.sleep(3)
                location = self.browser.find_element_by_xpath("//*[@id='location']/a")
                location.click()
                time.sleep(1)
                location_box = self.browser.find_element_by_xpath("//*[@id='location']/div/form/input")
                location_box.click()
                location_box.clear()
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

    @Robotmethod
    def end(self):
        """Finish robot execution, cleanup environment, close applications and send reports"""

        self.browser.close()


class BusinessException(RobotException):
    """Manage Exceptions Caused by business errors"""

    def _init__(self, message, action):
        super().__init__(get_instances(Main), action)
        self.action = action
        self.message = message
        self.processException()

    def processException(self):
        """Write action when a Business exception occurs"""

        self.Log.businessException(self.message)


class SystemException(RobotException):
    """Manage Exceptions Caused by system errors"""

    def __init__(self, message, action):
        super().__init__(get_instances(Main), action)
        self.retry_times = settings.RETRY_TIMES
        self.action = action
        self.message = message
        self.processException()

    def processException(self):
        """Write action when a system exception occurs"""

        self.reestart(self.retry_times)
        self.Log.systemException(self.message)
