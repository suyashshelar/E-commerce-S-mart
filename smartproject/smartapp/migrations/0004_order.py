# Generated by Django 5.0.2 on 2024-03-02 08:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartapp', '0003_address11'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderid', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('pid', models.ForeignKey(db_column='pid', on_delete=django.db.models.deletion.CASCADE, to='smartapp.products')),
                ('uid', models.ForeignKey(db_column='uid', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
