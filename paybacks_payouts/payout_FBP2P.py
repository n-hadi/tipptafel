from bets.models import FixedBetP2P
from paybacks_payouts.models import PayoutFBP2P, PaybackFBP2P
from decimal import Decimal
from django.contrib import messages



   
def payout_bets(request, match):
  if match.outcome == "an":
   messages.add_message(request, messages.ERROR, 'Match outcome: anstehend')
  elif match.outcome == "u":
   messages.add_message(request, messages.ERROR, 'Match outcome: ungültig')
  else:
    bets = FixedBetP2P.objects.filter(match=match, active=True, paid_out=False, paid_back=False)
    for bet in bets:
      if bet.get_winner():
        payout_bet(bet)
      elif bet.contender == None:
        payback_challenger(bet)
    messages.success(request, "Wetten erfolgreich aus- und zurückgezahlt (sofern kein User gefunden)")

def payout_bet(bet):
    winner = bet.get_winner()
    payout = Decimal(bet.stake * 2).quantize(Decimal("0.00"))
    winner.balance.amount += payout
    winner.balance.save()
    bet.paid_out = True
    bet.active = False
    bet.save()
    PayoutFBP2P(bet=bet, winner=winner, amount=payout).save()

def payback_challenger(bet):
    bet.challenger.balance.amount += bet.stake
    bet.challenger.balance.save()
    bet.paid_back = True
    bet.active = False
    bet.save()
    pb_dict = {"challenger" : str(bet.stake), "contender": None}
    PaybackFBP2P(bet=bet, payback_type="A", amounts=pb_dict).save()

    
def payback_match_cancelled(request, match):
  if match.outcome != "u":
    err = 'Match outcome: '+ str(match.outcome) + '. Outcome has to be ungültig'
    messages.add_message(request, messages.ERROR, err)
  else:
   spielabbruch_or_absage = FixedBetP2P.objects.filter(match=match, active=True, paid_out=False, paid_back=False)
   for bet in spielabbruch_or_absage:
       try:
         bet.contender.balance.amount += bet.stake
         bet.contender.balance.save()
         contender_stake = str(bet.stake)
       except:
         contender_stake = None
       bet.challenger.balance.amount += bet.stake
       bet.challenger.balance.save()
       bet.paid_back = True
       bet.active = False
       bet.save()
       pb_dict = {"challenger": str(bet.stake), "contender": contender_stake}
       PaybackFBP2P(bet=bet,payback_type="B", amounts=pb_dict).save()
   messages.success(request, "Successfully paid back/undone bets.")

def payback_match_invalid(request, match):
  if match.outcome != "u":
    err = 'Match outcome: '+ str(match.outcome) + '. Outcome has to be ungültig'
    messages.add_message(request, messages.ERROR, err)
  else:
    spiel_ruckgangig = FixedBetP2P.objects.filter(match=match, active=False, paid_out=True, paid_back=False)
    for bet in spiel_ruckgangig:
       payout = PayoutFBP2P.objects.filter(bet=bet).last()
       winner = payout.winner
       if winner.balance.amount > bet.stake:
         winner.balance.amount -= bet.stake
       else:
         winner.balance.amount = 0
       winner.balance.save()
       loser = bet.get_opponent(winner)
       loser.balance.amount += bet.stake
       loser.balance.save()
       payout.undone = True
       payout.save()
       bet.paid_back = True
       bet.save()
       challenger_pb = -bet.stake if winner == bet.challenger else bet.stake
       pb_dict = {"challenger": str(challenger_pb), "contender": str(-challenger_pb)}
       PaybackFBP2P(bet=bet,payback_type="C", amounts=pb_dict).save()
    messages.success(request, "Successfully paid back/undone bets.")
         

#### COMMENTS ####
'''
if user found
if paid out/rückgängig: remove stake from winner, give to loser 
if not paid out/absage: give stake to both 
set paid_back true
if user not found:
if paid back false 
  payback challenger


  winner stake abziehen
  wenn winner balance < stake
    zieh so viel ab wie geht
  loser stake geben
'''
# mit contender jeder kriegt stake
# ohne contender nur einer kriegt stake
#Nachhinein spiel ungültig active=False, paid_out=True, paid_back=False
'''
if bets.payout == false 

if match.outcome [t1,t2,x]
if un give them their money back
if an raise error

if bet user gefunden => pay out
create betpayout
deactivate all bets
'''
