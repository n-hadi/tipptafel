import re
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models import User
from django.core.exceptions import ValidationError


class CustomUserCreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ['email', 'username']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) > 1000:
            raise ValidationError('Password too long')
        return password
        
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if type(username) != str:
         raise ValidationError('Nutzername ist kein String.')
        try:
         username_lower = username.lower()
        except ValidationError:
            raise ValidationError('Nutzername ist kein String.')
        if len(username) < 4:
            raise ValidationError('Der Benutzername muss mindestens 4 Zeichen lang sein.')
        nonolist = ['account', 'accounts', 'admin', 'administrator', 'anonymoususer', 'bitcoin', 'captcha', 'chat', 'create', 'customer', 'customers', 'customerservice', 'dashboard', 'delete', 'delete-item', 'email', 'home','inbox', 'index', 'invoice', 'mail','password', 'password_reset', 'payment', 'payment_completed', 'payments', 'paypal', 'tipptafel', 'profile','receive,' 'register', 'reset', 'resets', 'service', 'service', 'transaction', 'transactions', 'user']
        if username_lower in nonolist:
            raise ValidationError('Dieser Benutzername ist nicht erlaubt.')
        namex = re.compile(r'^[0-9a-zA-Z_]{4,20}$')
        if namex.match(username) == None:
            raise forms.ValidationError('Der Benutzername darf nur Buchstaben, Zahlen und Unterstriche enthalten und muss zwischen 4 und 20 Zeichen lang sein.')
        if username.count('_') > 3:
            raise ValidationError('Nicht mehr als 3 Unterstriche erlaubt')
        if username.isdigit():
            raise ValidationError('Der Benutzername muss Buchstaben enthalten')
        if not (any(c.isalpha() for c in username)):
            raise ValidationError('Der Benutzername muss Buchstaben enthalten')
        if username[0] == '_' or username[0].isdigit():
            raise ValidationError('Der Benutzername muss mit einem Buchstaben beginnen')
        if (User.objects.filter(username__iexact=username).exists()):
           raise ValidationError('Der Benutzername ist bereits vergeben.')
        return username



class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['email' ]