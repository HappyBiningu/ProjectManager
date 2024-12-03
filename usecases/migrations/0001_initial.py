# Generated by Django 5.0.9 on 2024-11-21 15:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('requirements', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UseCase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('actors', models.TextField(help_text='List the actors involved in the use case.')),
                ('preconditions', models.TextField(help_text='Conditions that must be met before the use case begins.')),
                ('steps', models.TextField(help_text='Detailed steps of the use case.')),
                ('postconditions', models.TextField(help_text='Expected results after the use case is completed.')),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('under_review', 'Under Review'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='draft', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('requirement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='use_cases', to='requirements.requirement')),
            ],
        ),
    ]
