# Generated by Django 3.0.7 on 2020-06-10 00:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('query', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserCounts',
            new_name='UserCount',
        ),
        migrations.RenameModel(
            old_name='VideoCounts',
            new_name='VideoCount',
        ),
    ]
