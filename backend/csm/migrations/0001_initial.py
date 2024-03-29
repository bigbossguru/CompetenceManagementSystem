# Generated by Django 3.2.13 on 2022-05-07 22:55

from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('is_regular_employee', models.BooleanField(default=True)),
                ('is_manager', models.BooleanField(default=False)),
                ('is_local_hr', models.BooleanField(default=False)),
                ('is_regional_hr', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AACompetence',
            fields=[
                ('code', models.CharField(max_length=6, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250)),
                ('weight', models.PositiveSmallIntegerField(default=5)),
            ],
        ),
        migrations.CreateModel(
            name='CareerAspiration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_date', models.DateField(null=True)),
                ('to_date', models.DateField(null=True)),
                ('current_stage', models.CharField(max_length=250, null=True)),
                ('stay_current_position', models.CharField(max_length=50, null=True)),
                ('expertise', models.CharField(max_length=50, null=True)),
                ('eligibility', models.CharField(max_length=50, null=True)),
                ('current_salary', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('new_salary', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('increase_proposal', models.CharField(max_length=50, null=True)),
                ('budget', models.CharField(max_length=50, null=True)),
                ('risk_resignation', models.CharField(max_length=50, null=True)),
                ('comments', models.TextField(blank=True, null=True)),
                ('create_date', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='CostCenter',
            fields=[
                ('code', models.CharField(max_length=6, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('ps_id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('person_id', models.PositiveIntegerField(null=True)),
                ('first_name', models.CharField(max_length=50, null=True)),
                ('last_name', models.CharField(max_length=50, null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('cadre', models.CharField(max_length=50, null=True)),
                ('full_part_time', models.CharField(max_length=50, null=True)),
                ('fte', models.DecimalField(decimal_places=1, default=0.0, max_digits=3)),
                ('type_of_contract', models.CharField(max_length=50, null=True)),
                ('location', models.CharField(max_length=50, null=True)),
                ('orgaloc', models.CharField(max_length=7, null=True)),
                ('start_date', models.DateField(null=True)),
                ('bg', models.CharField(max_length=50, null=True)),
                ('pg', models.CharField(max_length=50, null=True)),
                ('pl', models.CharField(max_length=50, null=True)),
                ('tpl', models.CharField(max_length=50, null=True)),
                ('status', models.BooleanField(default=True)),
                ('create_date', models.DateTimeField(auto_now=True)),
                ('cc', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='csm.costcenter')),
                ('fn1', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fn1s', to='csm.employee')),
                ('hn1', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hn1s', to='csm.employee')),
                ('hn2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hn2s', to='csm.employee')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeAACompetence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appraisal_id', models.CharField(max_length=50, null=True)),
                ('year', models.IntegerField(null=True)),
                ('from_date', models.DateField(null=True)),
                ('to_date', models.DateField(null=True)),
                ('interview_date', models.DateField(null=True)),
                ('stage', models.CharField(max_length=50, null=True)),
                ('status', models.CharField(max_length=50, null=True)),
                ('rating', models.CharField(max_length=50, null=True)),
                ('expected_lvl', models.CharField(max_length=50, null=True)),
                ('create_date', models.DateField(auto_now_add=True)),
                ('competence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aa_competences', to='csm.aacompetence')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aa_employees', to='csm.employee')),
            ],
            options={
                'ordering': ['-create_date'],
            },
        ),
        migrations.CreateModel(
            name='EmployeeRDCompetence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expected_lvl', models.SmallIntegerField(default=0)),
                ('manager_expected_lvl', models.SmallIntegerField(default=0)),
                ('acquired_lvl', models.SmallIntegerField(default=0)),
                ('gap', models.SmallIntegerField(default=0)),
                ('coverage', models.FloatField(default=0)),
                ('create_date', models.DateField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-create_date'],
            },
        ),
        migrations.CreateModel(
            name='FilesDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=250)),
                ('start_header', models.PositiveSmallIntegerField()),
                ('required', models.BooleanField(default=True)),
                ('file_upload', models.FileField(null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='FullAACompetence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appraisal_id', models.CharField(max_length=50, null=True)),
                ('from_date', models.DateField(null=True)),
                ('to_date', models.DateField(null=True)),
                ('interview_date', models.DateField(null=True)),
                ('stage', models.CharField(max_length=50, null=True)),
                ('status', models.CharField(max_length=50, null=True)),
                ('date_completed_on', models.DateField(null=True)),
                ('next_date_career_discus', models.DateField(null=True)),
                ('performance', models.CharField(max_length=50, null=True)),
                ('trend', models.CharField(max_length=50, null=True)),
                ('category', models.CharField(max_length=50, null=True)),
                ('level', models.CharField(max_length=50, null=True)),
                ('key_specific_obj', models.CharField(max_length=50, null=True)),
                ('general_mission', models.CharField(max_length=50, null=True)),
                ('demonstrated_behavior', models.CharField(max_length=50, null=True)),
                ('leadership', models.CharField(max_length=50, null=True)),
                ('comments', models.TextField(null=True)),
                ('create_date', models.DateTimeField(auto_now=True)),
                ('employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='fullaa_employees', to='csm.employee')),
            ],
            options={
                'ordering': ['-create_date'],
            },
        ),
        migrations.CreateModel(
            name='Hyperion',
            fields=[
                ('code', models.CharField(max_length=7, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250, null=True)),
                ('function', models.CharField(max_length=250, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MetierField',
            fields=[
                ('metier_field_id', models.PositiveSmallIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250)),
                ('bg', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('platform_id', models.PositiveSmallIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='RDCompetence',
            fields=[
                ('competence_id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250)),
                ('type', models.CharField(max_length=250)),
                ('metier_org', models.CharField(max_length=250)),
                ('category', models.CharField(max_length=250)),
                ('domain', models.CharField(max_length=250)),
                ('weight', models.PositiveSmallIntegerField(default=5)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceEmail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='UserAccessReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('is_access', models.BooleanField(default=False)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SystemConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_update_datetime', models.DateTimeField()),
                ('end_update_datetime', models.DateTimeField()),
                ('files_detail', models.ManyToManyField(to='csm.FilesDetail')),
                ('service_emails', models.ManyToManyField(to='csm.ServiceEmail')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='JobProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=6)),
                ('jobtitle', models.CharField(max_length=250)),
                ('metier_field', models.CharField(max_length=250, null=True)),
                ('metier', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='job_prof_metiers', to='csm.employee')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalFullAACompetence',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('appraisal_id', models.CharField(max_length=50, null=True)),
                ('from_date', models.DateField(null=True)),
                ('to_date', models.DateField(null=True)),
                ('interview_date', models.DateField(null=True)),
                ('stage', models.CharField(max_length=50, null=True)),
                ('status', models.CharField(max_length=50, null=True)),
                ('date_completed_on', models.DateField(null=True)),
                ('next_date_career_discus', models.DateField(null=True)),
                ('performance', models.CharField(max_length=50, null=True)),
                ('trend', models.CharField(max_length=50, null=True)),
                ('category', models.CharField(max_length=50, null=True)),
                ('level', models.CharField(max_length=50, null=True)),
                ('key_specific_obj', models.CharField(max_length=50, null=True)),
                ('general_mission', models.CharField(max_length=50, null=True)),
                ('demonstrated_behavior', models.CharField(max_length=50, null=True)),
                ('leadership', models.CharField(max_length=50, null=True)),
                ('comments', models.TextField(null=True)),
                ('create_date', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('employee', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='csm.employee')),
                ('history_relation', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='history_fullaa_competence', to='csm.fullaacompetence')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical full aa competence',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalEmployeeRDCompetence',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('expected_lvl', models.SmallIntegerField(default=0)),
                ('manager_expected_lvl', models.SmallIntegerField(default=0)),
                ('acquired_lvl', models.SmallIntegerField(default=0)),
                ('gap', models.SmallIntegerField(default=0)),
                ('coverage', models.FloatField(default=0)),
                ('create_date', models.DateField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('competence', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='csm.rdcompetence')),
                ('employee', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='csm.employee')),
                ('history_relation', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='history_rd_competence', to='csm.employeerdcompetence')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('metier_field', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='csm.metierfield')),
                ('platform', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='csm.platform')),
            ],
            options={
                'verbose_name': 'historical employee rd competence',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalEmployeeAACompetence',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('appraisal_id', models.CharField(max_length=50, null=True)),
                ('year', models.IntegerField(null=True)),
                ('from_date', models.DateField(null=True)),
                ('to_date', models.DateField(null=True)),
                ('interview_date', models.DateField(null=True)),
                ('stage', models.CharField(max_length=50, null=True)),
                ('status', models.CharField(max_length=50, null=True)),
                ('rating', models.CharField(max_length=50, null=True)),
                ('expected_lvl', models.CharField(max_length=50, null=True)),
                ('create_date', models.DateField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('competence', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='csm.aacompetence')),
                ('employee', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='csm.employee')),
                ('history_relation', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='history_aa_competence', to='csm.employeeaacompetence')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical employee aa competence',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalEmployee',
            fields=[
                ('ps_id', models.PositiveIntegerField(db_index=True)),
                ('person_id', models.PositiveIntegerField(null=True)),
                ('first_name', models.CharField(max_length=50, null=True)),
                ('last_name', models.CharField(max_length=50, null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('cadre', models.CharField(max_length=50, null=True)),
                ('full_part_time', models.CharField(max_length=50, null=True)),
                ('fte', models.DecimalField(decimal_places=1, default=0.0, max_digits=3)),
                ('type_of_contract', models.CharField(max_length=50, null=True)),
                ('location', models.CharField(max_length=50, null=True)),
                ('orgaloc', models.CharField(max_length=7, null=True)),
                ('start_date', models.DateField(null=True)),
                ('bg', models.CharField(max_length=50, null=True)),
                ('pg', models.CharField(max_length=50, null=True)),
                ('pl', models.CharField(max_length=50, null=True)),
                ('tpl', models.CharField(max_length=50, null=True)),
                ('status', models.BooleanField(default=True)),
                ('create_date', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('cc', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='csm.costcenter')),
                ('fn1', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='csm.employee')),
                ('history_relation', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='history_employee', to='csm.employee')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('hn1', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='csm.employee')),
                ('hn2', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='csm.employee')),
                ('hyperion', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='csm.hyperion')),
                ('job', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='csm.jobprofile')),
            ],
            options={
                'verbose_name': 'historical employee',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalCareerAspiration',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('from_date', models.DateField(null=True)),
                ('to_date', models.DateField(null=True)),
                ('current_stage', models.CharField(max_length=250, null=True)),
                ('stay_current_position', models.CharField(max_length=50, null=True)),
                ('expertise', models.CharField(max_length=50, null=True)),
                ('eligibility', models.CharField(max_length=50, null=True)),
                ('current_salary', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('new_salary', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('increase_proposal', models.CharField(max_length=50, null=True)),
                ('budget', models.CharField(max_length=50, null=True)),
                ('risk_resignation', models.CharField(max_length=50, null=True)),
                ('comments', models.TextField(blank=True, null=True)),
                ('create_date', models.DateField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('employee', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='csm.employee')),
                ('history_relation', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='history_ca', to='csm.careeraspiration')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('successor1', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='csm.employee')),
                ('successor2', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='csm.employee')),
                ('successor3', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='csm.employee')),
            ],
            options={
                'verbose_name': 'historical career aspiration',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.AddField(
            model_name='employeerdcompetence',
            name='competence',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rd_competences', to='csm.rdcompetence'),
        ),
        migrations.AddField(
            model_name='employeerdcompetence',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rd_employees', to='csm.employee'),
        ),
        migrations.AddField(
            model_name='employeerdcompetence',
            name='metier_field',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='csm.metierfield'),
        ),
        migrations.AddField(
            model_name='employeerdcompetence',
            name='platform',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='csm.platform'),
        ),
        migrations.AddField(
            model_name='employee',
            name='hyperion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='csm.hyperion'),
        ),
        migrations.AddField(
            model_name='employee',
            name='job',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='csm.jobprofile'),
        ),
        migrations.AddField(
            model_name='costcenter',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cc_employees', to='csm.employee'),
        ),
        migrations.AddField(
            model_name='careeraspiration',
            name='employee',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ca_employees', to='csm.employee'),
        ),
        migrations.AddField(
            model_name='careeraspiration',
            name='successor1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='successors1', to='csm.employee'),
        ),
        migrations.AddField(
            model_name='careeraspiration',
            name='successor2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='successors2', to='csm.employee'),
        ),
        migrations.AddField(
            model_name='careeraspiration',
            name='successor3',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='successors3', to='csm.employee'),
        ),
        migrations.AddConstraint(
            model_name='employeerdcompetence',
            constraint=models.UniqueConstraint(fields=('employee', 'competence'), name='employee_rdcompet'),
        ),
        migrations.AlterUniqueTogether(
            name='employeerdcompetence',
            unique_together={('employee', 'competence')},
        ),
        migrations.AddConstraint(
            model_name='employeeaacompetence',
            constraint=models.UniqueConstraint(fields=('employee', 'competence'), name='employee_aacompet'),
        ),
        migrations.AlterUniqueTogether(
            name='employeeaacompetence',
            unique_together={('employee', 'competence')},
        ),
    ]
