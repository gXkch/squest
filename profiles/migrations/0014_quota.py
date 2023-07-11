# Generated by Django 3.2.13 on 2023-06-29 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resource_tracker_v2', '0002_initial'),
        ('profiles', '0013_delete_billinggroup'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quota',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('limit', models.PositiveIntegerField(default=0)),
                ('attribute_definition', models.ForeignKey(help_text='The attribute definitions linked to this quota.', on_delete=django.db.models.deletion.CASCADE, related_name='quotas', related_query_name='quota', to='resource_tracker_v2.attributedefinition', verbose_name='Quota')),
                ('scope', models.ForeignKey(help_text='The attribute definitions linked to this quota.', on_delete=django.db.models.deletion.CASCADE, related_name='quotas', related_query_name='quota', to='profiles.scope', verbose_name='Quota')),
            ],
            options={
                'unique_together': {('scope', 'attribute_definition')},
            },
        ),
    ]