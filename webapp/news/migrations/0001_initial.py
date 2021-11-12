# Generated by Django 3.2 on 2021-11-08 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=255)),
                ('body', models.CharField(max_length=10000, null=True)),
                ('external', models.URLField(null=True)),
                ('supporters', models.ManyToManyField(to='events.Supporter')),
                ('tags', models.ManyToManyField(to='events.Tag')),
            ],
        ),
    ]
