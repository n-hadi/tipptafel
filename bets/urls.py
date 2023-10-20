from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
 path('meine_wetten/', views.mybetsview, name="mybets"),
 path('meine_wetten/wette_erstellen/',views.create_bet,name="create_bet"),
 path('$<identifier>/', views.detail_FBP2P, name="detail_FBP2P"),
]

htmxpatterns = [
 path('get/upcoming_games/<liga>/', views.upcoming_games, name="upcoming_games"),
 path('tippen/',views.tipptafel_take_bet, name="tipptafel_take_bet"),
 path('$<identifier>/take/', views.detail_take_FBP2P, name="detail_take_FBP2P")
]

urlpatterns += htmxpatterns

if settings.DEBUG:
 urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 