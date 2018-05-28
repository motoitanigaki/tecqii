# coding: utf-8

from datetime import date, timedelta, datetime, time
from qiita_v2.client import QiitaClient
from qiita_v2.response import QiitaResponse
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from tecqii.models import Tag
from django.conf import settings
from tecqii.crawler import Crawler


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("running crawl_users batch ...")
        crawler = Crawler()
        index = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '_']
        for char in index:
            has_next_page = True
            page = 1
            while has_next_page:
                has_next_page = crawler.crawl_qiita_users(char, page)
                page += 1
        crawler.tear_down()
        print('finished.')

