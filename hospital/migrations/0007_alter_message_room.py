# Generated by Django 4.2.2 on 2023-06-24 23:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0006_message_room'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='room',
            field=models.ForeignKey(max_length=100000000, on_delete=django.db.models.deletion.CASCADE, to='hospital.room'),
        ),
    ]
