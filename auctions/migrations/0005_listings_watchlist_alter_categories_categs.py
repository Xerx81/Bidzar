# Generated by Django 4.2.3 on 2023-07-24 12:43

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_alter_categories_categs'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='watchlist',
            field=models.ManyToManyField(blank=True, null=True, related_name='user_watchlist', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='categories',
            name='categs',
            field=models.CharField(max_length=50),
        ),
    ]
