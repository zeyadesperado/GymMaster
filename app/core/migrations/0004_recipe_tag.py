# Generated by Django 3.2.24 on 2024-03-08 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='tag',
            field=models.ManyToManyField(to='core.Tag'),
        ),
    ]
