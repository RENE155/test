# Generated by Django 4.2.7 on 2023-12-13 08:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testas', '0007_remove_response_user_remove_testresult_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Response',
        ),
    ]
