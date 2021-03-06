# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-23 08:46
from __future__ import unicode_literals

import courese.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courese', '0002_content_file_image_text_video'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='content',
            options={'ordering': ['order']},
        ),
        migrations.AlterModelOptions(
            name='module',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='content',
            name='order',
            field=courese.fields.OrderField(blank=True, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='module',
            name='order',
            field=courese.fields.OrderField(blank=True, default=2),
            preserve_default=False,
        ),
    ]
