# Generated by Django 4.0.5 on 2023-04-07 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0004_alter_keyword_options_keyword_order_delete_position'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='keyword',
            constraint=models.UniqueConstraint(fields=('order', 'note'), name='keyword_order_integrity'),
        ),
    ]
