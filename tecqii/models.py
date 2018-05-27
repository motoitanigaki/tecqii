from django.db import models


class Tag(models.Model):
    followers_count = models.IntegerField(default=0, db_index=True) # このタグをフォローしているユーザの数
    icon_url = models.URLField(max_length=1024, blank=True, null=True) # このタグに設定されたアイコン画像のURL
    tag_id = models.CharField(max_length=128, unique=True) # タグを特定するための一意な名前
    items_count = models.IntegerField(default=0, db_index=True) # このタグが付けられた投稿の数

    def __str__(self):
        return str(self.tag_id)

class User(models.Model):
    description = models.TextField(max_length=1024, blank=True, null=True, db_index=True) # 自己紹介文
    facebook_id = models.CharField(max_length=128, blank=True, null=True) # Facebook ID
    followees_count = models.IntegerField(default=0, db_index=True) # このユーザがフォローしているユーザの数
    followers_count = models.IntegerField(default=0, db_index=True) # このユーザをフォローしているユーザの数
    github_login_name = models.CharField(max_length=128, blank=True, null=True) # GitHub ID
    user_id = models.CharField(max_length=128, unique=True) # ユーザID
    items_count = models.IntegerField(default=0, db_index=True) # このユーザが qiita.com 上で公開している投稿の数
    linkedin_id = models.CharField(max_length=128, blank=True, null=True)
    location = models.CharField(max_length=128, blank=True, null=True, db_index=True)
    name = models.CharField(max_length=128, blank=True, null=True, db_index=True)
    organization = models.CharField(max_length=128, blank=True, null=True, db_index=True)
    permanent_id = models.IntegerField(default=0, db_index=True) # ユーザごとに割り当てられる整数のID
    profile_image_url = models.URLField(max_length=1024, blank=True, null=True) # 設定しているプロフィール画像のURL
    twitter_screen_name = models.CharField(max_length=128, blank=True, null=True) # Twitterのスクリーンネーム
    website_url = models.URLField(max_length=1024, blank=True, null=True) # 設定しているWebサイトのURL
    contribution_count = models.IntegerField(default=0, db_index=True) # Contributionの数 ユーザーごとの記事を全て取得して集計する

    def __str__(self):
        return str(self.user_id)
