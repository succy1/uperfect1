# Generated by Django 5.1.1 on 2024-10-13 15:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_remove_profile_skin_type_remove_skincaregoal_profile_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionTier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('price', models.BigIntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='profile',
            name='skin_elasticity',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='skin_texture',
        ),
        migrations.AddField(
            model_name='profile',
            name='subscription_tier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.subscriptiontier'),
        ),
    ]
