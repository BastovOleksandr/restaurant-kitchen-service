# Generated by Django 5.1.1 on 2024-09-24 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("kitchen", "0001_initial"),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name="cook",
            name="kitchen_coo_usernam_8e43b7_idx",
        ),
        migrations.RemoveIndex(
            model_name="dish",
            name="kitchen_dis_name_c59839_idx",
        ),
        migrations.RemoveIndex(
            model_name="dishtype",
            name="kitchen_dis_name_18e266_idx",
        ),
    ]
