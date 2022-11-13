# Generated by Django 4.0.2 on 2022-03-25 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_delete_details'),
    ]

    operations = [
        migrations.CreateModel(
            name='upload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=300, unique=True)),
                ('description', models.TextField()),
                ('file', models.FileField(upload_to='')),
            ],
        ),
    ]
