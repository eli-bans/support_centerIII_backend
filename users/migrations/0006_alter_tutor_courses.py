# Generated by Django 5.0.7 on 2024-08-09 04:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0005_alter_tutor_courses"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tutor",
            name="courses",
            field=models.CharField(default="", max_length=255),
        ),
    ]
