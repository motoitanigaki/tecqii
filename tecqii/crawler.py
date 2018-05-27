import os
import time
import datetime
import traceback
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from django.conf import settings
from tecqii.models import User

class Crawler():

    def __init__(self):
        self.driver = webdriver.PhantomJS(settings.PHANTOMJS_PATH)  # VPS用
        self.driver.set_window_size(1400, 1000)
        self.driver.implicitly_wait(10)

    def crawl_qiita_user_ranking(self, page):
        try:
            print('page: ',page,' --------------')
            self.driver.get(settings.QIITA_USER_RANKING_URL+'?page='+str(page))
            element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/main/h2")))
            user_ids = self.driver.find_elements_by_xpath('/html/body/main/p[4<position()<24]/a')
            for user_id in user_ids:
                print(user_id.text.strip())
                User.objects.update_or_create(
                    user_id=user_id.text.strip(),
                )
        except TimeoutException:
            print('loading took too much time')
            return False
