# Generated by Django 5.1.1 on 2024-09-26 15:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_rename_name_articletag_tag'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ArticleScope',
            new_name='Scope',
        ),
        migrations.RenameModel(
            old_name='ArticleTag',
            new_name='Tag',
        ),
        migrations.RenameField(
            model_name='tag',
            old_name='tag',
            new_name='name',
        ),
    ]