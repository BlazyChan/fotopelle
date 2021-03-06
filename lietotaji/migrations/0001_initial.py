# Generated by Django 4.0.4 on 2022-06-19 17:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import lietotaji.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lietotajs',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('epasts', models.EmailField(max_length=64, primary_key=True, serialize=False, verbose_name='e-pasts')),
                ('is_active', models.BooleanField(default=True, verbose_name='ir aktīvs')),
                ('is_admin', models.BooleanField(default=False, verbose_name='ir administrators')),
                ('is_staff', models.BooleanField(default=False, verbose_name='ir personāls')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='ir superlietotājs')),
                ('vards', models.CharField(max_length=32, verbose_name='vārds')),
                ('uzvards', models.CharField(max_length=32, verbose_name='uzvārds')),
                ('telefona_numurs', models.CharField(max_length=15)),
                ('profila_bilde', models.ImageField(default='profila_bilde/noklusējuma_profila_bilde.png', upload_to=lietotaji.models.lietotaja_profila_bildes_cels)),
            ],
            options={
                'verbose_name': 'Lietotājs',
                'verbose_name_plural': 'Lietotāji',
            },
        ),
        migrations.CreateModel(
            name='Fotografs',
            fields=[
                ('lietotajs', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='lietotājs')),
                ('apraksts', models.TextField()),
            ],
            options={
                'verbose_name': 'Fotogrāfs',
                'verbose_name_plural': 'Fotogrāfi',
            },
        ),
    ]
