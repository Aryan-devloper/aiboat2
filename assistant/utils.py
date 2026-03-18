import pandas as pd
from datetime import datetime, time
from .models import Boat, MenuEntry


def process_excel_file(excel_upload):
    """
    Process uploaded Excel file and create menu entries.
    
    Expected Excel format:
    | Boat Name | Meal Type | Date | Items | Time From | Time To | Price | Special Note |
    
    Returns:
        tuple: (records_created, error_message)
    """
    try:
        # Read Excel file
        df = pd.read_excel(excel_upload.file.path)
        
        records_created = 0
        errors = []
        
        # Validate required columns
        required_columns = ['Boat Name', 'Meal Type', 'Date', 'Items', 'Time From', 'Time To']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            return 0, f"Missing required columns: {', '.join(missing_columns)}"
        
        # Process each row
        for idx, row in df.iterrows():
            try:
                # Get or skip boat
                boat_name = str(row['Boat Name']).strip()
                boat = Boat.objects.filter(
                    city=excel_upload.city,
                    name__icontains=boat_name
                ).first()
                
                if not boat:
                    # Try Gujarati name
                    boat = Boat.objects.filter(
                        city=excel_upload.city,
                        name_gujarati__icontains=boat_name
                    ).first()
                
                if not boat:
                    errors.append(f"Row {idx+2}: Boat '{boat_name}' not found in {excel_upload.city.name}")
                    continue
                
                # Parse meal type
                meal_type = str(row['Meal Type']).strip()
                if meal_type not in ['નાસ્તો', 'બપોર', 'રાત']:
                    # Try English to Gujarati mapping
                    meal_mapping = {
                        'breakfast': 'નાસ્તો',
                        'lunch': 'બપોર',
                        'dinner': 'રાત',
                        'nasto': 'નાસ્તો',
                        'bapor': 'બપોર',
                        'rat': 'રાત'
                    }
                    meal_type = meal_mapping.get(meal_type.lower(), meal_type)
                
                # Parse date
                if isinstance(row['Date'], str):
                    date = pd.to_datetime(row['Date']).date()
                else:
                    date = row['Date'].date() if hasattr(row['Date'], 'date') else row['Date']
                
                # Parse times
                time_from = parse_time(row['Time From'])
                time_to = parse_time(row['Time To'])
                
                # Get items
                items = str(row['Items']).strip()
                
                # Get price (optional)
                price = 0
                if 'Price' in df.columns and pd.notna(row['Price']):
                    try:
                        price = float(row['Price'])
                    except:
                        price = 0
                
                # Get special note (optional)
                special_note = ''
                if 'Special Note' in df.columns and pd.notna(row['Special Note']):
                    special_note = str(row['Special Note']).strip()
                
                # Create or update menu entry
                menu_entry, created = MenuEntry.objects.update_or_create(
                    boat=boat,
                    meal_type=meal_type,
                    date=date,
                    defaults={
                        'items': items,
                        'time_from': time_from,
                        'time_to': time_to,
                        'price': price,
                        'special_note': special_note
                    }
                )
                
                if created:
                    records_created += 1
                
            except Exception as e:
                errors.append(f"Row {idx+2}: {str(e)}")
                continue
        
        error_message = '\n'.join(errors) if errors else ''
        return records_created, error_message
        
    except Exception as e:
        return 0, f"Error reading Excel file: {str(e)}"


def parse_time(time_value):
    """Parse time from various formats."""
    if isinstance(time_value, time):
        return time_value
    
    if isinstance(time_value, str):
        # Try various time formats
        for fmt in ['%H:%M', '%I:%M %p', '%H:%M:%S']:
            try:
                return datetime.strptime(time_value.strip(), fmt).time()
            except:
                continue
    
    # If it's a datetime
    if hasattr(time_value, 'time'):
        return time_value.time()
    
    # Default fallback
    return time(0, 0)
