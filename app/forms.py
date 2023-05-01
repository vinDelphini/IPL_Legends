from django import forms
from app.models import Match, Contender, MatchScore, LegendCupScore, SCORE_CHOICES


class MatchForm(forms.ModelForm):

    class Meta:
        model = Match
        fields = ['match_no', 'team_1', 'team_2']


class ContenderForm(forms.ModelForm):

    class Meta:
        model = Contender
        fields = ['name',]


class LegendCupScoreForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['contender'].widget.attrs['disabled'] = 'disabled'

    class Meta:
        model = LegendCupScore
        fields = ['contender', 'score']

    def save(self, commit=True):
        instance = super(LegendCupScoreForm, self).save(commit=False)
        instance.contender = self.cleaned_data['contender']
        if commit:
            instance.save()
        return instance


class MatchScoreForm(forms.ModelForm):
    match = forms.ModelChoiceField(queryset=Match.objects.all(), widget=forms.Select(attrs={'class': 'form-control', 'required': True}))
    contender = forms.ModelChoiceField(queryset=Contender.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    score = forms.ChoiceField(choices=SCORE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = MatchScore
        fields = ['match', 'contender', 'score']
        