# Generated by Django 2.1.8 on 2021-03-30 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gentannieReferal', '0004_auto_20210319_2333'),
    ]

    operations = [
        migrations.AddField(
            model_name='referral_account',
            name='ammount',
            field=models.CharField(default=0, max_length=20),
            preserve_default=False,
        ),
    ]
