# Generated by Django 3.2.16 on 2022-11-07 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_auto_20221107_1935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(choices=[('Crimson', '#DC143C'), ('PaleVioletRed', '#DB7093'), ('Orange', '#FFA500'), ('DarkKhaki', '#BDB76B'), ('Violet', '#EE82EE'), ('Chocolate', '#D2691E'), ('Silver', '#C0C0C0'), ('Lime', '#00FF00'), ('DeepSkyBlue', '#00BFFF'), ('Olive', '#808000'), ('Lime', '#00FF00')], max_length=48, verbose_name='HEX-код'),
        ),
    ]
