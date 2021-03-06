# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-08-28 16:52
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_line_1', models.CharField(max_length=200, verbose_name='Address Line 1')),
                ('address_line_2', models.CharField(blank=True, max_length=200, null=True, verbose_name='Address Line 2')),
                ('pin', models.CharField(max_length=10, verbose_name='Pin Code')),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GeneralInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fathers_name', models.CharField(max_length=200, verbose_name="Father's Name")),
                ('mothers_name', models.CharField(max_length=200, verbose_name="Mother's Name")),
                ('fathers_occupation', models.CharField(choices=[('1', 'Service'), ('2', 'Business'), ('3', 'None'), ('4', 'Gov Job')], max_length=5, verbose_name="Father's Occupation")),
                ('mothers_occupation', models.CharField(choices=[('1', 'Service'), ('2', 'Business'), ('3', 'None'), ('4', 'Gov Job'), ('5', 'Housewife')], max_length=5, verbose_name="Mother's Occupation")),
                ('religion', models.CharField(choices=[('1', 'Hindu'), ('2', 'Muslim'), ('3', 'Sikh'), ('4', 'Christian')], max_length=5, verbose_name='Religion')),
                ('nationality', models.CharField(choices=[('1', 'Indian'), ('2', 'Others')], max_length=5, verbose_name='Nationality')),
                ('has_qualified_entrance', models.BooleanField(default=False, verbose_name='Has Student qualified the entrance examination?')),
                ('thumb_impression', models.FileField(blank=True, null=True, upload_to=b'/private/var/live_code/vision/vision/uploads')),
                ('correspondence_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='correspondence_address_general_info', to='student.Address')),
                ('permanant_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='permanant_address_general_info', to='student.Address')),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='general_info', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PreviousEducationDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.CharField(max_length=50, verbose_name='Course Name')),
                ('year_of_passing', models.CharField(choices=[(b'1990', b'1990'), (b'1991', b'1991'), (b'1992', b'1992'), (b'1993', b'1993'), (b'1994', b'1994'), (b'1995', b'1995'), (b'1996', b'1996'), (b'1997', b'1997'), (b'1998', b'1998'), (b'1999', b'1999'), (b'2000', b'2000'), (b'2001', b'2001'), (b'2002', b'2002'), (b'2003', b'2003'), (b'2004', b'2004'), (b'2005', b'2005'), (b'2006', b'2006'), (b'2007', b'2007'), (b'2008', b'2008'), (b'2009', b'2009'), (b'2010', b'2010'), (b'2011', b'2011'), (b'2012', b'2012'), (b'2013', b'2013'), (b'2014', b'2014'), (b'2015', b'2015'), (b'2016', b'2016'), (b'2017', b'2017')], max_length=50, verbose_name='Course Name')),
                ('board_or_university', models.CharField(max_length=200, verbose_name='Board or University')),
                ('college_name', models.CharField(max_length=200, verbose_name='College Name')),
                ('result', models.CharField(choices=[('1', 'Pass'), ('2', 'Fail')], max_length=50, verbose_name='Result')),
                ('percentage', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Result')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='education_details', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='states', to='student.Country')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='district',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='districts', to='student.State'),
        ),
        migrations.AddField(
            model_name='address',
            name='district',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students_addresses', to='student.District'),
        ),
    ]
