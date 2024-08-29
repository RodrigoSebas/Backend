# Generated by Django 5.1 on 2024-08-23 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0001_creacion_tablas_usuarios'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='tipoUsuario',
            field=models.TextField(choices=[('NOVIO', 'NOVIO'), ('INVITADO', 'INVITADO'), ('ADMIN', 'ADMIN')], db_column='tipo_usuario'),
        ),
    ]
