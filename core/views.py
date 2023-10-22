from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta
from core.models import HomePageBackground
from core.models import Match, Tournament
from bets.models import FixedBetP2P
from core.utils import mockup_bets, htmx_required, valid_maxmin, valid_sort
from paybacks_payouts.payout_FBP2P import payback_match_cancelled, payback_match_invalid
from django.http import HttpResponseBadRequest
from django.contrib.admin.views.decorators import staff_member_required


# buy credit before submit checken
# create bet add event listener auch bei dynamic loading für inputs
# betview falls geshared wird
# mybets share button



# Create your views here.
def index(request):
 user = request.user if request.user.is_authenticated else None
 if request.htmx and request.GET and user != None: #Filter
      if not request.GET.get('tournament'):
        #filter modal
        matches = Match.objects.filter(identifier__in=request.GET.getlist('games'))
        min = request.GET['Min']
        max = request.GET['Max']
        sort = request.GET['sortby']
      else:
        # side navigation league selection
        matches = Match.objects.filter(tournament__name__in=request.GET.getlist('tournament'))
        min = 5
        max = 99999
        sort = "-creation_date"
      filtered_bets = FixedBetP2P.objects.filter(active=True,
                                        private=False,
                                        contender__isnull=True,
                                        stake__gte=valid_maxmin(False,min), #greater than equal
                                        stake__lte=valid_maxmin(True, max), #lesser than equal
                                        match__in=matches,
                                        ).exclude(challenger=user).order_by(valid_sort(sort))[:50]
      return render(request,'core/index.html', context={'open_bets': filtered_bets})
 else:
  open_bets = FixedBetP2P.objects.filter(active=True,private=False,contender__isnull=True, match__start__gt=timezone.now()).exclude(challenger=user).order_by('match__start')[:50]
  mockup_betss = mockup_bets() if user == None else None
  return render(request,'core/index.html', context={'open_bets': open_bets, 
                                                    'mockup_bets': mockup_betss})
 #<QueryDict: {'games': ['1', '5', '8'], 'Min': ['12'], 'Max': ['33'], 'sortby': ['new']}>
 #context={'background': HomePageBackground.objects.get(id=1),'block_path' : block_paths['index']})


def contact(request):
  return render(request,'core/contact.html')

def agb(request):
  return render(request,'core/agb.html')

@htmx_required #für index filter
def get_games(request):
  try:
   tournament = Tournament.objects.get(name=request.GET['liga-select']).id
   current_date = timezone.now() + timedelta(minutes=15) 
   end_date = current_date + timedelta(days=30)
   matches = Match.objects.filter(tournament=tournament, start__range=[current_date,end_date])
   return render(request, 'core/blocks/upcoming_games.html', context={'matches': matches})
  except Exception as e:
   print(e)
   return HttpResponseBadRequest()
  


### FÜR ADMIN PANEL ### 
@staff_member_required
def admin_payback_FBP2P(request, match_id):
 request.session['next'] = request.GET.get('next')
 if request.POST:
   payback_reason = request.POST.get("payback")
   if payback_reason == "cancelled":
    payback_match_cancelled(request, Match.objects.get(id=match_id))
   elif payback_reason == "invalid":
    payback_match_invalid(request, Match.objects.get(id=match_id))
   return redirect(request.session['next'])
 return render(request, 'core/admin/payback_FBP2P.html')

