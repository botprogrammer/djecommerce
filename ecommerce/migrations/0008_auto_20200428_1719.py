# Generated by Django 2.2.10 on 2020-04-28 11:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0007_auto_20200428_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 28, 17, 19, 17, 393445)),
        ),
    ]
