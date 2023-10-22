from datetime import timedelta
from django.utils.timezone import localtime


def minutes_till_kickoff(minutes,match):
   current_time = localtime()
   kickoff = match.start
   time_difference = kickoff - current_time
   if time_difference > timedelta(minutes=minutes):
      return True
   else:
      return False

def bet_ok(bet, user):
 conditions = [
    bet.contender == None,
    bet.active == True,
    bet.challenger != user,
    bet.match.outcome == 'an',
    minutes_till_kickoff(15,bet.match),
 ]

 if all(conditions):
    return True
 else:
    return False