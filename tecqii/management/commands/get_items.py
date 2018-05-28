# coding: utf-8

import sys
import time
import math
from datetime import datetime as dt
from datetime import date, timedelta, datetime
from qiita_v2.client import QiitaClient
from qiita_v2.response import QiitaResponse
from django.core.management.base import BaseCommand
from django.conf import settings
from tecqii.models import User, Tag, Item


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("running get_tags batch ...")

        client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKEN)
        client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKENS[0])
        users = User.objects.filter(items_count__gte=1) # users who has ever posted
        counter = 0
        for user in users:
            if counter == 1000:
                client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKENS[1])
            elif counter == 2000:
                client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKENS[2])
            elif counter == 3000:
                client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKENS[3])
            elif counter == 4000:
                client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKENS[4])
            elif counter == 5000:
                client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKENS[5])
            elif counter == 6000:
                client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKENS[6])
            elif counter == 7000:
                client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKENS[7])
            elif counter == 8000:
                client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKENS[8])
            elif counter == 9000:
                client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKENS[9])
            elif counter > 10000:
                counter = 1
                print('wait for 1 hour. --------------------')
                time.sleep(3600)
                print('1 hour has passed. --------------------')
                client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKENS[0])
            call_count = math.ceil(user.items_count/100)
            for page in range(call_count):
                try:
                    print('user_id: ', user.user_id, ' page: ', page + 1)
                    counter += 1
                    response = client.list_user_items(user_id=user.user_id, params='page='+str(page + 1)+'&per_page=100&sort=count')
                except:
                    print(sys.exc_info()[1])
                    # User.objects.get(user_id=user.user_id).delete()
                    print(user.user_id,' deleted.')
                else:
                    response_json = response.to_json()
                    for item_json in response_json:
                        created_at = item_json['created_at'][:-6] # ignore timezone. not sure about the problem.
                        created_at = dt.strptime(created_at, '%Y-%m-%dT%H:%M:%S')
                        updated_at = item_json['updated_at'][:-6]
                        updated_at = dt.strptime(updated_at, '%Y-%m-%dT%H:%M:%S')
                        auther = item_json['user']['id']
                        auther = User.objects.get(user_id=auther)

                        Item.objects.update_or_create(
                            item_id = item_json['id'],
                            defaults={
                                "rendered_body": item_json['rendered_body'],
                                "body": item_json['body'],
                                "comments_count": item_json['comments_count'],
                                "created_at": created_at,
                                "likes_count": item_json['likes_count'],
                                "reactions_count": item_json['reactions_count'],
                                "title": item_json['title'],
                                "updated_at": updated_at,
                                "url": item_json['url'],
                                "user":auther,
                            }
                        )

                        item = Item.objects.get(item_id=item_json['id'])
                        tags_json = item_json['tags']
                        for tag_json in tags_json:
                            Tag.objects.get_or_create(tag_id=tag_json['name'])
                            tag = Tag.objects.get(tag_id=tag_json['name'])
                            item.tags.add(tag)
                        item.save()
        print('finished.')

