# Generated by Django 3.1.7 on 2021-08-19 13:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resource_tracker', '004_over_commitment_ratio'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResourceGroupTextAttributeDefinition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('resource_group_definition', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='text_attribute_definitions', related_query_name='text_attribute_definition', to='resource_tracker.resourcegroup')),
            ],
            options={
                'unique_together': {('name', 'resource_group_definition')},
            },
        ),
        migrations.CreateModel(
            name='ResourceTextAttribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(default='', max_length=500)),
                ('resource', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='text_attributes', related_query_name='text_attribute', to='resource_tracker.resource')),
                ('text_attribute_type', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='text_attribute_types', related_query_name='text_attribute_type', to='resource_tracker.resourcegrouptextattributedefinition')),
            ],
        ),
    ]