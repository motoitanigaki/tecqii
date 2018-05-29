import csv
from django.core.management.base import BaseCommand
from tecqii.models import Tag, User, Item, UserTagRelation

class Command(BaseCommand):

    def handle(self, *args, **options):
        print("Running batch 'export_users' ...")

        users = User.objects.all()
        with open('users_data.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            for user in users:
                writer.writerow([user.user_id,
                                user.items_count,
                                user.contribution_count,
                                user.permanent_id, user.name,
                                user.profile_image_url])

        print('finished.')