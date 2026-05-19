from django import forms
from .models import Klasse, Tisch, SchuelerIn, Vorliebe, Verboten, TischVorliebe


class KlasseForm(forms.ModelForm):
    class Meta:
        model = Klasse
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'z.B. 5a'}),
        }


class TischForm(forms.ModelForm):
    class Meta:
        model = Tisch
        fields = ['name', 'kapazitaet']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'z.B. Tisch 1'}),
            'kapazitaet': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }


class SchuelerInForm(forms.ModelForm):
    class Meta:
        model = SchuelerIn
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
        }


class VorliebeForm(forms.ModelForm):
    class Meta:
        model = Vorliebe
        fields = ['schuelerIn_a', 'schuelerIn_b', 'score']
        widgets = {
            'schuelerIn_a': forms.Select(attrs={'class': 'form-select'}),
            'schuelerIn_b': forms.Select(attrs={'class': 'form-select'}),
            'score': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, klasse=None, **kwargs):
        super().__init__(*args, **kwargs)
        if klasse:
            qs = SchuelerIn.objects.filter(klasse=klasse)
            self.fields['schuelerIn_a'].queryset = qs
            self.fields['schuelerIn_b'].queryset = qs


class VerbotenForm(forms.ModelForm):
    class Meta:
        model = Verboten
        fields = ['schuelerIn_a', 'schuelerIn_b']
        widgets = {
            'schuelerIn_a': forms.Select(attrs={'class': 'form-select'}),
            'schuelerIn_b': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, klasse=None, **kwargs):
        super().__init__(*args, **kwargs)
        if klasse:
            qs = SchuelerIn.objects.filter(klasse=klasse)
            self.fields['schuelerIn_a'].queryset = qs
            self.fields['schuelerIn_b'].queryset = qs


class TischVorliebeForm(forms.ModelForm):
    class Meta:
        model = TischVorliebe
        fields = ['schuelerIn', 'kapazitaet', 'score']
        widgets = {
            'schuelerIn': forms.Select(attrs={'class': 'form-select'}),
            'kapazitaet': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'score': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, klasse=None, **kwargs):
        super().__init__(*args, **kwargs)
        if klasse:
            self.fields['schuelerIn'].queryset = SchuelerIn.objects.filter(klasse=klasse)
