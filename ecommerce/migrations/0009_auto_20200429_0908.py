# Generated by Django 2.2.10 on 2020-04-29 03:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0008_auto_20200428_1719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 29, 9, 8, 8, 222085)),
        ),
    ]