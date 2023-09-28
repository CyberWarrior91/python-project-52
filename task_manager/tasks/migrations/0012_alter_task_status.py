# Generated by Django 4.2.2 on 2023-09-28 16:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('statuses', '0002_alter_status_name'),
        ('tasks', '0011_alter_task_labels'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='statuses.status', verbose_name='tatus'),
        ),
    ]
