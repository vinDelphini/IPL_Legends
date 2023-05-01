from django import forms
from app.models import Match, Contender, MatchScore


class MatchForm(forms.ModelForm):

    class Meta:
        model = Match
        fields = ['match_no', 'team_1', 'team_2']
