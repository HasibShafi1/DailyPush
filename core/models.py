from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=7, default='#10B981') # Hex code
    icon = models.CharField(max_length=50, default='star') # Icon name
    
    # Frequency & Rules
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('custom', 'Custom'),
    ]
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default='daily')
    target_days = models.CharField(max_length=255, blank=True, null=True) # e.g. "Mon,Wed,Fri" or JSON
    reminder_time = models.TimeField(blank=True, null=True)
    
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(blank=True, null=True)
    archived = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_current_streak(self):
        # Allow checking streak efficiently
        # Get all check-ins dates ordered by date desc
        checkins = self.checkins.order_by('-date').values_list('date', flat=True)
        if not checkins:
            return 0
        
        today = timezone.now().date()
        current_date = today
        streak = 0
        
        # Check if checked in today
        if today in checkins:
            pass # Continues below
        elif (today - timezone.timedelta(days=1)) in checkins:
             current_date = today - timezone.timedelta(days=1)
        else:
            return 0
            
        for date in checkins:
            if date == current_date:
                streak += 1
                current_date -= timezone.timedelta(days=1)
            elif date < current_date:
                break
                
        return streak

class CheckIn(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='checkins')
    date = models.DateField()

    class Meta:
        unique_together = ('habit', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.habit.name} on {self.date}"
