# Generated by Django 4.0.5 on 2023-04-07 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0006_alter_keyword_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='keyword',
            options={'ordering': ['pos_id']},
        ),
        migrations.RemoveConstraint(
            model_name='keyword',
            name='keyword_order_integrity',
        ),
        migrations.RenameField(
            model_name='keyword',
            old_name='order',
            new_name='pos_id',
        ),
        migrations.AddConstraint(
            model_name='keyword',
            constraint=models.UniqueConstraint(fields=('pos_id', 'note'), name='keyword_pos_id_integrity'),
        ),
    ]
