from decimal import Decimal 


def set_message(length):
    if length >1:
       return "✅ Wetten erfolgreich platziert! User werden gesucht..."
    else:
       return "✅ Wette erfolgreich platziert! User wird gesucht..."

def FBP2P_text(Bet):
   texts = [],[]
   for index, bet in enumerate([Bet.challenger_bet, Bet.contender_bet]):
      for tip in bet:
         if tip == "t1" or tip == 't2':
          texts[index].append(getattr(Bet.match, tip).short_name)
         else:
          texts[index].append('Unentschieden')
   return texts

def update_contenderbalance_FBP2P(bet,user):
   bet.contender = user
   balance = user.balance.amount
   user.balance.amount = Decimal(balance) - Decimal(bet.stake)
   user.balance.save()
   bet.save()


def maxdays(tournament):
   return 14 if tournament == "Bundesliga" else 30

