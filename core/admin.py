from django.contrib import admin
from .models import Tournament,Match,Team, HomePageBackground
import nested_admin 
from django_object_actions import DjangoObjectActions, action
from admin_confirm.admin import AdminConfirmMixin, confirm_action
from paybacks_payouts.payout_FBP2P import payout_bets
from django.http import HttpResponseRedirect
from urllib.parse import urlparse
from django.utils.safestring import mark_safe
from django.utils import timezone
from datetime import datetime





class MatchAdmin(DjangoObjectActions,AdminConfirmMixin,admin.ModelAdmin):

    def central_european_time(self, obj): 
        formatted_date = obj.convert_timezone_and_format('Europe/Berlin', "%d.%m.%y - %H:%M")
        return formatted_date
    
    def kickoff(self, obj):
        european_style = obj.start.strftime("%d-%m-%Y %H:%M")
        if obj.start < timezone.now():
            if (obj.t1_goals is None or obj.t2_goals is None) and obj.outcome != "u":
                return mark_safe("<span style='color: red;'>%s</span>" % european_style)
            else:
                return mark_safe("<span style='color: gray;'>%s</span>" % european_style)
        else:
            return european_style


    list_display = ["__str__","kickoff"]
    ordering = ["start"]
    list_filter = ["tournament"]
    fields = ["start", "central_european_time","friendly", "tournament","season","outcome","t1","t2","t1_goals","t2_goals","penalties", "t1_goals_penalties","t2_goals_penalties","draw_impossible","open_db_info"]
    search_fields = ('t1__full_name','t2__full_name')
    readonly_fields = ['id','central_european_time']
    actions = ["Wetten_auszahlen"] #admin-confirm module

    @confirm_action
    @action(label="P2P Festwetten auszahlen",description="Auszahlen und NoUserFound zurückzahlen")  
    def Wetten_auszahlen(modeladmin, request, obj): 
        payout_bets(request, obj)
    Wetten_auszahlen.allowed_permissions = ('change','add') #admin-confirm module

    def Zurückzahlen(self, request, obj): 
        parsed_url = urlparse(request.headers.get('Referer'))
        path = parsed_url.path
        return HttpResponseRedirect(
        "/administrator/payback_FBP2P/%s/?next=%s" % (str(obj.id), path)
    )

    change_actions = ('Wetten_auszahlen', 'Zurückzahlen')  #django-object-actions module

    '''
    def payout_bets_4_all_matches(modeladmin, request, queryset):
        print('im payying out :3')
    changelist_actions = ('payout_bets_4_all_matches', ) 
    '''



admin.site.register(Tournament)
admin.site.register(Match, MatchAdmin)
admin.site.register(Team)
admin.site.register(HomePageBackground)
