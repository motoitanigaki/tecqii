from django.core.management.base import BaseCommand
from tecqii.models import Tag, User, Item, UserTagRelation

class Command(BaseCommand):

    def handle(self, *args, **options):
        print("Running batch 'user_tag_relation' ...")

        users = User.objects.filter(items_count__gte=1)
        for user in users:
            items = Item.objects.filter(user=user)
            tag_item_count = {}
            tag_contribution_count = {}
            for item in items:
                tags = item.tags.all()
                for tag in tags:
                    if tag.tag_id in tag_item_count:
                        tag_item_count[tag.tag_id] += 1
                        tag_contribution_count[tag.tag_id] += item.likes_count
                    else:
                        tag_item_count[tag.tag_id] = 1
                        tag_contribution_count[tag.tag_id] = item.likes_count

            tag_item_count = sorted(tag_item_count.items(), key=lambda x: -x[1])
            tag_contribution_count = sorted(tag_contribution_count.items(), key=lambda x: -x[1])

            for item in tag_item_count:
                tag = Tag.objects.get(tag_id=item[0])
                UserTagRelation.objects.update_or_create(
                    user=user,
                    tag=tag,
                    defaults={
                        'items_count': int(item[1])
                    }
                )

            for contribution in tag_contribution_count:
                tag = Tag.objects.get(tag_id=contribution[0])
                UserTagRelation.objects.update_or_create(
                    user=user,
                    tag=tag,
                    defaults={
                        'contribution_count': int(contribution[1])
                    }
                )

        print('finished.')