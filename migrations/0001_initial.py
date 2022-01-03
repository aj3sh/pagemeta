# Generated by Django 3.2.2 on 2022-01-03 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MetaForPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_url', models.CharField(max_length=255, verbose_name='Page Url')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('description', models.CharField(max_length=255, verbose_name='Description')),
                ('image', models.ImageField(upload_to='', verbose_name='Image')),
                ('keywords', models.CharField(blank=True, max_length=255, null=True, verbose_name='Keywords')),
            ],
        ),
    ]
