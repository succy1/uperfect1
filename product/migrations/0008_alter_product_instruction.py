# Generated by Django 5.1.1 on 2024-10-14 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_remove_product_recommended_age_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='instruction',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
