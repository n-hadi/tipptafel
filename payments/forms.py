from decimal import Decimal
from django import forms
from .models import Withdrawal
from decimal import Decimal
from django.core.exceptions import ValidationError


def is_valid_deposit(user_input):
    
    if user_input is None:
        return False  # "id-credit" parameter is missing
    
    try:
        numeric_value = Decimal(user_input)  # Convert to float
    except ValueError:
        return False  # Not a valid number
    
    if numeric_value >= 5:
        return True  # Valid number and greater than 5
    
    return False  

class WithdrawalForm(forms.ModelForm):
    payment_infos = forms.CharField(max_length=100)
    class Meta:
        model = Withdrawal
        fields = ["tt_amount", "payment_infos"]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(WithdrawalForm, self).__init__(*args, **kwargs)
    
    def clean(self):
        cleaned_data = super().clean()
        try:
            user = self.request.user
            withdraw_amount = cleaned_data["tt_amount"] 
            bitcoin_address = cleaned_data["payment_infos"]
        except:
            raise ValidationError("Key Error")
        
        try:
            # Attempt to create a Decimal instance from user input
            withdraw_amount = Decimal(withdraw_amount)
        except ValidationError:
            raise ValidationError("This is not a valid decimal number.")
        
        if user.balance.amount < withdraw_amount:
            raise ValidationError("Not enough credit to withdraw.")
        elif withdraw_amount < 10:
            raise ValidationError("Withdraw amount has to be greater than 10.")
        #bitcoin_wallet_addresse nicht validiert aber egal
        return cleaned_data
