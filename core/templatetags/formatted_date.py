from django import template
from datetime import datetime as dt, timedelta
from django.utils.safestring import mark_safe
from django.utils import translation
import pytz, locale

register = template.Library()

@register.filter(expects_localtime=True)
def formatted_date(game_time): 
 game_time = game_time.astimezone(pytz.timezone("Europe/Berlin")) #UTC to CET
 today = dt.today().date()
 if game_time.date() == today:
  return mark_safe('Heute, <br>' + game_time.strftime("%H:%M") + ' Uhr')
 elif today + timedelta(days=1) == game_time.date():
  return mark_safe('Morgen,  <br>' + game_time.strftime("%H:%M") + ' Uhr')
 elif today + timedelta(days=6) >= game_time.date() and today < game_time.date():
  try:
        locale.setlocale(locale.LC_TIME, 'de_DE.utf8') 
  except:
        locale.setlocale(locale.LC_TIME, 'de_DE')
  german_weekday = game_time.strftime("%A")
  german_date = mark_safe(german_weekday+',  <br>' + game_time.strftime("%H:%M") + ' Uhr')
  locale.setlocale(locale.LC_TIME, '')
  return german_date
 else:
  #print(game_time.date(), dt.today().date(), game_time.strftime("%D, %H:%M"))
  #2023-05-13  2023-05-14    05/13/23, 15:30
  return mark_safe(game_time.strftime("%d.%m.%y") + '<br>' + game_time.strftime("%H:%M") + ' Uhr')
