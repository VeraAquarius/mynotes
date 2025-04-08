from celery import shared_task
from datetime import datetime
from .models import Reminder
from django.utils import timezone

@shared_task
def check_reminders():
    now = timezone.now()
    reminders = Reminder.objects.filter(reminder_time__lte=now, sent=False)
    for reminder in reminders:
        # 发送提醒逻辑
        print(f"提醒: {reminder.note.title} - {reminder.reminder_time}")
        reminder.sent = True
        reminder.save()