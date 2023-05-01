from django.urls import path
from django.views.generic import TemplateView
from app.views import (
    MatchCreate,
    MatchUpdate,
    MatchDelete,
    MatchList,
)
urlpatterns = [
    path('', TemplateView.as_view(template_name='dashboard/dashboard.html', 
                                    extra_context={'title': 'IPL Legends'}),
                                    name='dashboard'),
    path('list', MatchList.as_view(), name='match_list'),
    path('create/', MatchCreate.as_view(), name='match_create'),
    path('<int:pk>/update/', MatchUpdate.as_view(), name='match_update'),
    path('<int:pk>/delete/', MatchDelete.as_view(), name='match_delete'),
]
