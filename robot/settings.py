import os
from pathlib import Path

ROBOT_FOLDER = Path(os.path.dirname(os.path.realpath(__file__))).parent

RETRY_TIMES = 3

"""Folder to store Chrome Driver"""
CHROMEDRIVER_PATH = os.path.join(ROBOT_FOLDER, "Driver")

"""Emial General settings"""
EMAIL_ACCOUNT = None
EMAIL_PASSWORD = None

"""Outgoing email settings"""
EMAIL_SMTP_SERVER = None
EMAIL_SMTP_POST = None


LOGIN_MAIL = "info@travelandabroad.com"
LOGIN_PASSWORD = "Gonzalo01!"


"""Incoming email settings"""
EMAIL_IMAP_SERVER = None
EMAIL_IMAP_PORT = None
