# Generated by Django 3.2.13 on 2023-09-19 11:53

from django.db import migrations, models


def move_name_in_variable(apps, schema_editor):
    TowerSurveyField = apps.get_model('service_catalog', 'TowerSurveyField')
    for survey_field in TowerSurveyField.objects.all():
        survey_field.variable = survey_field.name
        survey_field.name = ""
        survey_field.save()


class Migration(migrations.Migration):
    dependencies = [
        ('service_catalog', '0025_alter_approvalstep_auto_accept_condition'),
    ]

    operations = [
        migrations.AddField(
            model_name='towersurveyfield',
            name='description',
            field=models.CharField(default='', max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='towersurveyfield',
            name='field_options',
            field=models.JSONField(default={}),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='towersurveyfield',
            name='required',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='towersurveyfield',
            name='type',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='towersurveyfield',
            name='variable',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.RunPython(move_name_in_variable),
        migrations.AlterField(
            model_name='towersurveyfield',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterUniqueTogether(
            name='towersurveyfield',
            unique_together={('operation', 'variable')},
        ),
        migrations.AlterField(
            model_name='towersurveyfield',
            name='is_customer_field',
            field=models.BooleanField(default=True, help_text='Display for non approver user'),
        ),
    ]