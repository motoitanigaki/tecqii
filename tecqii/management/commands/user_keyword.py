import collections
import termextract.japanese_plaintext
import termextract.core
from django.core.management.base import BaseCommand
from tecqii.models import Tag, User, Item, UserTagRelation

class Command(BaseCommand):

    def handle(self, *args, **options):
        print("Running batch 'user_keyword' ...")
