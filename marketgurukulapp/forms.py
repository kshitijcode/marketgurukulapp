from django.forms import ModelForm

from .models import Quote


class UserInputForm(ModelForm):
    class Meta:
        model = Quote
        fields = ['symbol']
