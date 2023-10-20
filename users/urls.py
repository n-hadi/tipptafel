from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
 path('login/',views.loginview, name='login'),
 path('registrieren/',views.registerview, name="register"),
 path('logout/',views.logoutview,name='logout'),
 path('einstellungen/', views.settingsview, name="settings"),
 path('einstellungen/email_aendern/', views.changemailview, name="changemail"),
 path('einstellungen/passwort_aendern/', views.changepasswordview, name="changepw")
]

htmxpatterns = []

urlpatterns += htmxpatterns

if settings.DEBUG:
 urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 