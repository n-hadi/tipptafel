from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
 path('',views.index, name="index"),
 path('agb/',views.agb, name="agb"),
 path('kontakt/',views.contact, name="contact"),
]

admintpatterns = [
 path('administrator/payback_FBP2P/<match_id>/', views.admin_payback_FBP2P, name="admin_payback")
]

htmxpatterns = [
 path('get/upcoming_games', views.get_games,name="get_games")
]

urlpatterns += htmxpatterns
urlpatterns += admintpatterns

if settings.DEBUG:
 urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 