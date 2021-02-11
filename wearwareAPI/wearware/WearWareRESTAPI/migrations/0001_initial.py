# Generated by Django 3.1.6 on 2021-02-11 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('participant_id', models.IntegerField(primary_key=True, serialize=False)),
                ('subscriber_id', models.IntegerField(blank=True, null=True)),
                ('device_model', models.CharField(blank=True, max_length=20, null=True)),
                ('device_version', models.CharField(blank=True, max_length=20, null=True)),
                ('device_status', models.CharField(blank=True, max_length=20, null=True)),
                ('last_logged_activity', models.DateTimeField(blank=True, null=True)),
                ('email', models.CharField(blank=True, max_length=20, null=True)),
                ('join_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'participant',
            },
        ),
        migrations.CreateModel(
            name='Researcher',
            fields=[
                ('researcher_id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.CharField(blank=True, max_length=20, null=True)),
                ('permissions', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'db_table': 'researcher',
            },
        ),
        migrations.CreateModel(
            name='Study',
            fields=[
                ('study_id', models.IntegerField(primary_key=True, serialize=False)),
                ('study_title', models.CharField(blank=True, max_length=20, null=True)),
                ('short_name', models.CharField(blank=True, max_length=20, null=True)),
                ('study_desc', models.CharField(blank=True, max_length=20, null=True)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('study_url', models.CharField(blank=True, max_length=20, null=True)),
                ('researcher_id', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'study',
            },
        ),
        migrations.CreateModel(
            name='SleepData',
            fields=[
                ('participant_id', models.IntegerField(primary_key=True, serialize=False)),
                ('datetime', models.DateTimeField()),
                ('light_sleep', models.IntegerField(blank=True, null=True)),
                ('rem', models.IntegerField(blank=True, null=True)),
                ('restless', models.IntegerField(blank=True, null=True)),
                ('deep_sleep', models.IntegerField(blank=True, null=True)),
                ('wake', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'sleep_data',
                'unique_together': {('participant_id', 'datetime')},
            },
        ),
        migrations.CreateModel(
            name='ResearcherStudy',
            fields=[
                ('researcher_id', models.IntegerField(primary_key=True, serialize=False)),
                ('study_id', models.IntegerField()),
            ],
            options={
                'db_table': 'researcher_study',
                'unique_together': {('researcher_id', 'study_id')},
            },
        ),
        migrations.CreateModel(
            name='ParticipantStudy',
            fields=[
                ('participant_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('study_id', models.IntegerField()),
                ('partipant_id_pk', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'db_table': 'participant_study',
                'unique_together': {('participant_id', 'study_id')},
            },
        ),
        migrations.CreateModel(
            name='HeartRate',
            fields=[
                ('participant_id', models.IntegerField(primary_key=True, serialize=False)),
                ('datetime', models.DateTimeField()),
                ('bpm', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'heart_rate',
                'unique_together': {('participant_id', 'datetime')},
            },
        ),
        migrations.CreateModel(
            name='ActivityLevel',
            fields=[
                ('participant_id', models.IntegerField(primary_key=True, serialize=False)),
                ('datetime', models.DateTimeField()),
                ('activity_level', models.IntegerField(blank=True, null=True)),
                ('steps', models.IntegerField(blank=True, null=True)),
                ('mets', models.FloatField(blank=True, null=True)),
                ('calories', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'activity_level',
                'unique_together': {('participant_id', 'datetime')},
            },
        ),
    ]
