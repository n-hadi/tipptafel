from django.contrib import admin
from paybacks_payouts.models import PayoutFBP2P, PaybackFBP2P

# Register your models here.
admin.site.register(PayoutFBP2P)
admin.site.register(PaybackFBP2P)