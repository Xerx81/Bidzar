# Generated by Django 4.2.3 on 2023-07-26 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_alter_bid_bidder_alter_comments_commenter_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
