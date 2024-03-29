# Generated by Django 5.0.2 on 2024-03-13 13:20

import multiselectfield.db.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inkfluence', '0002_profile_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='genre_likes',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('FAN', 'Fantasy'), ('SCF', 'Sci-Fi'), ('ACT', 'Action & Adventure'), ('MYS', 'Mystery'), ('HOR', 'Horror'), ('THR', 'Thriller & Crime'), ('HIS', 'Historical Fiction'), ('ROM', 'Romance'), ('COM', 'Comedy'), ('YA', 'Young Adult'), ('CHI', 'Children')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, default='default.png', upload_to='group_django_project/files/profile_pics'),
        ),
    ]
