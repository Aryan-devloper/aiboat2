from django.contrib import admin
from django.shortcuts import render, redirect
from django.urls import path
from django.contrib import messages
from django.utils import timezone
from .models import City, Boat, MenuEntry, ExcelUpload, Query
from .utils import process_excel_file


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_gujarati', 'is_active', 'boat_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'name_gujarati']
    
    def boat_count(self, obj):
        return obj.boats.count()
    boat_count.short_description = 'Number of Boats'


@admin.register(Boat)
class BoatAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_gujarati', 'city', 'boat_number', 'capacity', 'is_active']
    list_filter = ['city', 'is_active', 'created_at']
    search_fields = ['name', 'name_gujarati', 'boat_number']
    list_select_related = ['city']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'name_gujarati', 'city')
        }),
        ('Details', {
            'fields': ('boat_number', 'capacity', 'description')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


@admin.register(MenuEntry)
class MenuEntryAdmin(admin.ModelAdmin):
    list_display = ['boat', 'meal_type', 'date', 'time_from', 'time_to', 'price']
    list_filter = ['date', 'meal_type', 'boat__city', 'boat']
    search_fields = ['items', 'boat__name', 'special_note']
    date_hierarchy = 'date'
    list_select_related = ['boat', 'boat__city']
    
    fieldsets = (
        ('Boat & Meal Info', {
            'fields': ('boat', 'meal_type', 'date')
        }),
        ('Menu Details', {
            'fields': ('items', 'price', 'special_note')
        }),
        ('Timing', {
            'fields': ('time_from', 'time_to')
        }),
    )
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "boat":
            kwargs["queryset"] = Boat.objects.select_related('city').filter(is_active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(ExcelUpload)
class ExcelUploadAdmin(admin.ModelAdmin):
    list_display = ['city', 'uploaded_at', 'processed', 'records_created', 'uploaded_by']
    list_filter = ['processed', 'city', 'uploaded_at']
    readonly_fields = ['uploaded_at', 'processed', 'processed_at', 'records_created', 'error_log']
    
    fieldsets = (
        ('Upload Info', {
            'fields': ('file', 'city', 'uploaded_by')
        }),
        ('Processing Status', {
            'fields': ('processed', 'processed_at', 'records_created', 'error_log')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # New upload
            obj.uploaded_by = request.user.username
        super().save_model(request, obj, form, change)
        
        # Process the Excel file automatically
        if not obj.processed:
            try:
                records_created, error_msg = process_excel_file(obj)
                obj.records_created = records_created
                obj.processed = True
                obj.processed_at = timezone.now()
                if error_msg:
                    obj.error_log = error_msg
                obj.save()
                
                if error_msg:
                    messages.warning(request, f'File processed with warnings: {error_msg}')
                else:
                    messages.success(request, f'Successfully processed! Created {records_created} menu entries.')
            except Exception as e:
                obj.error_log = str(e)
                obj.save()
                messages.error(request, f'Error processing file: {str(e)}')


@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'short_query', 'boat', 'short_response']
    list_filter = ['timestamp', 'boat__city', 'boat']
    search_fields = ['query_text', 'response_text']
    date_hierarchy = 'timestamp'
    readonly_fields = ['timestamp']
    list_select_related = ['boat', 'boat__city']
    
    def short_query(self, obj):
        return obj.query_text[:50] + '...' if len(obj.query_text) > 50 else obj.query_text
    short_query.short_description = 'Query'
    
    def short_response(self, obj):
        return obj.response_text[:50] + '...' if len(obj.response_text) > 50 else obj.response_text
    short_response.short_description = 'Response'
