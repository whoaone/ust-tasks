# Generated by Django 3.0.8 on 2020-07-22 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_remove_task_task_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='task_no',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
