# Generated by Django 5.2.4 on 2025-07-22 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_remove_article_category_article_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='source',
            field=models.CharField(default='Unknown', max_length=100),
        ),
    ]
