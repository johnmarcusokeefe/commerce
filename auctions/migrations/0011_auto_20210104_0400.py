# Generated by Django 3.0.7 on 2021-01-04 04:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_auto_20210104_0353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlistings',
            name='listing',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='listing_name', to='auctions.Listings'),
        ),
        migrations.AlterField(
            model_name='userlistings',
            name='listing_owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL),
        ),
    ]
