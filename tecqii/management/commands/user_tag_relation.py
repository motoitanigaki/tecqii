from django.core.management.base import BaseCommand
from tecqii.models import Tag, User, Item, UserTagRelation

class Command(BaseCommand):

    def handle(self, *args, **options):
        print("Running batch 'user_tag_relation' ...")

        users = User.objects.filter(items_count__gte=1)
        # for user in users:

