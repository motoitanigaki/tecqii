# coding: utf-8

from datetime import date, timedelta, datetime, time
from qiita_v2.client import QiitaClient
from qiita_v2.response import QiitaResponse
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from tecqii.models import User, Tag
from django.conf import settings
from tecqii.crawler import Crawler


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("running crawl_users batch ...")
        crawler = Crawler()
        users = User.objects.all()
        for user in users:
            crawler.crawl_qiita_user(user.user_id)
        crawler.tear_down()
        print('finished.')