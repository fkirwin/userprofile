# Generated by Django 2.1 on 2018-10-14 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20181013_2119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='C:/TreehouseProjects/userprofile/user_profile/assets/images/'),
        ),
    ]
