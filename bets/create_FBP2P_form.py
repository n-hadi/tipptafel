from core.models import Match
from core.accept_FBP2P_form import minutes_till_kickoff

def validate_form(form, match_ids):
    bets = []
    for match_id in match_ids:
     raw_input = form.getlist(match_id) #['t1','5'] ['t1','t2','6']['']
     ordered_bet = normalize_input_data(raw_input, match_id)
     try:
       bet = validate_bet(ordered_bet) if ordered_bet is not None else None
     except Exception as e:
       print(e)
       bet = None
     if bet != None:
      print('Valid bet:')
      print(ordered_bet)
      bets.append(bet)
    return bets
   
#['t1', 't2','5'] => {"tips": ['t1','t2'], "stake": '5', "match_id": "xyz"}
def normalize_input_data(raw_input, match_id): 
  if len(raw_input) == 2 : 
       return {"tips": [raw_input[0]] , "stake": raw_input[1] , "match_id": match_id }
  elif len(raw_input) == 3:
     return {"tips": [raw_input[0], raw_input[1]], "stake": raw_input[2] , "match_id": match_id }
  else: #['']
     return None
  
tip_options = ['t1','t2','x']

def validate_bet(orderedbet):
  tips = orderedbet["tips"] #list
  stake = orderedbet["stake"]
  match_id = orderedbet["match_id"]
  match = Match.objects.get(identifier=match_id)
  conditions = [
    (all(i in tip_options for i in tips),"Invalid Tipp"),
    (stake_is_valid(stake),"Invalid stake"),
    (tips_not_duplicate(tips),"Duplicate Tipp"),
    (validate_draw_impossible(tips, match),"Draw impossible error"),
    (minutes_till_kickoff(30,match),"Betting creation too close to kick-off")
  ]
  conditions_failed = False
  for condition in conditions:
    if not condition[0]:
      conditions_failed = True
      print(f"Condition failed:\n" + condition[1])
  if not conditions_failed:
    stake = round(float(stake),2)
    tips = tips[0] if len(tips) == 1 else tips[0] +','+ tips[1]
    bet = {'match': match, 'challenger_bet': tips, 'stake': stake}
    return bet
  return None
    

def stake_is_valid(stake): 
  try:
     stake = round(float(stake),2)
     if type(stake) == float and stake >= 1 and stake <= 99999:
      return True
     else:
      return False
  except:
    return False
   
def tips_not_duplicate(tips):
  if len(tips) == 2:
    if len(tips) != len(set(tips)):
      return False
    else:
      return True
  else:
    return True

def validate_draw_impossible(tips, match):
  if match.draw_impossible:
    if len(tips) == 1 and tips[0] != "x":
      return True
    else:
      return False
  else:
    return True





   

