import os
import sys
import time
import datetime
import traceback
import requests
from urllib.error import URLError
from json.decoder import JSONDecodeError
from http.client import RemoteDisconnected
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

    def tear_down(self):
        self.driver.close()

    def crawl_qiita_user_ranking(self, page):
        QIITA_USER_RANKING_URL = 'https://qiita-user-ranking.herokuapp.com/'
        try:
            print('page: ',page,' --------------')
            self.driver.get(QIITA_USER_RANKING_URL+'?page='+str(page))
            element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/h2')))
            user_ids = self.driver.find_elements_by_xpath('/html/body/main/p[4<position()<24]/a')
            for user_id in user_ids:
                print(user_id.text.strip())
                User.objects.update_or_create(
                    user_id=user_id.text.strip(),
                )
        except TimeoutException:
            print('loading took too much time')
            return False

    def crawl_qiita_users(self, char='A', page=1):
        QIITA_USERS_URL = 'https://qiita.com/users'
        QIITA_INTERNALAPI_HOVERCARD = 'https://qiita.com/api/internal/hovercard_users/'
        try:
            self.driver.get(QIITA_USERS_URL + '?char=' + char + '&page=' + str(page))
            WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div/div[1]/h2')))
        except TimeoutException:
            print('loading took too much time')
        else:
            user_ids = self.driver.find_elements_by_xpath('//*[@id="main"]/div/div/div[2]/div[*]/div/div/p[1]/a')
            for user_id in user_ids:
                try:
                    hover_card = requests.request('GET', QIITA_INTERNALAPI_HOVERCARD+user_id.text.strip()) # using internal api.
                    hover_card_json = hover_card.json()
                    user = User.objects.update_or_create(
                        user_id=user_id.text.strip(),
                        defaults={
                            'items_count': hover_card_json['articles_count'],
                            'contribution_count': int(hover_card_json['contribution']),
                            'permanent_id': int(hover_card_json['id']),
                            'name': hover_card_json['name'],
                            'profile_image_url': hover_card_json['profile_image_url']
                        }
                    )
                    print(user)
                except JSONDecodeError:
                    user = User.objects.update_or_create(
                        user_id=user_id.text.strip(),
                    )
                    print(user, ' JSONDecodeError')
                except RemoteDisconnected:
                    print('RemoteDisconnected. will wait 1 minute.')
                    time.sleep(60)
                except URLError:
                    print('URLError. will break.')
                    break
            try:
                self.driver.find_element_by_xpath('//*[@id="main"]/div/div/div[2]/div[101]/ul/li[2]/a')
            except NoSuchElementException:
                print('no next button, will switch to next char.')
                return False
            except:
                print(sys.exc_info()[1])
            else:
                return True

    def crawl_qiita_user(self, user_id):
        QIITA_URL = 'https://qiita.com/'
        try:
            print('user_id: ',user_id)
            self.driver.get(QIITA_URL + user_id)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#main > div > div > div.col-md-3.col-sm-3.col-xs-12.newUserPageProfile > div.newUserPageProfile_avatar > img')))
        except TimeoutException:
            print('loading took too much time')
        except NoSuchElementException: # Consider the user no longer exists.
            deleted_user = User.objects.get(user_id=user_id)
            deleted_user.delete()
        else:
            try:
                description = self.driver.find_element_by_class_name('newUserPageProfile_description')
                description = description.text
            except NoSuchElementException:
                description = ''
            try:
                facebook_id = self.driver.find_element_by_css_selector(
                    '#main > div > div > div.col-md-3.col-sm-3.col-xs-12.newUserPageProfile > div.newUserPageProfile_header > ul > li.newUserPageProfile_socialLink-facebook > a')
                facebook_id = facebook_id.get_attribute('href')
                facebook_id = facebook_id.replace('https://facebook.com/', '')
            except NoSuchElementException:
                facebook_id = ''
            try:
                followees_count = self.driver.find_elements_by_class_name('userActivityChart_statCount')[2]
                followees_count = int(followees_count.text)
            except NoSuchElementException:
                followees_count = 0
            try:
                followers_count = self.driver.find_element_by_css_selector('#main > div > div > div.col-md-3.col-sm-3.col-xs-12.newUserPageProfile > div:nth-child(6) > div.newUserPageProfile_info_heading > span > a')
                followers_count = followers_count.text
            except NoSuchElementException:
                followers_count = 0
            try:
                github_login_name = self.driver.find_element_by_css_selector('#main > div > div > div.col-md-3.col-sm-3.col-xs-12.newUserPageProfile > div.newUserPageProfile_header > ul > li.newUserPageProfile_socialLink-github > a')
                github_login_name = github_login_name.get_attribute('href')
                github_login_name = github_login_name.replace('https://github.com/', '')
            except NoSuchElementException:
                github_login_name = ''
            try:
                items_count = self.driver.find_elements_by_class_name('userActivityChart_statCount')[0]
                items_count = int(items_count.text)
            except NoSuchElementException:
                items_count = 0
            try:
                linkedin_id = self.driver.find_element_by_css_selector('#main > div > div > div.col-md-3.col-sm-3.col-xs-12.newUserPageProfile > div.newUserPageProfile_header > ul > li.newUserPageProfile_socialLink-linkedin > a')
                linkedin_id = linkedin_id.get_attribute('href')
                linkedin_id = linkedin_id.replace('https://www.linkedin.com/in/','')
            except NoSuchElementException:
                linkedin_id = ''
            try:
                location = self.driver.find_element_by_css_selector('#main > div > div > div.col-md-3.col-sm-3.col-xs-12.newUserPageProfile > div:nth-child(3) > div:nth-child(4)')
                location = location.text
            except NoSuchElementException:
                location = ''
            try:
                name = self.driver.find_element_by_class_name('newUserPageProfile_fullName')
                name = name.text
            except NoSuchElementException:
                name = ''
            try:
                organization = self.driver.find_element_by_css_selector('#main > div > div > div.col-md-3.col-sm-3.col-xs-12.newUserPageProfile > div:nth-child(3) > div:nth-child(3)')
                organization = organization.text
            except NoSuchElementException:
                organization = ''
            try:
                profile_image_url = self.driver.find_element_by_css_selector('#main > div > div > div.col-md-3.col-sm-3.col-xs-12.newUserPageProfile > div.newUserPageProfile_avatar > img')
                profile_image_url = profile_image_url.get_attribute('src')
            except NoSuchElementException:
                profile_image_url = ''
            try:
                twitter_screen_name = self.driver.find_element_by_css_selector('#main > div > div > div.col-md-3.col-sm-3.col-xs-12.newUserPageProfile > div.newUserPageProfile_header > ul > li.newUserPageProfile_socialLink-twitter > a')
                twitter_screen_name = twitter_screen_name.get_attribute('href')
                twitter_screen_name = twitter_screen_name.replace('https://twitter.com/','')
            except NoSuchElementException:
                twitter_screen_name = ''
            try:
                website_url = self.driver.find_element_by_css_selector('#main > div > div > div.col-md-3.col-sm-3.col-xs-12.newUserPageProfile > div:nth-child(3) > div:nth-child(2) > a')
                website_url = website_url.get_attribute('href')
            except NoSuchElementException:
                website_url = ''
            try:
                contribution_count = self.driver.find_elements_by_class_name('userActivityChart_statCount')[1]
                contribution_count = contribution_count.text
            except NoSuchElementException:
                contribution_count = 0

            User.objects.update_or_create(
                user_id=user_id,
                defaults={
                    'description': description,
                    'facebook_id': facebook_id,
                    'followees_count': followees_count,
                    'followers_count': followers_count,
                    'github_login_name': github_login_name,
                    'items_count': items_count,
                    'linkedin_id': linkedin_id,
                    'location': location,
                    'name': name,
                    'organization': organization,
                    'profile_image_url': profile_image_url,
                    'twitter_screen_name': twitter_screen_name,
                    'website_url': website_url,
                    'contribution_count': contribution_count,
                }
            )

            print('description: ',description)
            print('facebook_id: ',facebook_id)
            print('followees_count: ',followees_count)
            print('followers_count: ',followers_count)
            print('github_login_name: ',github_login_name)
            print('items_count: ',items_count)
            print('linkedin_id: ',linkedin_id)
            print('location: ',location)
            print('name: ',name)
            print('organization: ',organization)
            print('profile_image_url: ',profile_image_url)
            print('twitter_screen_name: ',twitter_screen_name)
            print('website_url: ',website_url)
            print('contribution_count: ',contribution_count)