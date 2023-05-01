from django.contrib import admin
from app.models import Match, Contender, MatchScore
# Register your models here.


class MatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'match_no', 'team_names')
    ordering = ('id',)
    
    def team_names(self, obj):
        return f"{obj.team_1} - {obj.team_2}"

admin.site.register(Match, MatchAdmin)


class ContenderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    ordering = ('id',)

admin.site.register(Contender, ContenderAdmin)


class MatchScoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'match', 'contender', 'score')
    list_filter = ('match',)
    ordering = ('id',)

admin.site.register(MatchScore, MatchScoreAdmin)
