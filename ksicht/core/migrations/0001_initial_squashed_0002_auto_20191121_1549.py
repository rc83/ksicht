# Generated by Django 2.2.7 on 2019-11-21 15:55

import cuser.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import ksicht.core.models
import uuid


class Migration(migrations.Migration):

    replaces = [('core', '0001_initial'), ('core', '0002_auto_20191121_1549')]

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(error_messages={'unique': 'A user with that email address already exists.'}, max_length=254, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', cuser.models.CUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('school_year', models.CharField(db_index=True, default=ksicht.core.models.default_grade_school_year, max_length=50, unique=True, verbose_name='Školní rok')),
                ('errata', models.TextField(blank=True, verbose_name='Errata')),
                ('start_date', models.DateField(db_index=True, default=ksicht.core.models.default_grade_start, verbose_name='Začíná')),
                ('end_date', models.DateField(db_index=True, default=ksicht.core.models.default_grade_end, verbose_name='Končí')),
            ],
            options={
                'verbose_name': 'Ročník',
                'verbose_name_plural': 'Ročníky',
                'ordering': ('-end_date',),
            },
        ),
        migrations.CreateModel(
            name='GradeApplication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Grade')),
            ],
            options={
                'verbose_name': 'Přihláška do ročníku',
                'verbose_name_plural': 'Přihlášky do ročníku',
            },
        ),
        migrations.CreateModel(
            name='GradeSeries',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('series', models.CharField(choices=[('1', '1.'), ('2', '2.'), ('3', '3.'), ('4', '4.')], db_index=True, max_length=1, verbose_name='Série')),
                ('submission_deadline', models.DateTimeField(verbose_name='Deadline pro odeslání řešení')),
                ('task_file', models.FileField(blank=True, null=True, upload_to='rocniky/zadani/', verbose_name='Brožura')),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='series', to='core.Grade', verbose_name='Ročník')),
            ],
            options={
                'verbose_name': 'Série',
                'verbose_name_plural': 'Série',
                'ordering': ('grade', 'series'),
                'unique_together': {('grade', 'series')},
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nr', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], db_index=True, max_length=1, verbose_name='Číslo')),
                ('title', models.CharField(max_length=150, verbose_name='Název')),
                ('points', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Max. počet bodů')),
                ('series', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tasks', to='core.GradeSeries', verbose_name='Série')),
            ],
            options={
                'verbose_name': 'Úloha',
                'verbose_name_plural': 'Úlohy',
                'ordering': ('series', 'nr'),
                'unique_together': {('series', 'nr')},
            },
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='participant_profile', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('phone', models.CharField(max_length=20, null=True, verbose_name='Telefon')),
                ('street', models.CharField(max_length=100, verbose_name='Ulice')),
                ('city', models.CharField(max_length=100, verbose_name='Obec')),
                ('zip_code', models.CharField(max_length=10, verbose_name='PSČ')),
                ('country', models.CharField(choices=[('other', '-- jiný --'), ('cz', 'Česko'), ('sk', 'Slovensko')], max_length=10, verbose_name='Stát')),
                ('school', models.CharField(choices=[('--jiná--', '-- jiná --'), ('gypce', 'Gymnázium Dašická, Pardubice')], max_length=80, verbose_name='Škola')),
                ('school_year', models.CharField(choices=[('4', '4'), ('3', '3'), ('2', '2'), ('1', '1'), ('l', 'nižší')], max_length=1, verbose_name='Ročník')),
                ('school_alt_name', models.CharField(blank=True, max_length=80, null=True, verbose_name='Název školy')),
                ('school_alt_street', models.CharField(blank=True, max_length=100, null=True, verbose_name='Ulice školy')),
                ('school_alt_city', models.CharField(blank=True, max_length=100, null=True, verbose_name='Obec školy')),
                ('school_alt_zip_code', models.CharField(blank=True, max_length=10, null=True, verbose_name='PSČ školy')),
                ('applications', models.ManyToManyField(blank=True, related_name='participants', through='core.GradeApplication', to='core.Grade', verbose_name='Přihlášky')),
            ],
            options={
                'verbose_name': 'Řešitel',
                'verbose_name_plural': 'Řešitelé',
            },
        ),
        migrations.AddField(
            model_name='gradeapplication',
            name='participant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.Participant'),
        ),
        migrations.CreateModel(
            name='TaskSolutionSubmission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='rocniky/reseni/', verbose_name='Soubor s řešením')),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solution_submissions', to='core.GradeApplication', verbose_name='Přihláška')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='solution_submissions', to='core.Task', verbose_name='Úloha')),
            ],
            options={
                'permissions': (('change_solution_submission_presence', 'Úprava stavu odevzdání řešení'),),
                'verbose_name': 'Odevzdané řešení',
                'verbose_name_plural': 'Odevzdaná řešení',
            },
        ),
    ]