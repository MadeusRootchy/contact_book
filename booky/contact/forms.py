from django import forms
from django.core.exceptions import ValidationError
from .models import *
from django.contrib.auth.models import User

class NewUserForm(forms.ModelForm):
    modpas = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'my-input-class'}),
        label='Modpas'
    )
    modpas2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'my-input-class'}),
        label='Tape modpas ou ankò pou konfime li'
    )

    class Meta:
        model = NewUser
        fields = ("non", "modpas", "modpas2")  

    def clean(self):
        cleaned_data = super().clean()
        non = cleaned_data.get('non')  
        modpas = cleaned_data.get('modpas')
        modpas2 = cleaned_data.get('modpas2')

        if len(modpas) < 8:
            self.add_error('modpas', 'Modpas la dwe gen 8 karakte minimòm')

        if modpas2 != modpas:
            self.add_error('modpas2', 'Modpas yo pa koresponn!')
