# Generated by Django 2.2.5 on 2019-10-05 15:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appOne', '0006_student'),
    ]

    operations = [
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('userprofileinfo_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='appOne.UserProfileInfo')),
                ('prof_title', models.CharField(max_length=30)),
            ],
            bases=('appOne.userprofileinfo',),
        ),
    ]
