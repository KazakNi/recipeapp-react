# Generated by Django 4.1.7 on 2023-04-19 08:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_remove_subscriptions_unique subscriber_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='subscriptions',
            unique_together=set(),
        ),
    ]
