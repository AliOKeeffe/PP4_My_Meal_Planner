# Generated by Django 3.2.13 on 2022-06-23 13:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eateasy', '0011_auto_20220623_1336'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='ingredients',
        ),
    ]