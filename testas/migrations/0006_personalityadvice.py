# Generated by Django 4.2.7 on 2023-12-12 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testas', '0005_testresult'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonalityAdvice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('personality_type', models.CharField(max_length=100, unique=True)),
                ('professional_advice', models.TextField(help_text='Advice for professional development.')),
                ('personal_advice', models.TextField(help_text='Advice for personal growth.')),
                ('growth_advice', models.TextField(help_text='Advice for overall growth and development.')),
            ],
        ),
    ]
