# Generated by Django 5.1.1 on 2024-09-15 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='preview',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='lesson_previews/'),
        ),
    ]
