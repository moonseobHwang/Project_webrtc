# Generated by Django 3.1 on 2020-09-16 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('drone', models.CharField(max_length=50)),
                ('path', models.CharField(max_length=100)),
                ('filename', models.CharField(max_length=100)),
                ('datetime', models.DateTimeField()),
                ('ip', models.CharField(max_length=50)),
                ('latitude', models.CharField(max_length=50)),
                ('longitude', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=100)),
            ],
        ),
    ]
