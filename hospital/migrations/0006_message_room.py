# Generated by Django 4.2.2 on 2023-06-24 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0005_rename_dat_message_date_room_patient'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='room',
            field=models.CharField(blank=True, max_length=100000000),
        ),
    ]
