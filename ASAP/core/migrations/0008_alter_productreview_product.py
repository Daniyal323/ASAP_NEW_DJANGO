# Generated by Django 5.0 on 2024-09-17 16:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_productimages_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productreview',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviews', to='core.product'),
        ),
    ]
