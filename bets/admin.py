from django.contrib import admin
from .models import FixedBetP2P
import nested_admin 
from simple_history.admin import SimpleHistoryAdmin

class FixedBetP2PAdmin(SimpleHistoryAdmin):
    readonly_fields = ('id','identifier', 'match_status')
    search_fields = ["match__t1__full_name","match__t2__full_name"]
    list_filter = ["match__tournament"]

admin.site.register(FixedBetP2P, FixedBetP2PAdmin)

