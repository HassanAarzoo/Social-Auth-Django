# Generated by Django 3.0.5 on 2020-06-13 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200613_0906'),
    ]

    operations = [
        migrations.AddField(
            model_name='sociallogindetails',
            name='provider_social',
            field=models.CharField(default='', max_length=250, unique=True),
        ),
    ]
