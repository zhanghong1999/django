# Generated by Django 4.2 on 2023-04-23 13:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee_web', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrettyNum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobiles', models.CharField(max_length=11, verbose_name='号码')),
                ('price', models.IntegerField(blank=True, default=0, null=True, verbose_name='价格')),
                ('level', models.SmallIntegerField(choices=[(1, 'Ⅰ级'), (2, 'Ⅱ级'), (3, 'Ⅲ级')], default=1, verbose_name='级别')),
                ('status', models.SmallIntegerField(choices=[(1, '已占用'), (2, '未占用')], default=2, verbose_name='状态')),
            ],
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='depart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee_web.department', verbose_name='部门'),
        ),
    ]
