from django.shortcuts import render
from app.mixins import (
    SuperUserRequiredMixin,
)
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
    RedirectView,
    ListView,
)
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin
from app.forms import MatchForm
from app.models import Match, Contender, MatchScore
from app.tables import MatchTable
from app.filters import MatchFilterSet
from django.urls import reverse_lazy
from django.db.models import Q


class MatchCreate(SuperUserRequiredMixin, CreateView):
    model = Match
    form_class = MatchForm
    template_name = 'match/match_create_form.html'
    success_url = reverse_lazy('match_list')


class MatchUpdate(UpdateView):
    model = Match
    form_class = MatchForm
    template_name = 'match/match_update_form.html'
    success_url = reverse_lazy('match_list')


class MatchDelete(DeleteView):
    model = Match
    template_name = 'match/match_delete.html'
    success_url = reverse_lazy('match_list')


class MatchList(ListView):
    model = Match
    template_name = 'match/match_list.html'
    context_object_name = 'matches'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')

        if search_query:
            queryset = queryset.filter(Q(match_no__icontains=search_query))

        return queryset


class ContenderCreate(SuperUserRequiredMixin, CreateView):
    model = Match
    form_class = MatchForm
    template_name = 'contender/contender_create_form.html'
    success_url = reverse_lazy('match_list')


class ContenderUpdate(UpdateView):
    model = Match
    form_class = MatchForm
    template_name = 'contender/contender_update_form.html'
    success_url = reverse_lazy('match_list')


class ContenderDelete(DeleteView):
    model = Match
    template_name = 'contender/contender_delete.html'
    success_url = reverse_lazy('match_list')


class ContenderList(ListView):
    model = Match
    template_name = 'contender/contender_list.html'
