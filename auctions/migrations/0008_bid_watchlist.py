# Generated by Django 3.1.4 on 2020-12-28 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auto_20201227_1015'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='watchlist',
            field=models.BooleanField(default=False),
        ),
    ]
