from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse, HttpResponseServerError, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F
from django.utils import timezone
from core.utils import htmx_required
from .adyen_payments import test_sessions_success
from .models import BTCPay_Client, Payment, BTCPay_IPN, Withdrawal
from .forms import is_valid_deposit, WithdrawalForm
from .utils import get_BTC_rate
from users.models import Balance
from decimal import Decimal
from itertools import chain
import pickle, json, math, datetime



# Create your views here.

@login_required
def paymentsview(request):
  withdrawals = Withdrawal.objects.filter(user=request.user)
  payments = Payment.objects.filter(user=request.user, deposit_unlocked=True)
  transactions = sorted(list(chain(withdrawals,payments)), key=lambda x: x.date)[::-1] 
  #payments.union(withdrawals) geht nicht weil dann alle objekte klasse Payment haben 
  return render(request, 'payments/payments.html', context={"transactions": transactions})

@login_required
def deposit_funds_view(request):
  if request.POST:
    if not is_valid_deposit(request.POST.get("id_credit")):
      messages.error(request, "Die Einzahlung sollte mehr als 5€ betragen.")
      return render(request, 'payments/deposit_funds.html')
    amount = Decimal(request.POST.get("id_credit")).quantize(Decimal('0.00'))
    payment = Payment(user=request.user,tt_amount=amount)
    payment.save()
    try: 
      pickled_client = BTCPay_Client.objects.get(id=1).pickle_data
      client = pickle.loads(pickled_client)
      #https://github.com/bitpay/python-bitpay-client/blob/master/docs/invoice.md
      #https://bitpay.com/docs/create-invoice
      redirect_url = request.build_absolute_uri(reverse('payments') + "?zahlungsbestätigung")
      notification_url = request.build_absolute_uri(reverse('btcpay_webhook'))
      transactionSpeed = "low" if amount > 1000 else "medium"
      new_invoice = client.create_invoice({"price": str(amount), 
                                          "currency": "EUR",
                                          "orderId": payment.identifier,
                                          "itemDesc": "Guthaben aufladen",
                                          "buyer": {"name": request.user.username},
                                          "redirectURL": redirect_url,
                                          "notificationURL": notification_url,
                                          "transactionSpeed": transactionSpeed
                                          }) #class dict
      payment.invoice_creation_data = new_invoice
      payment.save()
      return redirect(new_invoice["url"]) #leitet weiter zu btcpay
    except Exception as e:
      payment.invoice_creation_error = e
      payment.save()
      messages.error(request, "Ein Fehler ist aufgetreten.")
      return render(request, 'payments/deposit_funds.html')
  return render(request, 'payments/deposit_funds.html')

@require_http_methods(["POST"])
@csrf_exempt
def btcpayserver_webhook(request):
    data = json.loads(request.body)

    try:
      payment_identifier = data["orderId"]
      invoice_id = data["id"]
      payment = Payment.objects.get(identifier=payment_identifier)
    except Exception as e:
      return HttpResponseBadRequest()
    
    #nicht in conditions = [] damit niemand den server mit IPN vollkackt oder mich ripped
    if payment.deposit_unlocked == True or BTCPay_IPN.objects.filter(payment=payment).count() >= 30:
      return HttpResponseBadRequest()  
    
    BTCPay_IPN(webhook_response=data,payment=payment).save() 
    pickled_client = BTCPay_Client.objects.all().last().pickle_data
    client = pickle.loads(pickled_client)
    invoice = client.get_invoice(invoice_id)
    
    conditions = [
      #Payment.identifier is identified through data[orderId]
      #btcpay_invoice is identified through data[id]
      #invoice[orderId] created by TT server in deposit_funds_view
      #check if invoice[orderId] matches with payment_identifier/data[orderId]
      #damit man uns nicht mit mixed data verarscht
      invoice["orderId"] == payment_identifier, 

      #https://bitpay.com/docs/invoice-states
      invoice["status"] == "confirmed" or invoice["status"] == "complete",

      invoice["price"] >= payment.tt_amount,
      math.isclose(Decimal(invoice["btcDue"]),0, rel_tol=1e-9, abs_tol=0.0),

      #invoice["currency"] == payment.currency,
      #unnötig weil btcpay benötigt EUR, tipptafel BTC weil schon 1TT = 1EUR

      #datetime.datetime.fromtimestamp(invoice["expirationTime"]/1000 ,datetime.timezone.utc)>timezone.now()
      #unix time /1000 ms => seconds
      #unnötig weil webhook kann später kommen
    ]
    if all(conditions):
      Balance.objects.filter(user=payment.user).update(amount=F('amount') + payment.tt_amount)
      payment.deposit_unlocked = True
      payment.currency_amount = invoice["btcPaid"]
      payment.save()
      return HttpResponse(status=200)
    else:
      return HttpResponseBadRequest()

  


@login_required
def withdrawview(request):
  if request.POST:
    form = WithdrawalForm(request.POST, request=request)
    if form.is_valid():
      withdraw_amount = form.cleaned_data['tt_amount']
      btc_address = form.cleaned_data['payment_infos']
      fee_amount = withdraw_amount*Decimal(.05) if withdraw_amount < 100 else Decimal(5)
      user_was_promised = get_BTC_rate(withdraw_amount-fee_amount,"EUR")
      Balance.objects.filter(user=request.user).update(amount=F('amount') - withdraw_amount)
      Withdrawal.objects.create(
        user=request.user,
        tt_amount=withdraw_amount,
        fee_amount=fee_amount,
        withdraw_currency="BTC",
        withdraw_currency_amount=user_was_promised,
        withdraw_method="BTC",
        payment_infos={"btc_address":btc_address},
        status="pending"
      )
      messages.success(request, "Auszahlung erfolgreich angefordert! Die Bearbeitung kann 1 bis 2 Werktage benötigen.")
      return redirect('payments')
    else:
      messages.error(request, "Die Auszahlung konnte nicht angefordert werden. \n")
      #str(form.errors.as_text()
      return redirect('withdraw')
  return render(request, 'payments/withdraw.html')



"""
btcpay_webhook response data after json loads
{
   "id":"WrE8YbXhZZg64CaHrRvXcp",
   "url":"https://btcpay110659.lndyn.com/invoice?id=WrE8YbXhZZg64CaHrRvXcp",
   "posData":"None",
   "status":"confirmed",
   "btcPrice":"0.00003520",
   "price":1.0,
   "currency":"EUR",
   "invoiceTime":1688401984000,
   "expirationTime":1688403784000,
   "currentTime":1688405196732,
   "btcPaid":"0.00003520",
   "btcDue":"0.00000000",
   "rate":28413.2,
   "exceptionStatus":false,
   "buyerFields":"None",
   "transactionCurrency":"None",
   "paymentSubtotals":{
      "btc":3520.0,
      "btC_LightningLike":3520.0
   },
   "paymentTotals":{
      "btc":3520.0,
      "btC_LightningLike":3520.0
   },
   "amountPaid":"0.00000000",
   "exchangeRates":{
      "btc":{
         "eur":0.0
      }
   },
   "orderId":"40",
   "_warning":"This data could have easily been faked and should not be trusted. Please run any invoice checks by first fetching the invoice through the API."
}
"""