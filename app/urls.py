from django.urls import path
from django.views.generic import TemplateView
from app.views import (
    MatchCreate,
    MatchUpdate,
    MatchDelete,
    MatchList,
    ContenderCreate,
    ContenderUpdate,
    ContenderDelete,
    ContenderList,
    LegendCupScoreUpdateView,
    LegendCupList,
    LegendCupDelete,
    MatchScoreCreateView,
    MatchScoreList,
    MatchScoreUpdateView,
    MatchScoreDelete,
    Dashboard,
)


urlpatterns = [
    # dashboard
    path('', Dashboard.as_view(), name='dashboard'),
    # match
    path('list', MatchList.as_view(), name='match_list'),
    path('create/', MatchCreate.as_view(), name='match_create'),
    path('<int:pk>/update/', MatchUpdate.as_view(), name='match_update'),
    path('<int:pk>/delete/', MatchDelete.as_view(), name='match_delete'),
    # contender
    path('c-list', ContenderList.as_view(), name='contender_list'),
    path('c-create/', ContenderCreate.as_view(), name='contender_create'),
    path('<int:pk>/c-update/', ContenderUpdate.as_view(), name='contender_update'),
    path('<int:pk>/c-delete/', ContenderDelete.as_view(), name='contender_delete'),
    # legend cup
    path('lc-list', LegendCupList.as_view(), name='legendcup_list'),
    path('<int:pk>/lg-update/', LegendCupScoreUpdateView.as_view(), name='legendcup_update'),
    path('<int:pk>/lg-delete/', LegendCupDelete.as_view(), name='legendcup_delete'),
    path('ms-create/', MatchScoreCreateView.as_view(), name='match_score_create'),
    path('ms-list/', MatchScoreList.as_view(), name='match_score_list'),
    path('<int:pk>/ms-update/', MatchScoreUpdateView.as_view(), name='match_score_update'),
    path('<int:pk>/ms-delete/', MatchScoreDelete.as_view(), name='match_score_delete'),
]
