# Generated by Django 4.2.3 on 2023-07-08 21:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Usuario",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nome", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Email",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("endereco", models.EmailField(max_length=254)),
                (
                    "usuario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="investorapp.usuario",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Ativo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nome", models.CharField(max_length=100)),
                ("tempo_verificacao", models.PositiveIntegerField()),
                (
                    "limite_superior",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                (
                    "limite_inferior",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                (
                    "usuario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="investorapp.usuario",
                    ),
                ),
            ],
        ),
    ]
