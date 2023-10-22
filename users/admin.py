from django.contrib import admin
from .models import User, Balance
from simple_history.admin import SimpleHistoryAdmin
import nested_admin 

class BalanceInline(nested_admin.NestedTabularInline):
  model = Balance

class UserAdmin(nested_admin.NestedModelAdmin):
 inlines = [BalanceInline,]

class BalanceAdmin(SimpleHistoryAdmin):
  model = Balance
  history_list_display = ["amount"]

admin.site.register(User, UserAdmin)
admin.site.register(Balance, BalanceAdmin)