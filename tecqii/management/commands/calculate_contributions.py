# coding: utf-8

from django.core.management.base import BaseCommand
from tecqii.models import User, UserTagRelation
from django.conf import settings
from django.db.models import Sum
from tecqii.crawler import Crawler


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("running calculate_contributions batch ...")

        users = User.objects.all()
        for user in users:
            sum = user.item_set.all().aggregate(Sum('likes_count'))
            user.contribution_count = sum
            print(user,' ',user.contribution_count,' ',sum)
            user.save()
