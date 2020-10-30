# Generated by Django 3.1.2 on 2020-10-29 22:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalogue', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid_from', models.DateTimeField(help_text='Time Stamp after which booking is valid.')),
                ('applicable_base_rental_rate', models.FloatField(help_text='Applicable Base Rental Rate at which the booking was done.')),
                ('applicable_par_kilometer_price', models.FloatField(help_text='Applicable Par Kilometer Price at which the booking was done.')),
                ('booking_number', models.CharField(help_text='A human readable unique identifier this booking.', max_length=10, unique=True)),
                ('initial_milage', models.FloatField(help_text='Represents the initial milage of the car at the time of booking.')),
                ('last_milage', models.FloatField(help_text='Represents the last milage of the car at return.', null=True)),
                ('returned_at', models.DateTimeField(help_text='Time Stamp at which the car was returned and booking was closed.', null=True)),
                ('payable_amount', models.FloatField(help_text='Total Payable Amount for this booking.', null=True)),
                ('car', models.ForeignKey(help_text='Car for which this booking is done.', on_delete=django.db.models.deletion.PROTECT, related_name='bookings', to='catalogue.car')),
                ('customer', models.ForeignKey(help_text='Customer who owns this booking.', on_delete=django.db.models.deletion.PROTECT, related_name='bookings_owned', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
