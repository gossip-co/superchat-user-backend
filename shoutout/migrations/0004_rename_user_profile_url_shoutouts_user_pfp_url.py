# Generated by Django 4.1.7 on 2023-03-17 19:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shoutout', '0003_alter_shoutouts_options_shoutouts_amount_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shoutouts',
            old_name='user_profile_url',
            new_name='user_pfp_url',
        ),
    ]
