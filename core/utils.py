import random
from core.models import Match
from functools import wraps
from django.http import HttpResponseBadRequest
from datetime import timedelta
from django.utils import timezone



def htmx_required(function):
  @wraps(function)
  def wrap(request, *args, **kwargs):
        if request.htmx:
             return function(request, *args, **kwargs)
        else:
            return HttpResponseBadRequest()

  return wrap

def mockup_bets():
 mockup_usernames = ["GorillaGoalie1", "S04andi", "Fc_Feiern", "Kev342", "Luftlocher997","spitzerFlitzer", "Energie_Kopfnuss", "Siuuuuuu", "sanchez", "Kiezkicker23", "AMGKreidewagen", "Pfosten_mit_Latte","La_Pulga", "koelsche_jung", "Alpenadler86","jogisack","chico_aus_dortmund", "Bankwärmer12", "Sturmführer", "Kampftrinker99","Kellerkicker2",  "pyromane1860", "Eintracht_Prügel", "Juventus_Rubin",  "TSGLiebe", "trendsetter_", "suedkurve21", "Hangover96",  "Krombacher", "AlBundy85", "yildrim98",  "Semmelbrösel", "Cooligan09",  "LuckyLuke991", "ronaldinho99", "BVBoss", "fullhdVAR", "Ultra_Escobar", "Dr_FFM", "Capitano57",   "alteFlamme", "SuperMario8", "MrNiceGuy", "Ajax_Dauerstramm", "rotrotweiß", "Härter_BSC", "zFlame","nurderfc", "werderhaemmert", "bratwurstler34",  ]
 random.shuffle(mockup_usernames)


 mockup_stakes = [random.randint(5, 100) for _ in range(50)]

 options = [['t1'],['t2'],['x'],['t1','t2'],['t1','x'],['t2','x']]
 mockup_tips = [ options[random.randint(0,5)] for _ in range(50) ]
 start_range = [ timezone.now(), timezone.now()+timedelta(days=60 )]
 mockup_bets = zip(Match.objects.filter(start__range=start_range).order_by('start')[:50], 
                    mockup_usernames, 
                    mockup_stakes,
                    mockup_tips)
 return mockup_bets

def valid_maxmin(is_max,number):
  try:
    if float(number) <0:
       raise ValueError
    else:
     return float(number)
  except:
     if is_max:
        return 99999
     else:
        return 5
  
def valid_sort(sortby):
   options = ['stake','-stake','creation_date','-creation_date']
   if sortby in options:
      return sortby
   else:
      return '-creation_date'

   
