# Generated by Django 3.2.16 on 2022-10-30 13:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_auto_20221030_1542'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favorite',
            options={'verbose_name': 'Избранное', 'verbose_name_plural': 'Избранное'},
        ),
        migrations.RenameField(
            model_name='ingredient',
            old_name='count',
            new_name='amount',
        ),
    ]
