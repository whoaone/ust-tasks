# Generated by Django 3.0.8 on 2020-07-26 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0020_auto_20200725_2014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='close_project',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
