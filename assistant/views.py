from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import datetime, timedelta
import json
from .models import City, Boat, MenuEntry, Query


def index(request):
    """Render the main AI assistant page."""
    cities = City.objects.filter(is_active=True)
    boats = Boat.objects.filter(is_active=True).select_related('city')
    
    context = {
        'cities': cities,
        'boats': boats
    }
    return render(request, 'assistant/index.html', context)


@csrf_exempt
def query(request):
    """Handle AI assistant queries via API."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_input = data.get('query', '')
            boat_id = data.get('boat_id')
            
            # Get boat if specified
            boat = None
            if boat_id:
                try:
                    boat = Boat.objects.get(id=boat_id, is_active=True)
                except Boat.DoesNotExist:
                    pass
            
            # Generate response based on input
            response_text = generate_response(user_input.lower(), boat)
            
            # Save query for analytics
            Query.objects.create(
                query_text=user_input,
                response_text=response_text,
                boat=boat
            )
            
            return JsonResponse({
                'success': True,
                'response': response_text
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    }, status=405)


def generate_response(user_input, boat=None):
    """Generate AI response based on user input and boat."""
    
    today = timezone.now().date()
    
    # If no boat specified, provide general info
    if not boat:
        if 'નાસ્તો' in user_input or 'breakfast' in user_input:
            return 'કૃપા કરીને પહેલા તમારી બોટ પસંદ કરો, પછી હું તમને મેનૂ જણાવી શકીશ।'
        elif 'બપોર' in user_input or 'lunch' in user_input:
            return 'કૃપા કરીને પહેલા તમારી બોટ પસંદ કરો, પછી હું તમને મેનૂ જણાવી શકીશ।'
        elif 'રાત' in user_input or 'dinner' in user_input:
            return 'કૃપા કરીને પહેલા તમારી બોટ પસંદ કરો, પછી હું તમને મેનૂ જણાવી શકીશ।'
        else:
            return 'નમસ્તે! કૃપા કરીને તમારી બોટ પસંદ કરો અને મને "નાસ્તો", "બપોર" અથવા "રાત" વિશે પૂછો।'
    
    # Get menu for selected boat
    boat_name = boat.name_gujarati if boat.name_gujarati else boat.name
    
    # Check for meal type
    if 'નાસ્તો' in user_input or 'breakfast' in user_input:
        menu = MenuEntry.objects.filter(
            boat=boat,
            meal_type='નાસ્તો',
            date=today
        ).first()
        
        if menu:
            response = f"🚢 {boat_name}\n\n"
            response += f"📅 આજે નાસ્તામાં: {menu.items}\n"
            response += f"⏰ સમય: {menu.time_from.strftime('%I:%M %p')} થી {menu.time_to.strftime('%I:%M %p')}\n"
            if menu.price:
                response += f"💰 કિંમત: ₹{menu.price}\n"
            if menu.special_note:
                response += f"📝 નોંધ: {menu.special_note}"
            return response
        else:
            return f"{boat_name} માટે આજે નાસ્તાનું મેનૂ ઉપલબ્ધ નથી।"
    
    elif 'બપોર' in user_input or 'lunch' in user_input:
        menu = MenuEntry.objects.filter(
            boat=boat,
            meal_type='બપોર',
            date=today
        ).first()
        
        if menu:
            response = f"🚢 {boat_name}\n\n"
            response += f"📅 આજે બપોરે: {menu.items}\n"
            response += f"⏰ સમય: {menu.time_from.strftime('%I:%M %p')} થી {menu.time_to.strftime('%I:%M %p')}\n"
            if menu.price:
                response += f"💰 કિંમત: ₹{menu.price}\n"
            if menu.special_note:
                response += f"📝 નોંધ: {menu.special_note}"
            return response
        else:
            return f"{boat_name} માટે આજે બપોરના ભોજનનું મેનૂ ઉપલબ્ધ નથી।"
    
    elif 'રાત' in user_input or 'dinner' in user_input:
        menu = MenuEntry.objects.filter(
            boat=boat,
            meal_type='રાત',
            date=today
        ).first()
        
        if menu:
            response = f"🚢 {boat_name}\n\n"
            response += f"📅 આજે રાત્રે: {menu.items}\n"
            response += f"⏰ સમય: {menu.time_from.strftime('%I:%M %p')} થી {menu.time_to.strftime('%I:%M %p')}\n"
            if menu.price:
                response += f"💰 કિંમત: ₹{menu.price}\n"
            if menu.special_note:
                response += f"📝 નોંધ: {menu.special_note}"
            return response
        else:
            return f"{boat_name} માટે આજે રાત્રિભોજનનું મેનૂ ઉપલબ્ધ નથી।"
    
    elif 'મેનૂ' in user_input or 'menu' in user_input:
        menus = MenuEntry.objects.filter(
            boat=boat,
            date=today
        ).order_by('time_from')
        
        if menus.exists():
            response = f"🚢 {boat_name}\n📅 આજનું સંપૂર્ણ મેનૂ:\n\n"
            for menu in menus:
                response += f"🍽️ {menu.meal_type}: {menu.items}\n"
                response += f"⏰ {menu.time_from.strftime('%I:%M %p')} - {menu.time_to.strftime('%I:%M %p')}\n"
                if menu.price:
                    response += f"💰 ₹{menu.price}\n"
                response += "\n"
            return response
        else:
            return f"{boat_name} માટે આજનું મેનૂ ઉપલબ્ધ નથી।"
    
    elif 'સમય' in user_input or 'time' in user_input or 'timing' in user_input:
        menus = MenuEntry.objects.filter(
            boat=boat,
            date=today
        ).order_by('time_from')
        
        if menus.exists():
            response = f"🚢 {boat_name}\n⏰ આજના ભોજન સમય:\n\n"
            for menu in menus:
                response += f"{menu.meal_type}: {menu.time_from.strftime('%I:%M %p')} થી {menu.time_to.strftime('%I:%M %p')}\n"
            return response
        else:
            return f"{boat_name} માટે સમય ઉપલબ્ધ નથી।"
    
    # Default response
    return f'{boat_name} માટે "નાસ્તો", "બપોર", "રાત" અથવા "મેનૂ" પૂછો।'
