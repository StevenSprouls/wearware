# Generated by Django 3.1.7 on 2021-03-15 03:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FitbitAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(db_index=True, max_length=10)),
                ('is_active', models.BooleanField(default=True)),
                ('timezone', models.CharField(max_length=50)),
                ('token_type', models.CharField(blank=True, max_length=20)),
                ('refresh_token', models.CharField(blank=True, max_length=100)),
                ('access_token', models.CharField(blank=True, max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='FitbitHeartRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('second', models.IntegerField()),
                ('bpm', models.IntegerField()),
                ('timestamp', models.DateTimeField()),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='WearWareRESTAPI.fitbitaccount')),
            ],
        ),
        migrations.CreateModel(
            name='FitbitMinuteRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(db_index=True)),
                ('steps', models.IntegerField(blank=True, db_index=True, null=True)),
                ('calories', models.FloatField(blank=True, null=True)),
                ('mets', models.FloatField(blank=True, null=True)),
                ('activity_level', models.IntegerField(blank=True, null=True)),
                ('distance', models.FloatField(blank=True, null=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='WearWareRESTAPI.fitbitaccount')),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=25)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(db_index=True, max_length=100, unique=True)),
                ('sex', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('pairing_token', models.UUIDField(default=uuid.uuid4)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Study',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=150)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('comment', models.CharField(blank=True, default='', max_length=2000)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'permissions': (('view_study_data', 'View and export study data.'), ('add_subject_to_study', 'Create a new subject and add to study.')),
            },
        ),
        migrations.CreateModel(
            name='SyncRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('sync_type', models.CharField(db_index=True, max_length=100)),
                ('successful', models.BooleanField(default=True)),
                ('message', models.CharField(default='', max_length=10000)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='WearWareRESTAPI.fitbitaccount')),
            ],
        ),
        migrations.CreateModel(
            name='ParticipantData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_level', models.ManyToManyField(related_name='_participantdata_activity_level_+', to='WearWareRESTAPI.FitbitMinuteRecord')),
                ('bpm', models.ManyToManyField(related_name='_participantdata_bpm_+', to='WearWareRESTAPI.FitbitHeartRecord')),
                ('calories', models.ManyToManyField(related_name='_participantdata_calories_+', to='WearWareRESTAPI.FitbitMinuteRecord')),
                ('device', models.ManyToManyField(related_name='_participantdata_device_+', to='WearWareRESTAPI.FitbitHeartRecord')),
                ('distance', models.ManyToManyField(related_name='_participantdata_distance_+', to='WearWareRESTAPI.FitbitMinuteRecord')),
                ('mets', models.ManyToManyField(related_name='_participantdata_mets_+', to='WearWareRESTAPI.FitbitMinuteRecord')),
                ('steps', models.ManyToManyField(related_name='_participantdata_steps_+', to='WearWareRESTAPI.FitbitMinuteRecord')),
            ],
        ),
        migrations.AddField(
            model_name='fitbitaccount',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='WearWareRESTAPI.participant'),
        ),
        migrations.CreateModel(
            name='StudyHasParticipant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('data_collection_start_date', models.DateField(verbose_name='earliest date for data sync')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='WearWareRESTAPI.participant')),
                ('study', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='WearWareRESTAPI.study')),
            ],
            options={
                'unique_together': {('study', 'participant')},
            },
        ),
        migrations.CreateModel(
            name='ResearcherHasStudy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('researcher', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('study', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='WearWareRESTAPI.study')),
            ],
            options={
                'unique_together': {('researcher', 'study')},
            },
        ),
        migrations.CreateModel(
            name='FitbitSleepRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateField()),
                ('record_number', models.IntegerField()),
                ('deep_sleep_minutes', models.IntegerField(blank=True, null=True)),
                ('light_sleep_minutes', models.IntegerField(blank=True, null=True)),
                ('rem_sleep_minutes', models.IntegerField(blank=True, null=True)),
                ('awake_minutes', models.IntegerField(blank=True, null=True)),
                ('total_sleep_minutes', models.IntegerField(blank=True, null=True)),
                ('time_in_bed', models.IntegerField(blank=True, null=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='WearWareRESTAPI.fitbitaccount')),
            ],
            options={
                'unique_together': {('timestamp', 'record_number')},
            },
        ),
    ]
