# Generated by Django 2.2.5 on 2019-10-12 12:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appOne', '0014_auto_20191007_1243'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='professor',
            name='prof_title',
        ),
    ]