# coding: utf-8

from datetime import date, timedelta, datetime, time
from qiita_v2.client import QiitaClient
from qiita_v2.response import QiitaResponse
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from tecqii.models import Tag
from tecqii.settings_base import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("running get_tags batch ...")

        client = QiitaClient(access_token=QIITA_ACCESS_TOKEN)
        for i in range(100):
            page = i + 1
            try:
                response = client.list_tags(params='page='+str(page)+'&per_page=100&sort=count')
            except QiitaResponse:
                print('page: '+page)
                pass
            else:
                response_json = response.to_json()
                for tag_json in response_json:
                    Tag.objects.update_or_create(
                        tag_id = tag_json['id'],
                        defaults={
                            'followers_count': tag_json['followers_count'],
                            'icon_url': tag_json['icon_url'],
                            'items_count': tag_json['items_count'],
                        }
                    )
        print('finished.')