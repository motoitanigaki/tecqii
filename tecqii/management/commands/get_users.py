# coding: utf-8

import sys
import time
from datetime import date, timedelta, datetime
from qiita_v2.client import QiitaClient
from qiita_v2.response import QiitaResponse
from django.core.management.base import BaseCommand
from django.conf import settings
from tecqii.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("running get_tags batch ...")

        client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKEN)
        client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKENS[0])
        users = User.objects.all()
        counter = 0
        for user in users:
            counter += 1
            if counter == 1000:
                print('1000 user finished.')
                client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKENS[1])
            elif counter == 2000:
                print('2000 user finished.')
                client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKENS[2])
            elif counter == 3000:
                print('3000 user finished.')
                client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKENS[3])
            elif counter == 4000:
                print('4000 user finished.')
                client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKENS[4])
            elif counter == 5000:
                print('5000 user finished.')
                client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKENS[5])
            elif counter == 6000:
                print('6000 user finished.')
                client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKENS[6])
            elif counter == 7000:
                print('7000 user finished.')
                client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKENS[7])
            elif counter == 8000:
                print('8000 user finished.')
                client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKENS[8])
            elif counter == 9000:
                print('9000 user finished.')
                client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKENS[9])
            elif counter == 10000:
                print('10000 user finished.')
                client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKENS[10])
            elif counter == 11000:
                print('11000 user finished.')
                client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKENS[11])
            elif counter == 12000:
                print('12000 user finished.')
                client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKENS[12])
            elif counter == 13000:
                print('13000 user finished.')
                client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKENS[13])
            elif counter == 14000:
                print('14000 user finished.')
                client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKENS[14])
            elif counter == 15000:
                print('15000 user finished.')
                client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKENS[15])
            elif counter == 16000:
                print('16000 user finished.')
                client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKENS[16])
            elif counter == 17000:
                print('17000 user finished.')
                client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKENS[17])
            elif counter == 18000:
                print('18000 user finished.')
                client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKENS[18])
            elif counter == 19000:
                print('19000 user finished.')
                client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKENS[19])
            elif counter > 20000:
                print('20000 user finished.')
                counter = 1
                print('wait for 1 hour. --------------------')
                time.sleep(3600)
                print('1 hour has passed. --------------------')
                client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKENS[0])
            try:
                response = client.get_user(id=user.user_id)
            except:
                print(sys.exc_info()[1])
                User.objects.get(user_id=user.user_id).delete()
                print(user.user_id,' deleted.')
            else:
                response_json = response.to_json()
                User.objects.update_or_create(
                    user_id = response_json['id'],
                    defaults={
                        'description': response_json['description'],
                        'facebook_id': response_json['facebook_id'],
                        'followees_count': response_json['followees_count'],
                        'followers_count': response_json['followers_count'],
                        'github_login_name': response_json['github_login_name'],
                        'items_count': response_json['items_count'],
                        'linkedin_id': response_json['linkedin_id'],
                        'location': response_json['location'],
                        'name': response_json['name'],
                        'organization': response_json['organization'],
                        'permanent_id': response_json['permanent_id'],
                        'profile_image_url': response_json['profile_image_url'],
                        'twitter_screen_name': response_json['twitter_screen_name'],
                        'website_url': response_json['website_url'],
                    }
                )
        print('finished.')

