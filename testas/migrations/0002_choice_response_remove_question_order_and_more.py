# Generated by Django 4.2.7 on 2023-12-07 12:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('testas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(choices=[(1, 'Strongly disagree'), (2, 'Disagree'), (3, 'Neutral'), (4, 'Agree'), (5, 'Strongly agree')])),
            ],
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testas.choice')),
            ],
        ),
        migrations.RemoveField(
            model_name='question',
            name='order',
        ),
        migrations.RemoveField(
            model_name='question',
            name='test',
        ),
        migrations.AlterField(
            model_name='question',
            name='text',
            field=models.CharField(max_length=255),
        ),
        migrations.DeleteModel(
            name='Answer',
        ),
        migrations.DeleteModel(
            name='Test',
        ),
        migrations.AddField(
            model_name='response',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testas.question'),
        ),
        migrations.AddField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testas.question'),
        ),
    ]
