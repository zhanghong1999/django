# Generated by Django 4.2 on 2023-05-16 12:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee_web', '0005_news'),
    ]

    operations = [
        migrations.RenameField(
            model_name='news',
            old_name='user',
            new_name='admin',
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oid', models.CharField(max_length=64, verbose_name='订单号')),
                ('name', models.CharField(max_length=32, verbose_name='商品名称')),
                ('price', models.IntegerField(verbose_name='价格')),
                ('status', models.SmallIntegerField(choices=[(1, '未支付'), (2, '已支付')], default=1, verbose_name='状态')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee_web.userinfo', verbose_name='用户')),
            ],
        ),
    ]