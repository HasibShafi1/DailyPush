from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from .models import Habit, CheckIn
from datetime import timedelta
import json

def get_or_create_guest_user():
    user, created = User.objects.get_or_create(username='guest')
    return user

def dashboard(request):
    user = get_or_create_guest_user()
    habits = Habit.objects.filter(user=user, archived=False).prefetch_related('checkins')
    
    # Generate last 365 days dates
    today = timezone.now().date()
    dates = [today - timedelta(days=i) for i in range(364, -1, -1)] # 365 days ending today
    
    # Prepare data for template
    habits_data = []
    for habit in habits:
        checkin_dates = set(habit.checkins.values_list('date', flat=True))
        days_data = []
        for date in dates:
            is_checked = date in checkin_dates
            days_data.append({
                'date': date,
                'is_checked': is_checked,
                'date_str': date.strftime('%Y-%m-%d')
            })
        
        habits_data.append({
            'habit': habit,
            'days': days_data,
            'streak': habit.get_current_streak()
        })
        
    return render(request, 'core/dashboard.html', {'habits_data': habits_data})

def habit_detail(request, habit_id):
    user = get_or_create_guest_user()
    habit = get_object_or_404(Habit, id=habit_id, user=user)
    
    # Stats
    total_checkins = habit.checkins.count()
    current_streak = habit.get_current_streak()
    
    # Generate full year heatmap for detail view
    today = timezone.now().date()
    dates = [today - timedelta(days=i) for i in range(364, -1, -1)]
    checkin_dates = set(habit.checkins.values_list('date', flat=True))
    
    days_data = []
    # Data for Chart (Last 30 days)
    chart_labels = []
    chart_data = []
    
    # Last 30 days reversed (oldest first) for Chart
    last_30_days = [today - timedelta(days=i) for i in range(29, -1, -1)]
    
    for date in last_30_days:
        is_checked = date in checkin_dates
        chart_labels.append(date.strftime('%b %d'))
        chart_data.append(1 if is_checked else 0)

    # For heatmap (newest first)
    for date in dates:
        is_checked = date in checkin_dates
        days_data.append({
            'date': date,
            'is_checked': is_checked,
            'date_str': date.strftime('%Y-%m-%d')
        })

    return render(request, 'core/habit_detail.html', {
        'habit': habit,
        'days': days_data,
        'total_checkins': total_checkins,
        'current_streak': current_streak,
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data)
    })

def settings(request):
    return render(request, 'core/settings.html')

@require_POST
def update_habit(request, habit_id):
    user = get_or_create_guest_user()
    habit = get_object_or_404(Habit, id=habit_id, user=user)
    
    habit.name = request.POST.get('name', habit.name)
    habit.description = request.POST.get('description', habit.description)
    habit.color = request.POST.get('color', habit.color)
    habit.save()
    
    return redirect('habit_detail', habit_id=habit.id)

@require_POST
def delete_habit(request, habit_id):
    user = get_or_create_guest_user()
    habit = get_object_or_404(Habit, id=habit_id, user=user)
    habit.archived = True
    habit.save()
    return redirect('dashboard')

@require_POST
def toggle_checkin(request):
    habit_id = request.POST.get('habit_id')
    date_str = request.POST.get('date')
    
    user = get_or_create_guest_user()
    habit = get_object_or_404(Habit, id=habit_id, user=user)
    date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
    
    checkin, created = CheckIn.objects.get_or_create(habit=habit, date=date)
    
    if not created:
        checkin.delete()
        is_checked = False
    else:
        is_checked = True
        
    return render(request, 'core/partials/day_square.html', {
        'habit': habit,
        'day': {'date': date, 'is_checked': is_checked, 'date_str': date_str},
        'color': habit.color
    })

@require_POST
def create_habit(request):
    name = request.POST.get('name')
    description = request.POST.get('description')
    color = request.POST.get('color')
    
    if name:
        if not color:
             import random
             colors = ['#EF4444', '#F59E0B', '#10B981', '#3B82F6', '#6366F1', '#8B5CF6', '#EC4899']
             color = random.choice(colors)
             
        user = get_or_create_guest_user()
        Habit.objects.create(user=user, name=name, description=description, color=color)
        
    return redirect('dashboard')
