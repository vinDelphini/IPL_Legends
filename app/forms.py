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
    
    class Meta:
        model = MatchScore
        fields = ['match', 'contender', 'score']


class ScoreFilterForm(forms.Form):
    score = forms.ChoiceField(choices=SCORE_CHOICES, required=False, label='Filter by Positions', initial='1')
