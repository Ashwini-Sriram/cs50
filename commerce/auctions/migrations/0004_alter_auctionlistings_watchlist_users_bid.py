# Generated by Django 4.0.5 on 2022-06-14 16:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_remove_auctionlistings_watchlist_items_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlistings',
            name='watchlist_users',
            field=models.ManyToManyField(blank=True, related_name='watchlist', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid', models.FloatField(blank=True, max_length=64)),
                ('current_bid', models.FloatField(max_length=64)),
                ('list_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.auctionlistings')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
