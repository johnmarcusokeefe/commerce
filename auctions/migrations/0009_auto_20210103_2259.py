# Generated by Django 3.1.1 on 2021-01-03 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20210103_2207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlistings',
            name='listing_id',
            field=models.CharField(default=None, max_length=50),
        ),
        migrations.AlterField(
            model_name='userlistings',
            name='user_id',
            field=models.CharField(default=None, max_length=50),
        ),
    ]