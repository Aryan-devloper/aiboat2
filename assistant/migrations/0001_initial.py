# Generated migrations for assistant app

from django.db import migrations, models
import django.db.models.deletion
import django.core.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('name_gujarati', models.CharField(help_text='City name in Gujarati', max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'City',
                'verbose_name_plural': 'Cities',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Boat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('name_gujarati', models.CharField(help_text='Boat name in Gujarati', max_length=100)),
                ('boat_number', models.CharField(blank=True, max_length=50)),
                ('capacity', models.IntegerField(default=0, help_text='Number of passengers')),
                ('is_active', models.BooleanField(default=True)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='boats', to='assistant.city')),
            ],
            options={
                'verbose_name': 'Boat',
                'verbose_name_plural': 'Boats',
                'ordering': ['city', 'name'],
                'unique_together': {('name', 'city')},
            },
        ),
        migrations.CreateModel(
            name='MenuEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meal_type', models.CharField(choices=[('નાસ્તો', 'Breakfast'), ('બપોર', 'Lunch'), ('રાત', 'Dinner')], max_length=50)),
                ('items', models.TextField(help_text='Menu items separated by commas')),
                ('time_from', models.TimeField()),
                ('time_to', models.TimeField()),
                ('date', models.DateField()),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('special_note', models.TextField(blank=True, help_text='Special notes in Gujarati')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('boat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menus', to='assistant.boat')),
            ],
            options={
                'verbose_name': 'Menu Entry',
                'verbose_name_plural': 'Menu Entries',
                'ordering': ['-date', 'time_from'],
                'unique_together': {('boat', 'meal_type', 'date')},
            },
        ),
        migrations.CreateModel(
            name='ExcelUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='menu_uploads/%Y/%m/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['xlsx', 'xls'])])),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('processed', models.BooleanField(default=False)),
                ('processed_at', models.DateTimeField(blank=True, null=True)),
                ('records_created', models.IntegerField(default=0)),
                ('error_log', models.TextField(blank=True)),
                ('uploaded_by', models.CharField(blank=True, max_length=100)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uploads', to='assistant.city')),
            ],
            options={
                'verbose_name': 'Excel Upload',
                'verbose_name_plural': 'Excel Uploads',
                'ordering': ['-uploaded_at'],
            },
        ),
        migrations.CreateModel(
            name='Query',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query_text', models.TextField()),
                ('response_text', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('boat', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='assistant.boat')),
            ],
            options={
                'verbose_name': 'User Query',
                'verbose_name_plural': 'User Queries',
                'ordering': ['-timestamp'],
            },
        ),
    ]
