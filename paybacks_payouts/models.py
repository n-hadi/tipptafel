from django.db import models
import random, string 
from django.dispatch import receiver
from django.db.models.signals import post_save
from bets.models import FixedBetP2P

# Create your models here.


class PayoutFBP2P(models.Model):
  date = models.DateTimeField(auto_now_add=True)
  bet = models.ForeignKey('bets.FixedBetP2P', on_delete=models.CASCADE)
  winner = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="winner")
  amount = models.DecimalField(max_digits=8, decimal_places=2) #double stake
  undone = models.BooleanField(default=False)

  def __str__(self):
    return str(self.winner) + " wins " + str(self.amount) 

class PaybackFBP2P(models.Model):
  date = models.DateTimeField(auto_now_add=True)
  bet = models.ForeignKey('bets.FixedBetP2P', on_delete=models.CASCADE)
  payback_type_choices = [('A', 'No User Found'),('B','Match Cancelled'),('C','Match Invalid')]
  #B = Spielabsage oder Spielabbruch
  #C = Spiel im Nachhinein ungültig nach Auszahlungen
  payback_type = models.CharField(choices=payback_type_choices, default='A', max_length=1000)
  amounts = models.JSONField() #individual payback per user {"challenger":1, "contender": 3}

  def __str__(self):
    return str(self.bet) + ":  " + str(self.get_payback_type_display()) 


@receiver(post_save, sender=FixedBetP2P)
def create_FBP2P_identifier(sender, instance, created, **kwargs):
 if instance.identifier == '':
    while True:
      characters = string.ascii_letters + string.digits
      identifier = ''.join(random.choice(characters) for _ in range(11))
      if not FixedBetP2P.objects.filter(identifier=identifier).exists():
       instance.identifier = identifier
       instance.save()
       break
