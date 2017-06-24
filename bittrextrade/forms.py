from django import forms
from .models import Trade

class TradeForm(forms.ModelForm):

    class Meta:
        model = Trade
        fields = ('coin',)