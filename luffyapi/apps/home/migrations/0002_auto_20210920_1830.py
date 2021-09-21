# Generated by Django 2.2.2 on 2021-09-20 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='banner',
            old_name='create_time',
            new_name='created_time',
        ),
        migrations.RenameField(
            model_name='banner',
            old_name='update_time',
            new_name='updated_time',
        ),
        migrations.RemoveField(
            model_name='banner',
            name='display_order',
        ),
        migrations.AddField(
            model_name='banner',
            name='orders',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
