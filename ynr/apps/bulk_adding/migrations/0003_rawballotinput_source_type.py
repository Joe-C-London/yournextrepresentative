# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-09 08:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("bulk_adding", "0002_rawballotinput")]

    operations = [
        migrations.AddField(
            model_name="rawballotinput",
            name="source_type",
            field=models.CharField(
                choices=[
                    ("bulk_add_form", "Bulk Add form"),
                    ("council_csv", "Council CSV"),
                ],
                default="bulk_add_form",
                max_length=255,
            ),
        )
    ]
