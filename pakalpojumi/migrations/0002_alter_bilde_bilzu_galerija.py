# Generated by Django 4.0.4 on 2022-06-19 19:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pakalpojumi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bilde',
            name='bilzu_galerija',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pakalpojumi.bilzugalerija', verbose_name='bilžu galerija'),
        ),
    ]
