import os
import time
import random
import pandas as pd
from iBott.robot_activities import Robot, RobotException, Robotmethod, get_all_Methods, get_instances, Queue
from iBott.browser_activities import ChromeBrowser
import robot.settings as settings
from navigation.showaround import Showaround


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
        self.queue.setRetryTimes(10)
        for city in city_list:
            self.queue.createItem({"city": city})

        #Init showaaround classes
        self.showaround = Showaround(self.browser, self)


    @Robotmethod
    def login(self):
        try:
            self.showaround.login()
        except:
            raise SystemException("Login fail", "login")

    @Robotmethod
    def process(self):
        """Run robot process"""
        while True:
            city = self.queue.getNextItem()
            if city is None:
                break
            try:
                self.showaround.apply(city)
                city.setItemAsOk()
            except Exception as e:
                raise SystemException
                city.setItemAsFail()

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
