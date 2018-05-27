from django.db import models


class Tag(models.Model):
    followers_count = models.IntegerField(default=0, db_index=True)
    icon_url = models.URLField(max_length=1024, blank=True, null=True)
    tag_id = models.CharField(max_length=128, unique=True)
    items_count = models.IntegerField(default=0, db_index=True)

    def __str__(self):
        return str(self.tag_id)