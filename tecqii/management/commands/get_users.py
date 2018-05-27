# coding: utf-8

import sys
import time
from datetime import date, timedelta, datetime, time
from qiita_v2.client import QiitaClient
from qiita_v2.response import QiitaResponse
from django.core.management.base import BaseCommand
from django.conf import settings
from tecqii.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("running get_tags batch ...")

        client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKEN)
        # client = QiitaClient(access_token='hoge')
        users = User.objects.all()
        counter = 0
        for user in users:
            counter += 1
            if counter > 1000: # When the call count hits the limitation, wait till it gets callable again.
                counter = 1
                print('wait for 1 hour. --------------------')
                time.sleep(3600)
                print('1 hour has passed. --------------------')
            try:
                response = client.get_user(id=user.user_id)
            except:
                print(sys.exc_info()[1])
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
                print(response_json['id'])
        print('finished.')

