# coding: utf-8

import json
from datetime import date, timedelta, datetime, time
from qiita_v2.client import QiitaClient
from qiita_v2.response import QiitaResponse
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from tecqii.models import Tag
from tecqii.crawler import Crawler


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("running crawl_users_qiita batch ...")
        crawler = Crawler()
        index = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '_']
        json_file = open("crawl_users_qiita.json", 'r')
        json_data = json.load(json_file)
        first_char = json_data["char"]
        first_page = json_data["page"]
        char_found = False
        for char in index:
            has_next_page = True
            page = 1
            # if char == 'G':
            #     page = 16

            # find the character with which the process failed at the last time.
            if char == first_char:
                char_found = True
                page = first_page

            if char_found:
                while has_next_page:
                    has_next_page = crawler.crawl_qiita_users(char, page)
                    page += 1
                    
                    json_data["char"] = char
                    json_data["page"] = page
                    print(json_data)
                    json_file_write = open('crawl_users_qiita.json', 'w')
                    json.dump(json_data, json_file_write, indent=4)

        crawler.tear_down()
        print('finished.')

