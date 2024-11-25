# Generated by Django 5.1.1 on 2024-10-02 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AddBooks',
            fields=[
                ('bookid', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=100)),
                ('published_date', models.DateField()),
                ('isbn', models.CharField(max_length=13, unique=True)),
            ],
        ),
    ]
