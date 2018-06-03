# coding: utf-8

import sys
import time
import math
import pytz
import traceback
from datetime import date, timedelta, datetime
from qiita_v2.client import QiitaClient
from qiita_v2.response import QiitaResponse
from django.core.management.base import BaseCommand
from django.conf import settings
from tecqii.models import User, Tag, Item


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("running get_items_date batch ...")

        client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKENS[0])
        start_date = datetime.strptime('2011-09-16', '%Y-%m-%d')
        today = datetime.today()
        days_15 = timedelta(days=+15)

        counter = 0
        while start_date < today:
            end_date = start_date + days_15
            for i in range(100):
                # skip if the items_count and the item_set.count() is the same.
                if counter == 1000:
                    print('1000 calls finished.')
                    client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKENS[1])
                elif counter == 2000:
                    print('2000 calls finished.')
                    client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKENS[2])
                elif counter == 3000:
                    print('3000 calls finished.')
                    client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKENS[3])
                elif counter == 4000:
                    print('4000 calls finished.')
                    client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKENS[4])
                elif counter == 5000:
                    print('5000 calls finished.')
                    client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKENS[5])
                elif counter == 6000:
                    print('6000 calls finished.')
                    client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKENS[6])
                elif counter == 7000:
                    print('7000 calls finished.')
                    client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKENS[7])
                elif counter == 8000:
                    print('8000 calls finished.')
                    client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKENS[8])
                elif counter == 9000:
                    print('9000 calls finished.')
                    client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKENS[9])
                elif counter == 10000:
                    print('10000 calls finished.')
                    client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKENS[10])
                elif counter == 11000:
                    print('11000 calls finished.')
                    client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKENS[11])
                elif counter == 12000:
                    print('12000 calls finished.')
                    client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKENS[12])
                elif counter == 13000:
                    print('13000 calls finished.')
                    client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKENS[13])
                elif counter == 14000:
                    print('14000 calls finished.')
                    client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKENS[14])
                elif counter == 15000:
                    print('15000 calls finished.')
                    client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKENS[15])
                elif counter == 16000:
                    print('16000 calls finished.')
                    client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKENS[16])
                elif counter == 17000:
                    print('17000 calls finished.')
                    client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKENS[17])
                elif counter == 18000:
                    print('18000 calls finished.')
                    client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKENS[18])
                elif counter == 19000:
                    print('19000 calls finished.')
                    client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKENS[19])
                elif counter > 20000:
                    print('20000 calls finished.')
                    counter = 1
                    print('wait for 1 hour. --------------------')
                    time.sleep(3600)
                    print('1 hour has passed. --------------------')
                    client = QiitaClient(access_token=settings.QIITA_ACCESS_TOKENS[0])

                params = 'page=' + str(i+1) + '&per_page=100' + '&query=created:>=' + start_date.strftime('%Y-%m-%d') + '+created:<' + end_date.strftime('%Y-%m-%d')
                try:
                    counter += 1
                    response = client.list_items(params=params)
                except:
                    print(sys.exc_info()[1])
                else:
                    response_json = response.to_json()
                    for item_json in response_json:
                        created_at = item_json['created_at'] # ignore timezone. not sure about the problem.
                        created_at = datetime.strptime(''.join(created_at.rsplit(':', 1)), '%Y-%m-%dT%H:%M:%S%z')
                        updated_at = item_json['updated_at']
                        updated_at = datetime.strptime(''.join(updated_at.rsplit(':', 1)), '%Y-%m-%dT%H:%M:%S%z')
                        auther = item_json['user']['id']
                        auther = User.objects.get_or_create(user_id=auther)[0]
                        try:
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
                        except Exception:
                            traceback.print_exc()

                    print(params, '   saved item count: ', len(response_json))
                    if len(response_json) < 100:
                        break
            start_date += days_15

        print('finished. at: ', datetime.now())

