# Generated by Django 4.2.5 on 2023-11-08 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subida',
            name='image',
            field=models.ImageField(null=True, upload_to='upload'),
        ),
    ]