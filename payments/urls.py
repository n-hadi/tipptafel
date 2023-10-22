from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
  path('payments/btcpay_webhook/', views.btcpayserver_webhook, name='btcpay_webhook')
]
htmxpatterns = [
 path('aufladen/', views.deposit_funds_view, name='deposit_funds'),
 path('zahlungen/', views.paymentsview, name="payments"),
 path('auszahlen/', views.withdrawview, name="withdraw")
]

urlpatterns+= htmxpatterns
if settings.DEBUG:
 urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 