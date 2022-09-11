# Generated by Django 2.1.8 on 2021-06-05 21:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='notify_all_user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', tinymce.models.HTMLField(max_length=999)),
                ('sent_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='notify_user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', tinymce.models.HTMLField(max_length=49000)),
                ('message_time', models.DateField(auto_now_add=True)),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='smart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan', models.CharField(blank=True, default='smart', max_length=30, null=True)),
                ('plan_name', models.CharField(blank=True, choices=[('basic', 'basic'), ('standard', 'standard'), ('premium', 'premium'), ('bronze', 'bronze'), ('super_bronze', 'super_bronze'), ('silver', 'silver'), ('super_silver', 'super_silver'), ('Gold', 'Gold')], max_length=30, null=True)),
                ('amount_deposited', models.CharField(default=0.0, max_length=20)),
                ('ROI', models.CharField(default=0.0, max_length=20)),
                ('deposit_status', models.CharField(choices=[('pending', 'pending'), ('comfirmed', 'comfirmed'), ('rejected', 'rejected')], default='pending', max_length=15)),
                ('account_type', models.CharField(choices=[('locked', 'locked'), ('unlocked', 'unlocked')], max_length=30)),
                ('request', models.BooleanField(default=False)),
                ('payment_status', models.CharField(blank=True, choices=[('payment_pending', 'payment_pending'), ('payment_done', 'payment_done'), ('payment_declined', 'payment_declined')], default=None, max_length=20, null=True)),
                ('due_date', models.DateTimeField(blank=True, null=True)),
                ('payment_proof', models.FileField(upload_to='images')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('payment_count', models.IntegerField(default=0)),
                ('username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='smart_payment_comfirm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request', models.BooleanField()),
                ('username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='super',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan', models.CharField(blank=True, default='super', max_length=30, null=True)),
                ('plan_name', models.CharField(choices=[('diamond', 'diamond'), ('Ruby', 'Ruby'), ('peal', 'peal'), ('emerald', 'emerald'), ('Jasper', 'Jasper')], max_length=30)),
                ('amount_deposited', models.CharField(default=0.0, max_length=20)),
                ('ROI', models.CharField(default=0.0, max_length=20)),
                ('deposit_status', models.CharField(choices=[('pending', 'pending'), ('comfirmed', 'comfirmed'), ('rejected', 'rejected')], default='pending', max_length=15)),
                ('payment_status', models.CharField(blank=True, choices=[('payment_pending', 'payment_pending'), ('payment_done', 'payment_done'), ('payment_declined', 'payment_declined')], default=None, max_length=20, null=True)),
                ('account_type', models.CharField(choices=[('locked', 'locked'), ('unlocked', 'unlocked')], max_length=30)),
                ('request', models.BooleanField(default=False)),
                ('payment_proof', models.FileField(upload_to='images')),
                ('due_date', models.DateTimeField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('payment_count', models.IntegerField(default=0)),
                ('username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='super_payment_comfirm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request', models.BooleanField()),
                ('username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='supreme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan', models.CharField(blank=True, default='supreme', max_length=30, null=True)),
                ('amount_deposited', models.CharField(default=0.0, max_length=20)),
                ('ROI', models.CharField(default=0.0, max_length=20)),
                ('deposit_status', models.CharField(choices=[('pending', 'pending'), ('comfirmed', 'comfirmed'), ('rejected', 'rejected')], default='pending', max_length=15)),
                ('payment_status', models.CharField(blank=True, choices=[('payment_pending', 'payment_pending'), ('payment_done', 'payment_done'), ('payment_declined', 'payment_declined')], default=None, max_length=20, null=True)),
                ('plan_name', models.CharField(choices=[('Whale', 'Whale'), ('Patriot', 'Patriot')], max_length=30)),
                ('payment_proof', models.FileField(upload_to='images')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('due_date', models.DateTimeField(blank=True, null=True)),
                ('request', models.BooleanField(default=False)),
                ('payment_count', models.IntegerField(default=0)),
                ('username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='supreme_payment_comfirm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request', models.BooleanField()),
                ('username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='users_details',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('middle_name', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=15)),
                ('Email_address', models.EmailField(max_length=50)),
                ('profile_pic', models.FileField(upload_to='Images')),
                ('account_number', models.CharField(max_length=20)),
                ('account_name', models.CharField(max_length=50)),
                ('bank_name', models.CharField(max_length=50)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='users_investment_progress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('package', models.CharField(default='NONE', max_length=20)),
                ('plan', models.CharField(default='none', max_length=20)),
                ('account_type', models.CharField(default='NONE', max_length=20)),
                ('amount_deposited', models.CharField(default=0.0, max_length=20)),
                ('ROI', models.CharField(default=0.0, max_length=20)),
                ('deposit_status', models.CharField(choices=[('pending', 'pending'), ('comfirmed', 'comfirmed'), ('rejected', 'rejected')], default='pending', max_length=15)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('Due_date', models.DateTimeField(blank=True, null=True)),
                ('proof', models.FileField(upload_to='Images')),
                ('Roll_out_time', models.DateField(auto_now=True)),
                ('payment_status', models.CharField(blank=True, choices=[('payment_pending', 'payment_pending'), ('payment_done', 'payment_done'), ('payment_declined', 'payment_declined')], default=None, max_length=20, null=True)),
                ('life_span', models.CharField(max_length=50)),
                ('hault', models.BooleanField(default=False)),
                ('withdraw_request', models.BooleanField(default=False)),
                ('count', models.IntegerField(blank=True, default=0, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='withdrawal_tabel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('date_filled', models.DateTimeField(auto_now_add=True)),
                ('package', models.CharField(max_length=30)),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='withdrawal_table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.CharField(max_length=20)),
                ('requested_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('pending', 'pending'), ('comfirmed', 'comfirmed'), ('rejected', 'rejected')], max_length=20)),
                ('comfirmed_payment', models.BooleanField()),
                ('user', models.ForeignKey(on_delete=None, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
