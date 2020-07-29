# Generated by Django 3.0.8 on 2020-07-22 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_task_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='task_no',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='category',
            field=models.CharField(choices=[('01', '01-SSR'), ('02', '02-Test Plan'), ('03', '03-Weight & Balance'), ('04', '04-Electrical Load Analysis'), ('05', '05-Process Specification'), ('06', '06-Certification Plan'), ('07', '07-Sevice Bulletin'), ('08', '08-Standards'), ('09', '09-Engineering, Functional Hazard, Flamm'), ('10', '10-Manuals (IPC, CMM, AFMS..)'), ('11', '11-Kit Lists'), ('12', '12-Airworthiness'), ('13', '13-EO'), ('14', '14-Miscellaneious (Performance)'), ('15', '15-Compliance Reports'), ('16', '16-Regulatory Airworthiness Assessment (RAA)'), ('17', '17-Drawing'), ('18', '18-SolidWorks Model'), ('19', '19-Research'), ('20', '20-Training'), ('21', '21-Other')], max_length=100, null=True),
        ),
    ]
