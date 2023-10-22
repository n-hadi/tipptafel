from django.contrib import admin
from payments.models import BTCPay_Client, Payment, BTCPay_IPN, Withdrawal
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
import pickle
from btcpay import BTCPayClient #richtiger client
from django.contrib import messages

import nested_admin 

class BalanceInline(nested_admin.NestedTabularInline):
  model = BTCPay_IPN

class PaymentAdmin(nested_admin.NestedModelAdmin):
 inlines = [BalanceInline,]
 readonly_fields = ["date","identifier"]

class BTCPay_ClientAdmin(admin.ModelAdmin):
  add_form_template = 'payments/admin/add_btcpay_client.html'
  readonly_fields = ["id"]
  def add_view(self, request, form_url="", extra_context=None):
    if request.method == 'POST':
        try:
          token = request.POST.get('access_token') 
          client = BTCPayClient.create_client(host='https://btcpay.tipptafel.de', code=token) #real client
          pickled_client = pickle.dumps(client)
          try: #falls es noch keinen gibt
            BTCPay_Client.objects.all().delete() #database old saved client
          except:
            pass
          BTCPay_Client(pickle_data=pickled_client).save() #new client saved
          messages.success(request, 'Neuen Client erfolgreich erstellt')
        except Exception as e:
          print(e)
          messages.error(request, 'Fehler: ' + str(e))
        return HttpResponseRedirect('admin/')
    return super().add_view(request, form_url, extra_context)
  
class WithdrawalAdmin(admin.ModelAdmin):
  readonly_fields = ["date"]
  

# Register your models here.
admin.site.register(BTCPay_Client, BTCPay_ClientAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Withdrawal, WithdrawalAdmin)
