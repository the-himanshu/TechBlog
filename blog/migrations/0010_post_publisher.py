# Generated by Django 3.0.8 on 2020-07-27 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20200727_1722'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='publisher',
            field=models.CharField(default='Anonymous', max_length=50),
        ),
    ]
