# Generated by Django 4.2 on 2023-05-04 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_complaint_complaint_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='complaint',
            name='result',
        ),
        migrations.AlterField(
            model_name='complaint',
            name='list_docs',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
