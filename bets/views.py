from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from core.utils import htmx_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from core.models import Match, Tournament
from bets.models import FixedBetP2P
from users.models import Balance
from django.db.models import F,Q
from .utils import set_message, FBP2P_text, update_contenderbalance_FBP2P, maxdays
from bets.create_FBP2P_form import validate_form
from core.accept_FBP2P_form import bet_ok

@login_required
def mybetsview(request):
  user = request.user
  my_bets = FixedBetP2P.objects.filter(Q(challenger=user) | Q(contender=user)).order_by('match__start')
  return render(request, 'bets/mybets.html', context={'bets': my_bets})

@login_required 
def create_bet(request):
 if request.POST:
  try:
    bets = validate_form(request.POST, request.session['matches']) 
    bet_sum = round(Decimal(sum(bet['stake'] for bet in bets)),2)
    if bet_sum < request.user.balance.amount and len(bets) > 0:
     for bet in bets:
      FixedBetP2P(challenger=request.user, 
          match=bet['match'], 
          challenger_bet=bet['challenger_bet'],
          stake=bet['stake']).save()
     Balance.objects.filter(user=request.user).update(amount=F('amount') - bet_sum)
     messages.success(request, set_message(len(bets)))
    else:
      messages.error(request, "Fehler. Die Wette konnte nicht platziert werden.")
    return redirect('mybets')
  except Exception as e:
    print(e)
    messages.error(request, "Ein Fehler ist aufgetreten. Die Wette konnte nicht platziert werden.")
    return redirect('create_bet')
 else:
  return render(request, 'bets/create_bet.html')

@htmx_required
@login_required
def upcoming_games(request, liga): #Läd spiele für create bet
 tournament = Tournament.objects.get(name=liga)
 #alle spiele in den nächsten 30 Tagen ab in 30 minuten
 current_date = timezone.now() + timedelta(minutes=30) 
 end_date = current_date + timedelta(days=maxdays(tournament.name))
 matches = Match.objects.filter(tournament=tournament,start__range=[current_date, end_date]).order_by("start")[:30]
 request.session['matches'] = [match.identifier for match in matches]
 return render(request, 'bets/upcoming_games.html', context={"matches": matches})

@htmx_required
@login_required
def tipptafel_take_bet(request):#Die FBP2P Wetten auf der tipptafel 
    try: 
      bet = FixedBetP2P.objects.get(identifier=request.htmx.trigger_name)
      user = request.user
      if user.balance.amount < bet.stake:
        res_data= {"message":"Dein Guthaben reicht für diese Wette nicht aus."}
        return JsonResponse(res_data,status=403)
      if bet_ok(bet, user):
        update_contenderbalance_FBP2P(bet,user)
        updated_balance = Decimal.normalize(user.balance.amount)
        res_data = {"message":"🏆 Wette erfolgreich platziert!", "balance": updated_balance}
        return JsonResponse(res_data,status=200)
      else:
        return JsonResponse({"message":'Fehler. Wette konnte nicht platziert werden.'},status=400)
    except Exception as e:
      print(e)
      return JsonResponse({"message": 'Serverfehler'}, status=500)

def detail_FBP2P(request, identifier):
 bet = FixedBetP2P.objects.get(identifier=identifier)
 if (bet.contender == None and bet.active == True) or bet.user_is_contestant(request.user):
     bet_status = bet.status(request.user)
     bet_txt = FBP2P_text(bet)
     return render(request,'bets/detail_FBP2P.html',context={"bet": bet,
                                                           "bet_text": bet_txt,
                                                           "bet_status": bet_status
                                                           })
 else:
     return redirect('index')


def detail_take_FBP2P(request, identifier):
  if request.user.is_authenticated and request.htmx:
    bet = FixedBetP2P.objects.get(identifier=identifier)
    user = request.user
    if user.balance.amount < bet.stake:
      messages.error(request, "Dein Guthaben reicht für diese Wette nicht aus.")
    elif bet_ok(bet, user):
      update_contenderbalance_FBP2P(bet,user)
      messages.success(request, "🏆 Wette erfolgreich platziert!")
    else:
      messages.error(request, "Fehler. Wette konnte nicht platziert werden.")
    return redirect('mybets')
  else:
    response = HttpResponse()
    response["HX-Redirect"] = reverse("login")
    return response

   
   


