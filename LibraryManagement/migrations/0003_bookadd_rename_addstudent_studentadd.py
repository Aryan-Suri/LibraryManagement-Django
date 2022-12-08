# Generated by Django 4.1.4 on 2022-12-06 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LibraryManagement', '0002_alter_addstudent_studentage'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookAdd',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookName', models.CharField(max_length=20)),
                ('bookAuthor', models.CharField(max_length=20)),
                ('bookGenre', models.CharField(max_length=20)),
            ],
        ),
        migrations.RenameModel(
            old_name='AddStudent',
            new_name='StudentAdd',
        ),
    ]