# Generated by Django 2.2.5 on 2019-10-12 12:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appOne', '0014_auto_20191007_1243'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='can_start',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='chapter',
            name='end_datetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='ChapterTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=20)),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appOne.Chapter')),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='joined_teams',
            field=models.ManyToManyField(to='appOne.ChapterTeam'),
        ),
    ]