from django.db import models
from django.core.validators import FileExtensionValidator


class City(models.Model):
    """Model for storing cities where boats operate."""
    name = models.CharField(max_length=100, unique=True)
    name_gujarati = models.CharField(max_length=100, help_text="City name in Gujarati")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'City'
        verbose_name_plural = 'Cities'
    
    def __str__(self):
        return f"{self.name} ({self.name_gujarati})"


class Boat(models.Model):
    """Model for storing boat information."""
    name = models.CharField(max_length=100)
    name_gujarati = models.CharField(max_length=100, help_text="Boat name in Gujarati")
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='boats')
    boat_number = models.CharField(max_length=50, blank=True)
    capacity = models.IntegerField(default=0, help_text="Number of passengers")
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['city', 'name']
        verbose_name = 'Boat'
        verbose_name_plural = 'Boats'
        unique_together = ['name', 'city']
    
    def __str__(self):
        return f"{self.name} - {self.city.name}"


class MenuEntry(models.Model):
    """Model for storing boat menu entries."""
    MEAL_CHOICES = [
        ('નાસ્તો', 'Breakfast'),
        ('બપોર', 'Lunch'),
        ('રાત', 'Dinner'),
    ]
    
    boat = models.ForeignKey(Boat, on_delete=models.CASCADE, related_name='menus')
    meal_type = models.CharField(max_length=50, choices=MEAL_CHOICES)
    items = models.TextField(help_text="Menu items separated by commas")
    time_from = models.TimeField()
    time_to = models.TimeField()
    date = models.DateField()
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    special_note = models.TextField(blank=True, help_text="Special notes in Gujarati")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', 'time_from']
        verbose_name = 'Menu Entry'
        verbose_name_plural = 'Menu Entries'
        unique_together = ['boat', 'meal_type', 'date']
    
    def __str__(self):
        return f"{self.boat.name} - {self.meal_type} - {self.date}"


class ExcelUpload(models.Model):
    """Model for storing uploaded Excel files with menu data."""
    file = models.FileField(
        upload_to='menu_uploads/%Y/%m/',
        validators=[FileExtensionValidator(allowed_extensions=['xlsx', 'xls'])]
    )
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='uploads')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    processed_at = models.DateTimeField(null=True, blank=True)
    records_created = models.IntegerField(default=0)
    error_log = models.TextField(blank=True)
    uploaded_by = models.CharField(max_length=100, blank=True)
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Excel Upload'
        verbose_name_plural = 'Excel Uploads'
    
    def __str__(self):
        return f"Upload for {self.city.name} on {self.uploaded_at}"


class Query(models.Model):
    """Model for storing user queries for analytics."""
    query_text = models.TextField()
    response_text = models.TextField()
    boat = models.ForeignKey(Boat, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'User Query'
        verbose_name_plural = 'User Queries'
    
    def __str__(self):
        return f"Query at {self.timestamp}"
