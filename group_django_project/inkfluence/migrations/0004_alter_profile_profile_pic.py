# Generated by Django 5.0.2 on 2024-03-13 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inkfluence', '0003_alter_profile_genre_likes_alter_profile_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, default='default.png', upload_to='C:/files/profile_pics'),
        ),
    ]
