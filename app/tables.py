import django_tables2 as tables
from django.db.models import Count
from django_tables2.utils import A
from app.models import Match, Contender, MatchScore


class MatchTable(tables.Table):
    match_no = tables.LinkColumn("match-edit", args=[A("id")])

    class Meta:
        model = Match
        template_name = 'match/match_list.html'
        fields = ("match_no",)
        empty_text = "No Matches yet."


class ContenderTable(tables.Table):
    # match_no = tables.LinkColumn("match-edit", args=[A("id")])

    class Meta:
        model = Contender
        template_name = "common/base_table.html"
        fields = ("name",)
        empty_text = "No Contenders yet."
