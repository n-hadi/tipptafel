from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
import random, string
from simple_history.models import HistoricalRecords


# Create your models here.

class BTCPay_Client(models.Model):
  pickle_data = models.BinaryField(default=b'', editable=True)

class Payment(models.Model):
  identifier = models.CharField(default='', max_length=11, editable=False)#wegen false not im admin display
  user  = models.ForeignKey('users.User', on_delete=models.PROTECT)
  date = models.DateTimeField(auto_now_add=True) 
  tt_amount = models.DecimalField(default=0,max_digits=8, decimal_places=2) #amount purchased tt
  currencies = [("BTC","Bitcoin"),('EUR','Euro')]
  currency = models.CharField(choices=currencies, max_length=100, default='BTC')
  currency_amount = models.CharField(max_length=999, default='') 
  payment_methods = [('BTC','Bitcoin'),("PP", "PayPal"),("BANK", "Banküberweisung")]
  payment_method = models.CharField(choices=payment_methods, max_length=100, default='BTC')
  payment_types =[('Deposit','Deposit funds')] 
  deposit_unlocked = models.BooleanField(default=False)
  payment_type = models.CharField(choices=payment_types, max_length=100, default="Deposit")
  invoice_creation_data = models.JSONField(blank=True, null=True)
  invoice_creation_error = models.CharField(default="", max_length=99999, blank=True,null=True)

class BTCPay_IPN(models.Model): #Instant Payment Notification
   payment = models.ForeignKey('payments.Payment', on_delete=models.CASCADE)
   webhook_response = models.JSONField(blank=True,null=True)

  
@receiver(post_save, sender=Payment)
def create_payment_identifier(sender, instance, created, **kwargs):
 if instance.identifier == '':
    while True:
      characters = string.ascii_letters + string.digits
      identifier = ''.join(random.choice(characters) for _ in range(11))
      if not Payment.objects.filter(identifier=identifier).exists():
       instance.identifier = identifier
       instance.save()
       break

class Withdrawal(models.Model):
  identifier = models.CharField(default='', max_length=11, editable=False)#wegen false not im admin display
  user  = models.ForeignKey('users.User', on_delete=models.PROTECT)
  date = models.DateTimeField(auto_now_add=True)
  tt_amount = models.DecimalField(default=0,max_digits=8, decimal_places=2) #Tipptaler 1TT = 1€
  fee_amount = models.DecimalField(default=0, decimal_places=2,max_digits=8) #5% der tipptaler maximal 5€
  withdraw_currencies = [("BTC","Bitcoin"),("EUR","Euro"), ("USD","Dollar")]
  withdraw_currency = models.CharField(choices=withdraw_currencies,default="BTC", max_length=999) 
  withdraw_currency_amount = models.CharField(max_length=999, default='') 
  withdraw_methods = [("BTC", "Bitcoin"),("PP", "PayPal"),("BANK", "Banküberweisung")]
  withdraw_method = models.CharField(choices=withdraw_methods,default="BTC", max_length=999)
  payment_infos = models.JSONField()#{"btc_address": xxx }, {"paypal mail": xxx}, {"IBAN": DEXXX, BIC: xxx }
  WITHDRAWAL_STATUS_CHOICES = (
    ('pending', 'Ausstehend'),  
    ('approved', 'Genehmigt'),  
    ('rejected', 'Abgelehnt'),  
    ('completed', 'Erledigt'),  
  )
  status = models.CharField(max_length=99, choices=WITHDRAWAL_STATUS_CHOICES, default='pending')
  history = HistoricalRecords()



@receiver(post_save, sender=Withdrawal)
def create_payment_identifier(sender, instance, created, **kwargs):
 if instance.identifier == '':
    while True:
      characters = string.ascii_letters + string.digits
      identifier = ''.join(random.choice(characters) for _ in range(11))
      if not Withdrawal.objects.filter(identifier=identifier).exists():
       instance.identifier = identifier
       instance.save()
       break