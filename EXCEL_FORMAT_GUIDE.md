# Excel Upload Format Guide

This guide explains how to format your Excel file for uploading boat menu data.

## Required Columns

Your Excel file MUST include these columns (in any order):

1. **Boat Name** - The name of the boat (English or Gujarati)
2. **Meal Type** - Type of meal (નાસ્તો / Breakfast, બપોર / Lunch, રાત / Dinner)
3. **Date** - Date of the menu (format: YYYY-MM-DD or DD/MM/YYYY)
4. **Items** - Menu items (comma separated)
5. **Time From** - Start time (format: HH:MM or HH:MM AM/PM)
6. **Time To** - End time (format: HH:MM or HH:MM AM/PM)

## Optional Columns

7. **Price** - Price in rupees (number)
8. **Special Note** - Any special notes in Gujarati

## Example Excel Format

| Boat Name | Meal Type | Date | Items | Time From | Time To | Price | Special Note |
|-----------|-----------|------|-------|-----------|---------|-------|--------------|
| સી પ્રિન્સેસ | નાસ્તો | 2026-01-06 | પોહા, ઢોકળા, ચા | 08:00 | 09:30 | 50 | તાજું બનાવેલું |
| સી પ્રિન્સેસ | બપોર | 2026-01-06 | રોટલી, દાળ, ભાત, શાક | 12:00 PM | 02:00 PM | 100 | |
| સી પ્રિન્સેસ | રાત | 2026-01-06 | રોટલી, પરાઠા, પનીર સબ્જી | 08:00 PM | 10:00 PM | 120 | |

## Important Notes

1. **Boat Must Exist**: The boat name must already exist in the database for that city
2. **City Selection**: Select the correct city before uploading the Excel file
3. **Date Format**: Use YYYY-MM-DD format for best results
4. **Time Format**: 24-hour (08:00) or 12-hour (08:00 AM) both work
5. **Meal Types**: Use either Gujarati (નાસ્તો, બપોર, રાત) or English (breakfast, lunch, dinner)
6. **Multiple Rows**: You can have multiple boats and dates in one file

## Steps to Upload

1. Go to Django Admin Panel: `/admin/`
2. Login with admin credentials
3. Click on **"Excel Uploads"** section
4. Click **"Add Excel Upload"**
5. Select your Excel file
6. Choose the City
7. Enter your name (optional)
8. Click **Save**
9. The system will automatically process the file and create menu entries

## Error Handling

If there are errors:
- Check the "Error Log" field in the Excel Upload record
- Common errors:
  - Boat name not found in selected city
  - Invalid date format
  - Invalid time format
  - Missing required columns

## Sample Excel File

Download the sample template from admin panel or create one following the format above.

## Tips

- Keep boat names consistent with database
- Use bulk upload for multiple days at once
- One row = one meal for one boat on one date
- Duplicate entries (same boat, meal, date) will be updated, not duplicated
