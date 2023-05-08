# Generated by Django 4.1.8 on 2023-05-08 03:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0005_alter_auction_owner_watchlist_auction_watchers"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="watchlist",
            field=models.ManyToManyField(
                blank=True, related_name="watched_auctions", to="auctions.auction"
            ),
        ),
        migrations.AlterField(
            model_name="watchlist",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="watchlists",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]