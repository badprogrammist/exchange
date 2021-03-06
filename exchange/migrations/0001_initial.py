# Generated by Django 3.0.4 on 2020-03-07 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_ccy', models.CharField(choices=[('CZK', 'Czk'), ('EUR', 'Eur'), ('PLN', 'Pln'), ('USD', 'Usd')], max_length=3)),
                ('to_ccy', models.CharField(choices=[('CZK', 'Czk'), ('EUR', 'Eur'), ('PLN', 'Pln'), ('USD', 'Usd')], max_length=3)),
                ('value', models.DecimalField(decimal_places=5, max_digits=10)),
                ('dt', models.DateTimeField()),
            ],
            options={
                'unique_together': {('from_ccy', 'to_ccy')},
            },
        ),
    ]
