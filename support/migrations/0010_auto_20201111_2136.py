# Generated by Django 3.1.3 on 2020-11-11 16:06

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0009_delete_requeststatus'),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
            ],
        ),
        migrations.AlterField(
            model_name='raiserequest',
            name='description',
            field=models.CharField(max_length=400, validators=[django.core.validators.MinLengthValidator(30)]),
        ),
        migrations.AlterField(
            model_name='raiserequest',
            name='issue',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='support.issue'),
        ),
        migrations.AlterUniqueTogether(
            name='raiserequest',
            unique_together={('email', 'issue')},
        ),
    ]
