from django.db import models
from multiselectfield import MultiSelectField
from django.dispatch import receiver
from django.db.models.signals import post_save
from simple_history.models import HistoricalRecords


class FixedBetP2P(models.Model):
 identifier = models.CharField(default='', max_length=11, editable=False)
 creation_date = models.DateTimeField(auto_now_add=True)
 challenger = models.ForeignKey('users.User',related_name="challenger",on_delete=models.PROTECT)
 stake = models.DecimalField(max_digits=8, decimal_places=2)
 contender = models.ForeignKey('users.User',related_name="contender",on_delete=models.PROTECT, blank=True, null=True)
 match = models.ForeignKey('core.Match',on_delete=models.PROTECT, related_name='match')
 bet_choices = [('t1', 'Team 1'),('t2','Team 2'),('x', 'Unentschieden')]
 challenger_bet = MultiSelectField(choices=bet_choices,max_choices=2,max_length=100)
 contender_bet = MultiSelectField(choices=bet_choices,max_choices=2,max_length=100)
 active = models.BooleanField(default=True)
 private = models.BooleanField(default=False)
 paid_out = models.BooleanField(default=False)
 paid_back = models.BooleanField(default=False) #falls ungültig oder keinen user gefunden
 history = HistoricalRecords()

 def __str__(self):
  return str(self.match) + ': ' + self.challenger.username + ' ' + str(self.challenger_bet)
 
 def match_status(self):
  return self.match.status()

 def get_winner(self):
   if self.contender == None:
     return None
   if self.match.outcome in self.corresponding_userbet(self.challenger):
     return self.challenger
   elif self.match.outcome in self.corresponding_userbet(self.contender):
     return self.contender
 
 def get_loser(self):
   if self.get_winner():
    users = [self.contender, self.challenger]
    return next(user for user in users if user != self.get_winner())

 def get_opponent(self, user):
   return next(opp for opp in (self.challenger, self.contender) if opp != user)
 
 def corresponding_userbet(self, user):
   if user == self.challenger:
    return self.challenger_bet
   elif user == self.contender:
    return self.contender_bet
   
 def user_is_contestant(self, user):
   if user == self.challenger or user == self.contender:
     return True
   else: 
     return False
 
 def status(self, user): #status of a bet is relative to the user requesting it
   if self.user_is_contestant(user): 
         match = self.match
         if self.contender == None:
          if match.outcome == "an":
           status = "User wird gesucht..."
          elif match.outcome in ["t1","t2","x"]:
           status = "Keinen User gefunden"
         else:
          if match.outcome == "an":
           status = "Anstehend"
          else:
           status = "Gewonnen 🏆" if match.outcome in self.corresponding_userbet(user) else "Verloren ❌"
         status = "Ungültig" if match.outcome == "u" else status
         return status
   else:
    return "Nicht verfügbar"
  

@receiver(post_save, sender=FixedBetP2P)
def create_contender_bet(sender, instance, created, **kwargs):
 if not instance.contender_bet:
    choices = ['t1','t2'] if instance.match.draw_impossible else ['t1','t2','x']
    contender_bet_list = [x for x in choices if x not in instance.challenger_bet.split(",")]
    instance.contender_bet = ','.join(contender_bet_list)
    instance.save()