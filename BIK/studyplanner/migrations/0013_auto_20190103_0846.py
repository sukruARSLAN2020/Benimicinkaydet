# Generated by Django 2.1.4 on 2019-01-03 03:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studyplanner', '0012_auto_20190103_0845'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='method',
            options={'ordering': ['is_completed', 'deadline']},
        ),
        migrations.AlterModelOptions(
            name='subject',
            options={'ordering': ['is_completed', 'deadline']},
        ),
        migrations.AlterModelOptions(
            name='subtopic',
            options={'ordering': ['is_completed', 'deadline']},
        ),
    ]
