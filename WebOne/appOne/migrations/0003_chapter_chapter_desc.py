# Generated by Django 2.2.5 on 2019-10-03 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appOne', '0002_chapter_module'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='chapter_desc',
            field=models.CharField(default='Description', max_length=100),
        ),
    ]
