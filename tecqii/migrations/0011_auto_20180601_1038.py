# Generated by Django 2.0.5 on 2018-06-01 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tecqii', '0010_auto_20180529_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='facebook_id',
            field=models.CharField(blank=True, default='', max_length=256),
        ),
        migrations.AlterField(
            model_name='user',
            name='github_login_name',
            field=models.CharField(blank=True, default='', max_length=256),
        ),
        migrations.AlterField(
            model_name='user',
            name='linkedin_id',
            field=models.CharField(blank=True, default='', max_length=256),
        ),
        migrations.AlterField(
            model_name='user',
            name='location',
            field=models.CharField(blank=True, db_index=True, default='', max_length=256),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(blank=True, db_index=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='organization',
            field=models.CharField(blank=True, db_index=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='twitter_screen_name',
            field=models.CharField(blank=True, default='', max_length=256),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_id',
            field=models.CharField(max_length=256, unique=True),
        ),
    ]
