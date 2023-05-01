from datetime import timedelta
from django_filters import CharFilter, DateFilter, FilterSet
from app.models import Match, Contender, MatchScore


class MatchFilterSet(FilterSet):
    match_no = CharFilter(field_name="match_no", lookup_expr="icontains", label="Search")

    class Meta:
        model = Match
        fields = ["match_no"]
        