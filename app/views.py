from django.shortcuts import render, redirect
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
    TemplateView,
)
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin
from app.forms import MatchForm, ContenderForm, LegendCupScoreForm, MatchScoreForm
from app.models import Match, Contender, MatchScore, LegendCupScore, SCORE_MAPPING
from app.tables import MatchTable, ContenderTable
from app.filters import MatchFilterSet
from django.urls import reverse_lazy
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.db.models import Sum
import logging


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
    table_class = MatchTable
    model = Match
    template_name = 'match/match_list.html'
    context_object_name = 'matches'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')

        if search_query:
            queryset = queryset.filter(Q(match_no__icontains=search_query))

        return queryset.order_by('-id')


class ContenderCreate(SuperUserRequiredMixin, CreateView):
    model = Contender
    form_class = ContenderForm
    template_name = 'contender/contender_create_form.html'
    success_url = reverse_lazy('contender_list')


class ContenderUpdate(UpdateView):
    model = Contender
    form_class = ContenderForm
    template_name = 'contender/contender_update_form.html'
    success_url = reverse_lazy('contender_list')


class ContenderDelete(DeleteView):
    model = Contender
    template_name = 'contender/contender_delete.html'
    success_url = reverse_lazy('contender_list')


class ContenderList(ListView):
    model = Contender
    template_name = 'contender/contender_list.html'

    def get_queryset(self):
        return super().get_queryset().order_by('id')


class LegendCupScoreUpdateView(UpdateView):
    model = LegendCupScore
    form_class = LegendCupScoreForm
    template_name = 'legendcup/legendcup_update_form.html'
    success_url = reverse_lazy('legendcup_list')


class LegendCupList(ListView):
    model = LegendCupScore
    template_name = 'legendcup/legendcup_list.html'

    def get_queryset(self):
        return super().get_queryset().order_by('-score')

class LegendCupDelete(DeleteView):
    model = LegendCupScore
    template_name = 'legendcup/legendcup_delete.html'
    success_url = reverse_lazy('legendcup_list')

    def get_object(self):
        pk = self.kwargs['pk']
        return get_object_or_404(Contender, pk=pk)


class MatchScoreCreateView(CreateView):
    model = MatchScore
    form_class = MatchScoreForm
    template_name = 'matchscore/matchscore_create.html'
    success_url = reverse_lazy('match_score_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['matches'] = Match.objects.all()
        context['contender_scores'] = [
            {'contender': contender, 'form': MatchScoreForm(prefix=str(contender.pk))}
            for contender in Contender.objects.all()
        ]
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        contender_scores = [
            {'contender': contender, 'form': MatchScoreForm(request.POST, prefix=str(contender.pk))}
            for contender in Contender.objects.all()
        ]
        if form.is_valid() and all(sub_form.is_valid() for sub_form in [cs['form'] for cs in contender_scores]):
            match = form.cleaned_data.get('match')
            for cs in contender_scores:
                contender = cs['contender']
                score = cs['form'].cleaned_data.get('score')
                obj, created = MatchScore.objects.update_or_create(
                    match=match,
                    contender=contender,
                    defaults={'score': score}
                )
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form, contender_scores=contender_scores))


class MatchScoreList(ListView):
    model = MatchScore
    template_name = 'matchscore/matchscore_list.html'

    def get_queryset(self):
        return super().get_queryset().order_by('-score')


class MatchScoreUpdateView(UpdateView):
    model = MatchScore
    form_class = MatchScoreForm
    template_name = 'matchscore/matchscore_update_form.html'
    success_url = reverse_lazy('match_score_list')


class MatchScoreDelete(DeleteView):
    model = MatchScore
    template_name = 'matchscore/matchscore_delete.html'
    success_url = reverse_lazy('match_score_list')

    def get_object(self):
        pk = self.kwargs['pk']
        return get_object_or_404(MatchScore, pk=pk)


class Dashboard(TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contenders = Contender.objects.all()
        legendcupscore = LegendCupScore.objects.all()
        scores = []

        # Get total score for each contender in each match
        for contender in contenders:
            contender_score = {'name': contender.name, 'total_score': 0}
            match_scores = MatchScore.objects.filter(contender=contender)
            for match_score in match_scores:
                if match_score.score is not None:
                    score_value = match_score.get_score_value()
                    contender_score['total_score'] += score_value

            scores.append(contender_score)

        # Sort scores by total score in descending order
        scores = sorted(scores, key=lambda x: x['total_score'], reverse=True)
        
        # Get the top 3 scores
        context['first_place'] = scores[0]
        context['second_place'] = scores[1]
        context['third_place'] = scores[2]

        context['legendscores'] = legendcupscore
        context['legend_first'] = legendcupscore[0]
        context['scores'] = scores
        return context

    def form_valid(self, form):
        contender_scores = [
            {'contender': contender, 'form': MatchScoreForm(self.request.POST, prefix=str(contender.pk))}
            for contender in Contender.objects.all()
        ]
        if all(sub_form.is_valid() for sub_form in [form] + [cs['form'] for cs in contender_scores]):
            self.object = form.save()
            for cs in contender_scores:
                sub_object = cs['form'].save(commit=False)
                sub_object.match = self.object.match
                sub_object.contender = cs['contender']
                sub_object.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form, contender_scores=contender_scores))
